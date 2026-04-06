from __future__ import annotations

from pathlib import Path
from collections import defaultdict, Counter
import json
import re
from typing import Dict, List, Set, Tuple

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATES_ROOT = ROOT / "apps/web/app/templates"
STATIC_ROOT = ROOT / "apps/web/app/static"
ENTRY_TEMPLATE = ROOT / "apps/web/app/templates/campaign/index.html"

DEFAULT_CSS_CANDIDATES = [
    ROOT / "apps/web/app/static/css/ff.css",
    ROOT / "apps/web/app/static/css/ff-above-main-premium.css",
    ROOT / "apps/web/app/static/css/platform-pages.css",
]

OUT_JSON = ROOT / "tools/audit/ff_css_contract_map_v1.json"
OUT_MD = ROOT / "tools/audit/ff_css_contract_map_v1.md"


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


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def find_related_templates(entry: Path, templates_root: Path) -> List[Path]:
    patterns = [
        re.compile(r'{%\s*extends\s+["\']([^"\']+\.html)["\']'),
        re.compile(r'{%\s*include\s+["\']([^"\']+\.html)["\']'),
        re.compile(r'{%\s*from\s+["\']([^"\']+\.html)["\']\s+import'),
        re.compile(r'{%\s*import\s+["\']([^"\']+\.html)["\']'),
    ]

    seen: Set[Path] = set()
    ordered: List[Path] = []

    def visit(path: Path) -> None:
        if path in seen or not path.exists():
            return
        seen.add(path)
        ordered.append(path)

        text = read_text(path)
        for rx in patterns:
            for match in rx.finditer(text):
                target = match.group(1).strip()
                child = templates_root / target
                if child.exists():
                    visit(child)

    visit(entry)
    return ordered


def find_linked_css(template_paths: List[Path]) -> List[Path]:
    found: List[Path] = []
    seen: Set[Path] = set()

    patterns = [
        re.compile(r'filename\s*=\s*["\']css/([^"\']+\.css)["\']'),
        re.compile(r'href\s*=\s*["\']/static/css/([^"\']+\.css)["\']'),
        re.compile(r'href\s*=\s*["\'](?:\.\./)?(?:\.\./)?static/css/([^"\']+\.css)["\']'),
    ]

    for path in template_paths:
        text = read_text(path)
        for rx in patterns:
            for match in rx.finditer(text):
                css_name = match.group(1).strip()
                css_path = STATIC_ROOT / "css" / css_name
                if css_path.exists() and css_path not in seen:
                    seen.add(css_path)
                    found.append(css_path)

    for css_path in DEFAULT_CSS_CANDIDATES:
        if css_path.exists() and css_path not in seen:
            seen.add(css_path)
            found.append(css_path)

    return found


def extract_template_contract_tokens(template_paths: List[Path]) -> Dict[str, Set[str]]:
    classes: Set[str] = set()
    ids: Set[str] = set()
    hooks: Set[str] = set()

    attr_patterns = [
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

        for rx in attr_patterns:
            for match in rx.finditer(text):
                raw = strip_jinja(match.group(1))
                raw = normalize_spaces(raw)
                if not raw:
                    continue
                for token in raw.split(" "):
                    if token and not token.startswith(("{{", "{%")):
                        classes.add(token)

        for rx in id_patterns:
            for match in rx.finditer(text):
                raw = strip_jinja(match.group(1))
                raw = normalize_spaces(raw)
                if raw:
                    ids.add(raw)

        for match in hook_pattern.finditer(text):
            hooks.add(match.group(1))

    return {
        "classes": classes,
        "ids": ids,
        "hooks": hooks,
    }


def strip_css_comments(text: str) -> str:
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)


