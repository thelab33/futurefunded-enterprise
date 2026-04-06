from __future__ import annotations

from pathlib import Path
from collections import defaultdict, Counter
import json
import re

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATES_ROOT = ROOT / "apps/web/app/templates"
STATIC_ROOT = ROOT / "apps/web/app/static"
ENTRY_TEMPLATE = ROOT / "apps/web/app/templates/campaign/index.html"

FF_CSS = ROOT / "apps/web/app/static/css/ff.css"
ABOVE_CSS = ROOT / "apps/web/app/static/css/ff-above-main-premium.css"
PLATFORM_CSS = ROOT / "apps/web/app/static/css/platform-pages.css"

OUT_JSON = ROOT / "tools/audit/ff_css_authority_map_v2.json"
OUT_MD = ROOT / "tools/audit/ff_css_authority_map_v2.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except Exception:
        return str(path)


def strip_jinja(text: str) -> str:
    text = re.sub(r"{#.*?#}", " ", text, flags=re.S)
    text = re.sub(r"{%.*?%}", " ", text, flags=re.S)
    text = re.sub(r"{{.*?}}", " ", text, flags=re.S)
    return text


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def line_no(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def find_related_templates(entry: Path, templates_root: Path) -> list[Path]:
    patterns = [
        re.compile(r'{%\s*extends\s+["\']([^"\']+\.html)["\']'),
        re.compile(r'{%\s*include\s+["\']([^"\']+\.html)["\']'),
        re.compile(r'{%\s*from\s+["\']([^"\']+\.html)["\']\s+import'),
        re.compile(r'{%\s*import\s+["\']([^"\']+\.html)["\']'),
    ]

    seen: set[Path] = set()
    ordered: list[Path] = []

    def visit(path: Path) -> None:
        if path in seen or not path.exists():
            return
        seen.add(path)
        ordered.append(path)
        text = read_text(path)
        for rx in patterns:
            for m in rx.finditer(text):
                target = m.group(1).strip()
                child = templates_root / target
                if child.exists():
                    visit(child)

    visit(entry)
    return ordered


def find_linked_css(template_paths: list[Path]) -> list[Path]:
    found: list[Path] = []
    seen: set[Path] = set()

    patterns = [
        re.compile(r'filename\s*=\s*["\']css/([^"\']+\.css)["\']'),
        re.compile(r'href\s*=\s*["\']/static/css/([^"\']+\.css)["\']'),
        re.compile(r'href\s*=\s*["\'](?:\.\./)?(?:\.\./)?static/css/([^"\']+\.css)["\']'),
    ]

    for path in template_paths:
        text = read_text(path)
        for rx in patterns:
            for m in rx.finditer(text):
                css_name = m.group(1).strip()
                css_path = STATIC_ROOT / "css" / css_name
                if css_path.exists() and css_path not in seen:
                    seen.add(css_path)
                    found.append(css_path)

    for fallback in [FF_CSS, ABOVE_CSS, PLATFORM_CSS]:
        if fallback.exists() and fallback not in seen:
            seen.add(fallback)
            found.append(fallback)

    return found


def extract_template_contract(template_paths: list[Path]) -> dict[str, set[str]]:
    classes: set[str] = set()
    ids: set[str] = set()
    hooks: set[str] = set()

    class_patterns = [
        re.compile(r'class\s*=\s*"([^"]*)"'),
        re.compile(r"class\s*=\s*'([^']*)'"),
    ]
    id_patterns = [
        re.compile(r'id\s*=\s*"([^"]+)"'),
        re.compile(r"id\s*=\s*'([^']+)'"),
    ]
    hook_pattern = re.compile(r'\b(data-ff-[A-Za-z0-9_-]+)\s*=')

    for path in template_paths:
        text = read_text(path)

        for rx in class_patterns:
            for m in rx.finditer(text):
                raw = norm(strip_jinja(m.group(1)))
                if not raw:
                    continue
                for token in raw.split(" "):
                    if token and not token.startswith(("{", "}")):
                        classes.add(token)

        for rx in id_patterns:
            for m in rx.finditer(text):
                raw = norm(strip_jinja(m.group(1)))
                if raw:
                    ids.add(raw)

        for m in hook_pattern.finditer(text):
            hooks.add(m.group(1))

    return {"classes": classes, "ids": ids, "hooks": hooks}


def strip_css_comments(text: str) -> str:
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


def split_top_level_selector_groups(css_text: str) -> list[tuple[str, int]]:
    cleaned = strip_css_comments(css_text)
    out: list[tuple[str, int]] = []

    depth = 0
    buf = []
    group_start = 0

    for i, ch in enumerate(cleaned):
        if ch == "{":
            if depth == 0:
                selector = "".join(buf).strip()
                if selector:
                    out.append((selector, group_start))
                buf = []
            depth += 1
        elif ch == "}":
            depth = max(0, depth - 1)
            if depth == 0:
                group_start = i + 1
        else:
            if depth == 0:
                buf.append(ch)

    return out


CLASS_RX = re.compile(r'\.([A-Za-z_][A-Za-z0-9_-]*)')
ID_RX = re.compile(r'#([A-Za-z_][A-Za-z0-9_-]*)')
HOOK_RX = re.compile(r'\[(data-ff-[A-Za-z0-9_-]+)(?:[~|^$*]?=[^\]]+)?\]')


def tokenize_selector(selector: str) -> set[str]:
    tokens = set()
    tokens |= {f".{m.group(1)}" for m in CLASS_RX.finditer(selector)}
    tokens |= {f"#{m.group(1)}" for m in ID_RX.finditer(selector)}
    tokens |= {f"[{m.group(1)}]" for m in HOOK_RX.finditer(selector)}
    return tokens


def classify_selector(selector: str, css_path: Path) -> str:
    s = norm(selector)

    is_platform = 'body[data-ff-template="platform"]' in s
    is_fundraiser = 'body[data-ff-page="fundraiser"]' in s
    in_ff = css_path == FF_CSS
    in_above = css_path == ABOVE_CSS
    in_platform_file = css_path == PLATFORM_CSS

    if is_platform:
        return "platform_only"

    if in_platform_file and not is_fundraiser:
        return "platform_only"

    if in_above and is_fundraiser:
        return "scoped_override"

    if in_ff:
        return "authority"

    if in_above and not is_fundraiser:
        return "review_scope"

    return "unclassified"


def parse_css_origins(css_paths: list[Path]) -> dict[str, list[dict]]:
    token_map: dict[str, list[dict]] = defaultdict(list)

    for css_path in css_paths:
        original = read_text(css_path)
        selector_groups = split_top_level_selector_groups(original)

        for raw_group, offset in selector_groups:
            selectors = [norm(x) for x in raw_group.split(",") if norm(x)]
            if not selectors:
                continue
            lineno = line_no(original, offset)

            for selector in selectors:
                if selector.startswith("@"):
                    continue

                kind = classify_selector(selector, css_path)
                tokens = tokenize_selector(selector)

                for token in sorted(tokens):
                    token_map[token].append({
                        "file": rel(css_path),
                        "line": lineno,
                        "selector": selector,
                        "kind": kind,
                    })

    return token_map


def summarize(token_map: dict[str, list[dict]], used_tokens: set[str]) -> dict:
    results = {
        "authority_tokens": {},
        "scoped_override_tokens": {},
        "platform_only_tokens": {},
        "suspicious_cross_file_duplicates": {},
        "dead_or_unmapped_tokens": [],
        "move_to_ff_css": {},
        "keep_in_above_css": {},
        "keep_in_platform_css": {},
    }

    for token, origins in sorted(token_map.items()):
        files = {o["file"] for o in origins}
        kinds = {o["kind"] for o in origins}
        is_used = token in used_tokens

        if not is_used:
            results["dead_or_unmapped_tokens"].append(token)

        if "authority" in kinds:
            results["authority_tokens"][token] = origins

        if "scoped_override" in kinds:
            results["scoped_override_tokens"][token] = origins

        if "platform_only" in kinds:
            results["platform_only_tokens"][token] = origins

        if len(files) > 1 and is_used:
            authority_files = {o["file"] for o in origins if o["kind"] == "authority"}
            override_files = {o["file"] for o in origins if o["kind"] == "scoped_override"}
            platform_files = {o["file"] for o in origins if o["kind"] == "platform_only"}

            suspicious = False
            if len(authority_files) > 1:
                suspicious = True
            if authority_files and platform_files:
                suspicious = True
            if (ABOVE_CSS.exists() and rel(ABOVE_CSS) in files and rel(FF_CSS) in files and
                    "scoped_override" not in kinds):
                suspicious = True

            if suspicious:
                results["suspicious_cross_file_duplicates"][token] = origins

        has_ff = any(o["file"] == rel(FF_CSS) for o in origins)
        has_above = any(o["file"] == rel(ABOVE_CSS) for o in origins)
        has_platform = any(o["file"] == rel(PLATFORM_CSS) for o in origins)

        if is_used:
            if has_above and not has_ff and token.startswith(".ff-"):
                results["move_to_ff_css"][token] = origins
            if has_above and any(o["kind"] == "scoped_override" for o in origins):
                results["keep_in_above_css"][token] = origins
            if has_platform and all(o["kind"] == "platform_only" for o in origins):
                results["keep_in_platform_css"][token] = origins

    return results


def build_report() -> dict:
    if not ENTRY_TEMPLATE.exists():
        raise SystemExit(f"❌ entry template missing: {ENTRY_TEMPLATE}")

    templates = find_related_templates(ENTRY_TEMPLATE, TEMPLATES_ROOT)
    css_files = find_linked_css(templates)
    contract = extract_template_contract(templates)
    token_map = parse_css_origins(css_files)

    used_class_tokens = {f".{x}" for x in contract["classes"]}
    used_id_tokens = {f"#{x}" for x in contract["ids"]}
    used_hook_tokens = {f"[{x}]" for x in contract["hooks"]}
    used_tokens = used_class_tokens | used_id_tokens | used_hook_tokens

    summaries = summarize(token_map, used_tokens)

    counts = {
        "templates_scanned": len(templates),
        "css_files_scanned": len(css_files),
        "used_classes": len(contract["classes"]),
        "used_ids": len(contract["ids"]),
        "used_hooks": len(contract["hooks"]),
        "authority_tokens": len(summaries["authority_tokens"]),
        "scoped_override_tokens": len(summaries["scoped_override_tokens"]),
        "platform_only_tokens": len(summaries["platform_only_tokens"]),
        "suspicious_cross_file_duplicates": len(summaries["suspicious_cross_file_duplicates"]),
        "dead_or_unmapped_tokens": len(summaries["dead_or_unmapped_tokens"]),
        "move_to_ff_css": len(summaries["move_to_ff_css"]),
        "keep_in_above_css": len(summaries["keep_in_above_css"]),
        "keep_in_platform_css": len(summaries["keep_in_platform_css"]),
    }

    return {
        "entry_template": rel(ENTRY_TEMPLATE),
        "related_templates": [rel(p) for p in templates],
        "linked_css_files": [rel(p) for p in css_files],
        "counts": counts,
        "template_contract": {
            "classes": sorted(contract["classes"]),
            "ids": sorted(contract["ids"]),
            "hooks": sorted(contract["hooks"]),
        },
        "authority_tokens_sample": dict(list(summaries["authority_tokens"].items())[:200]),
        "scoped_override_tokens_sample": dict(list(summaries["scoped_override_tokens"].items())[:200]),
        "platform_only_tokens_sample": dict(list(summaries["platform_only_tokens"].items())[:200]),
        "suspicious_cross_file_duplicates": summaries["suspicious_cross_file_duplicates"],
        "dead_or_unmapped_tokens_sample": summaries["dead_or_unmapped_tokens"][:400],
        "move_to_ff_css": summaries["move_to_ff_css"],
        "keep_in_above_css": summaries["keep_in_above_css"],
        "keep_in_platform_css": summaries["keep_in_platform_css"],
    }


def write_markdown(report: dict) -> None:
    c = report["counts"]
    md = []

    md.append("# FF CSS Authority Map V2")
    md.append("")
    md.append(f"**Entry template:** `{report['entry_template']}`")
    md.append("")
    md.append("## Summary")
    md.append("")
    for k, v in c.items():
        md.append(f"- **{k}**: {v}")
    md.append("")
    md.append("## Related templates")
    md.append("")
    for p in report["related_templates"]:
        md.append(f"- `{p}`")
    md.append("")
    md.append("## Linked CSS files")
    md.append("")
    for p in report["linked_css_files"]:
        md.append(f"- `{p}`")
    md.append("")
    md.append("## Move to ff.css (sample)")
    md.append("")
    for token, origins in list(report["move_to_ff_css"].items())[:80]:
        md.append(f"- `{token}`")
        for o in origins[:6]:
            md.append(f"  - `{o['file']}:{o['line']}` — `{o['kind']}` — `{o['selector']}`")
    md.append("")
    md.append("## Keep in ff-above-main-premium.css (sample)")
    md.append("")
    for token, origins in list(report["keep_in_above_css"].items())[:80]:
        md.append(f"- `{token}`")
        for o in origins[:6]:
            md.append(f"  - `{o['file']}:{o['line']}` — `{o['kind']}` — `{o['selector']}`")
    md.append("")
    md.append("## Suspicious cross-file duplicates (sample)")
    md.append("")
    for token, origins in list(report["suspicious_cross_file_duplicates"].items())[:80]:
        md.append(f"- `{token}`")
        for o in origins[:8]:
            md.append(f"  - `{o['file']}:{o['line']}` — `{o['kind']}` — `{o['selector']}`")
    md.append("")
    md.append("## Dead or unmapped tokens (sample)")
    md.append("")
    for token in report["dead_or_unmapped_tokens_sample"][:120]:
        md.append(f"- `{token}`")
    md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    report = build_report()
    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_markdown(report)

    c = report["counts"]

    print("== FF CSS AUTHORITY MAP V2 ==")
    print(f"entry template                  : {report['entry_template']}")
    print(f"templates scanned               : {c['templates_scanned']}")
    print(f"css files scanned               : {c['css_files_scanned']}")
    print(f"used classes                    : {c['used_classes']}")
    print(f"used ids                        : {c['used_ids']}")
    print(f"used hooks                      : {c['used_hooks']}")
    print(f"authority tokens                : {c['authority_tokens']}")
    print(f"scoped override tokens          : {c['scoped_override_tokens']}")
    print(f"platform-only tokens            : {c['platform_only_tokens']}")
    print(f"suspicious cross-file dups      : {c['suspicious_cross_file_duplicates']}")
    print(f"dead/unmapped token sample size : {c['dead_or_unmapped_tokens']}")
    print(f"move to ff.css                  : {c['move_to_ff_css']}")
    print(f"keep in above css               : {c['keep_in_above_css']}")
    print(f"keep in platform css            : {c['keep_in_platform_css']}")
    print(f"json report                     : {rel(OUT_JSON)}")
    print(f"md report                       : {rel(OUT_MD)}")

    print("\n== LINKED CSS FILES ==")
    for p in report["linked_css_files"]:
        print(f" - {p}")

    if report["move_to_ff_css"]:
        print("\n== MOVE TO FF.CSS (sample) ==")
        for token, origins in list(report["move_to_ff_css"].items())[:20]:
            print(f" - {token}")
            for o in origins[:5]:
                print(f"    • {o['file']}:{o['line']} :: {o['kind']} :: {o['selector']}")

    if report["suspicious_cross_file_duplicates"]:
        print("\n== SUSPICIOUS CROSS-FILE DUPLICATES (sample) ==")
        for token, origins in list(report["suspicious_cross_file_duplicates"].items())[:20]:
            print(f" - {token}")
            for o in origins[:6]:
                print(f"    • {o['file']}:{o['line']} :: {o['kind']} :: {o['selector']}")


if __name__ == "__main__":
    main()