def line_number_from_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def parse_css_token_origins(css_paths: List[Path]) -> Dict[str, List[dict]]:
    token_origins: Dict[str, List[dict]] = defaultdict(list)

    selector_block_pattern = re.compile(r'([^{]+)\{', re.S)
    class_token_pattern = re.compile(r'\.([A-Za-z_][A-Za-z0-9_-]*)')
    id_token_pattern = re.compile(r'#([A-Za-z_][A-Za-z0-9_-]*)')
    hook_token_pattern = re.compile(r'\[(data-ff-[A-Za-z0-9_-]+)(?:[~|^$*]?=[^\]]+)?\]')

    for css_path in css_paths:
        original = read_text(css_path)
        text = strip_css_comments(original)

        for match in selector_block_pattern.finditer(text):
            raw_selector_group = match.group(1).strip()
            if not raw_selector_group or raw_selector_group.startswith("@"):
                continue

            lineno = line_number_from_offset(original, match.start())

            for selector in raw_selector_group.split(","):
                selector = normalize_spaces(selector)
                if not selector:
                    continue

                class_tokens = {f".{m.group(1)}" for m in class_token_pattern.finditer(selector)}
                id_tokens = {f"#{m.group(1)}" for m in id_token_pattern.finditer(selector)}
                hook_tokens = {f"[{m.group(1)}]" for m in hook_token_pattern.finditer(selector)}

                for token in sorted(class_tokens | id_tokens | hook_tokens):
                    token_origins[token].append(
                        {
                            "file": rel(css_path),
                            "line": lineno,
                            "selector": selector,
                        }
                    )

    return token_origins


def summarize_duplicates(token_origins: Dict[str, List[dict]], used_tokens: Set[str]) -> dict:
    cross_file = {}
    same_file = {}

    for token, origins in token_origins.items():
        if token not in used_tokens:
            continue

        files = [o["file"] for o in origins]
        file_counts = Counter(files)

        if len(set(files)) > 1:
            cross_file[token] = origins

        multi_same_file = [f for f, c in file_counts.items() if c > 1]
        if multi_same_file:
            same_file[token] = origins

    return {
        "cross_file_duplicates": cross_file,
        "same_file_duplicates": same_file,
    }


def build_report() -> dict:
    if not ENTRY_TEMPLATE.exists():
        raise SystemExit(f"❌ entry template not found: {ENTRY_TEMPLATE}")

    templates = find_related_templates(ENTRY_TEMPLATE, TEMPLATES_ROOT)
    css_files = find_linked_css(templates)
    contract = extract_template_contract_tokens(templates)
    token_origins = parse_css_token_origins(css_files)

    used_class_tokens = {f".{x}" for x in contract["classes"]}
    used_id_tokens = {f"#{x}" for x in contract["ids"]}
    used_hook_tokens = {f"[{x}]" for x in contract["hooks"]}

    used_tokens = used_class_tokens | used_id_tokens | used_hook_tokens
    css_defined_tokens = set(token_origins.keys())

    missing_classes = sorted(t for t in used_class_tokens if t not in css_defined_tokens)
    missing_ids = sorted(t for t in used_id_tokens if t not in css_defined_tokens)

    # Hooks are frequently JS-only; still useful to inspect but not necessarily an issue.
    missing_hooks = sorted(t for t in used_hook_tokens if t not in css_defined_tokens)

    unused_css_tokens = sorted(t for t in css_defined_tokens if t not in used_tokens)

    duplicates = summarize_duplicates(token_origins, used_tokens)

    file_defined_counts = defaultdict(int)
    for token, origins in token_origins.items():
        for origin in origins:
            file_defined_counts[origin["file"]] += 1

    report = {
        "entry_template": rel(ENTRY_TEMPLATE),
        "related_templates": [rel(p) for p in templates],
        "linked_css_files": [rel(p) for p in css_files],
        "counts": {
            "templates_scanned": len(templates),
            "css_files_scanned": len(css_files),
            "used_classes": len(contract["classes"]),
            "used_ids": len(contract["ids"]),
            "used_hooks": len(contract["hooks"]),
            "css_defined_tokens": len(css_defined_tokens),
            "missing_classes": len(missing_classes),
            "missing_ids": len(missing_ids),
            "missing_hooks": len(missing_hooks),
            "unused_css_tokens": len(unused_css_tokens),
            "cross_file_duplicates": len(duplicates["cross_file_duplicates"]),
            "same_file_duplicates": len(duplicates["same_file_duplicates"]),
        },
        "template_contract": {
            "classes": sorted(contract["classes"]),
            "ids": sorted(contract["ids"]),
            "hooks": sorted(contract["hooks"]),
        },
        "missing": {
            "classes": missing_classes,
            "ids": missing_ids,
            "hooks": missing_hooks,
        },
        "duplicates": duplicates,
        "unused_css_tokens_sample": unused_css_tokens[:400],
        "file_defined_counts": dict(sorted(file_defined_counts.items())),
        "token_origins_sample": {
            token: origins
            for token, origins in sorted(token_origins.items())[:400]
        },
    }

    return report


def write_markdown(report: dict) -> None:
    counts = report["counts"]
    linked_css = report["linked_css_files"]
    related_templates = report["related_templates"]
    missing = report["missing"]
    duplicates = report["duplicates"]

    md = []
    md.append("# FF CSS Contract Map V1")
    md.append("")
    md.append(f"**Entry template:** `{report['entry_template']}`")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append(f"- Templates scanned: **{counts['templates_scanned']}**")
    md.append(f"- CSS files scanned: **{counts['css_files_scanned']}**")
    md.append(f"- Used classes: **{counts['used_classes']}**")
    md.append(f"- Used ids: **{counts['used_ids']}**")
    md.append(f"- Used hooks: **{counts['used_hooks']}**")
    md.append(f"- Missing classes: **{counts['missing_classes']}**")
    md.append(f"- Missing ids: **{counts['missing_ids']}**")
    md.append(f"- Missing hooks: **{counts['missing_hooks']}**")
    md.append(f"- Cross-file duplicates: **{counts['cross_file_duplicates']}**")
    md.append(f"- Same-file duplicates: **{counts['same_file_duplicates']}**")
    md.append(f"- Unused CSS token sample size: **{len(report['unused_css_tokens_sample'])}**")
    md.append("")
    md.append("## Related templates")
    md.append("")
    for p in related_templates:
        md.append(f"- `{p}`")
    md.append("")
    md.append("## Linked CSS files")
    md.append("")
    for p in linked_css:
        md.append(f"- `{p}`")
    md.append("")
    md.append("## Missing classes (sample)")
    md.append("")
    for token in missing["classes"][:80]:
        md.append(f"- `{token}`")
    md.append("")
    md.append("## Missing ids (sample)")
    md.append("")
    for token in missing["ids"][:80]:
        md.append(f"- `{token}`")
    md.append("")
    md.append("## Missing hooks (sample, may be JS-only)")
    md.append("")
    for token in missing["hooks"][:80]:
        md.append(f"- `{token}`")
    md.append("")
    md.append("## Cross-file duplicates (sample)")
    md.append("")
    for token, origins in list(duplicates["cross_file_duplicates"].items())[:80]:
        md.append(f"- `{token}`")
        for origin in origins[:8]:
            md.append(
                f"  - `{origin['file']}:{origin['line']}` — `{origin['selector']}`"
            )
    md.append("")
    md.append("## Same-file duplicates (sample)")
    md.append("")
    for token, origins in list(duplicates["same_file_duplicates"].items())[:80]:
        md.append(f"- `{token}`")
        for origin in origins[:8]:
            md.append(
                f"  - `{origin['file']}:{origin['line']}` — `{origin['selector']}`"
            )
    md.append("")
    md.append("## Unused CSS tokens (sample)")
    md.append("")
    for token in report["unused_css_tokens_sample"][:120]:
        md.append(f"- `{token}`")
    md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    report = build_report()

    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_markdown(report)

    counts = report["counts"]

    print("== FF CSS CONTRACT MAP V1 ==")
    print(f"entry template : {report['entry_template']}")
    print(f"templates      : {counts['templates_scanned']}")
    print(f"css files      : {counts['css_files_scanned']}")
    print(f"used classes   : {counts['used_classes']}")
    print(f"used ids       : {counts['used_ids']}")
    print(f"used hooks     : {counts['used_hooks']}")
    print(f"missing classes: {counts['missing_classes']}")
    print(f"missing ids    : {counts['missing_ids']}")
    print(f"missing hooks  : {counts['missing_hooks']}  (not always bad)")
    print(f"cross-file dups: {counts['cross_file_duplicates']}")
    print(f"same-file dups : {counts['same_file_duplicates']}")
    print(f"json report    : {rel(OUT_JSON)}")
    print(f"md report      : {rel(OUT_MD)}")

    if report["linked_css_files"]:
        print("\n== LINKED CSS FILES ==")
        for p in report["linked_css_files"]:
            print(f" - {p}")

    if report["missing"]["classes"]:
        print("\n== MISSING CLASSES (sample) ==")
        for token in report["missing"]["classes"][:25]:
            print(f" - {token}")

    if report["duplicates"]["cross_file_duplicates"]:
        print("\n== CROSS-FILE DUPLICATES (sample) ==")
        for token, origins in list(report["duplicates"]["cross_file_duplicates"].items())[:20]:
            print(f" - {token}")
            for origin in origins[:5]:
                print(f"    • {origin['file']}:{origin['line']} :: {origin['selector']}")


if __name__ == "__main__":
    main()
