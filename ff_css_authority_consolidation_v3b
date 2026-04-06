from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json
import re

ROOT = Path.home() / "futurefunded-enterprise"
FF_CSS = ROOT / "apps/web/app/static/css/ff.css"
ABOVE_CSS = ROOT / "apps/web/app/static/css/ff-above-main-premium.css"
V2_JSON = ROOT / "tools/audit/ff_css_authority_consolidation_v2.json"
OUT_JSON = ROOT / "tools/audit/ff_css_authority_consolidation_v3b.json"
OUT_MD = ROOT / "tools/audit/ff_css_authority_consolidation_v3b.md"

START = "/* FF_FUNDRAISER_AUTHORITY_V3B_START */"
END = "/* FF_FUNDRAISER_AUTHORITY_V3B_END */"
COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)

FALLBACK_TARGETS = [
    ("(top-level)", 'body[data-ff-page="fundraiser"] .ff-topbarGoal'),
    ("(top-level)", 'body[data-ff-page="fundraiser"] .ff-topbarGoal__summary'),
    ("(top-level)", 'body[data-ff-page="fundraiser"] .ff-sponsorGhost'),
    ("(top-level)", 'body[data-ff-page="fundraiser"] .ff-footerMeta'),
    ("(top-level)", 'body[data-ff-page="fundraiser"] .ff-heroAccent'),
    ("(top-level)", 'body[data-ff-page="fundraiser"] .ff-heroName'),
    ("(top-level)", 'body[data-ff-page="fundraiser"] .ff-themeToggle--desktop'),
    ("(top-level)", 'body[data-ff-page="fundraiser"] .ff-topbarGoal__progressWrap .ff-help'),
    ('@media (max-width: 47.99rem)', 'body[data-ff-page="fundraiser"] .ff-heroAccent'),
]


@dataclass
class Rule:
    selector_group: str
    normalized_selector_group: str
    context: tuple[str, ...]
    declarations: str
    start: int
    end: int
    line: int


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except Exception:
        return str(path)


def backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = path.with_suffix(path.suffix + f".bak.{stamp}")
    bak.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return bak


def mask_comments(text: str) -> str:
    return COMMENT_RE.sub(lambda m: " " * (m.end() - m.start()), text)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def split_selector_group(text: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    depth_round = 0
    depth_square = 0
    in_string = False
    string_char = ""

    i = 0
    while i < len(text):
        ch = text[i]
        if in_string:
            buf.append(ch)
            if ch == string_char and (i == 0 or text[i - 1] != "\\"):
                in_string = False
            i += 1
            continue

        if ch in ("'", '"'):
            in_string = True
            string_char = ch
            buf.append(ch)
            i += 1
            continue

        if ch == "(":
            depth_round += 1
        elif ch == ")" and depth_round > 0:
            depth_round -= 1
        elif ch == "[":
            depth_square += 1
        elif ch == "]" and depth_square > 0:
            depth_square -= 1

        if ch == "," and depth_round == 0 and depth_square == 0:
            part = normalize_spaces("".join(buf))
            if part:
                parts.append(part)
            buf = []
            i += 1
            continue

        buf.append(ch)
        i += 1

    tail = normalize_spaces("".join(buf))
    if tail:
        parts.append(tail)
    return parts


def normalize_selector_group(text: str) -> str:
    return ", ".join(split_selector_group(text))


def find_matching_brace(text: str, open_idx: int) -> int:
    depth = 0
    in_string = False
    string_char = ""
    i = open_idx
    while i < len(text):
        ch = text[i]
        if in_string:
            if ch == string_char and text[i - 1] != "\\":
                in_string = False
            i += 1
            continue
        if ch in ("'", '"'):
            in_string = True
            string_char = ch
            i += 1
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    raise ValueError(f"Unmatched brace starting at {open_idx}")


def parse_css_rules(text: str) -> list[Rule]:
    masked = mask_comments(text)
    rules: list[Rule] = []
    recursive_context_headers = ("@media", "@supports", "@container", "@layer")
    skip_at_headers = ("@keyframes", "@font-face", "@property", "@page")

    def walk(start: int, end: int, context: tuple[str, ...]) -> None:
        i = start
        while i < end:
            while i < end and masked[i].isspace():
                i += 1
            if i >= end or masked[i] == "}":
                return

            open_idx = masked.find("{", i, end)
            if open_idx == -1:
                return

            prelude = normalize_spaces(masked[i:open_idx])
            if not prelude:
                i = open_idx + 1
                continue

            close_idx = find_matching_brace(masked, open_idx)
            if close_idx >= end:
                close_idx = end - 1

            block_body = text[open_idx + 1:close_idx]
            line = line_number(text, i)

            if prelude.startswith(recursive_context_headers):
                walk(open_idx + 1, close_idx, context + (prelude,))
            elif prelude.startswith(skip_at_headers):
                pass
            elif prelude.startswith("@"):
                pass
            else:
                rules.append(
                    Rule(
                        selector_group=prelude,
                        normalized_selector_group=normalize_selector_group(prelude),
                        context=context,
                        declarations=block_body.strip(),
                        start=i,
                        end=close_idx + 1,
                        line=line,
                    )
                )

            i = close_idx + 1

    walk(0, len(masked), tuple())
    return rules


def report_context_to_tuple(context: str) -> tuple[str, ...]:
    context = context.strip()
    if not context or context == "(top-level)":
        return tuple()
    return tuple(part.strip() for part in context.split(" | ") if part.strip())


def build_targets() -> list[tuple[tuple[str, ...], str]]:
    targets: list[tuple[tuple[str, ...], str]] = []

    if V2_JSON.exists():
        data = json.loads(V2_JSON.read_text(encoding="utf-8"))
        for item in data.get("merged_groups", []):
            context = report_context_to_tuple(item.get("context", "(top-level)"))
            selector = normalize_selector_group(item.get("selector_group", ""))
            if selector:
                targets.append((context, selector))

    if not targets:
        for context_str, selector in FALLBACK_TARGETS:
            targets.append((report_context_to_tuple(context_str), normalize_selector_group(selector)))

    # de-dup while preserving order
    seen = set()
    ordered = []
    for item in targets:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def build_authority_block(found: list[Rule]) -> str:
    top_level = [r for r in found if not r.context]
    by_context: dict[tuple[str, ...], list[Rule]] = defaultdict(list)
    for rule in found:
        if rule.context:
            by_context[rule.context].append(rule)

    lines: list[str] = [START]
    lines.append("/* Canonical fundraiser component ownership migrated from ff-above-main-premium.css */")
    lines.append("")

    for rule in top_level:
        lines.append(f"{rule.normalized_selector_group} {{")
        for row in rule.declarations.splitlines():
            row = row.rstrip()
            if row:
                lines.append(f"  {row.strip()}")
        lines.append("}")
        lines.append("")

    for context, rules in by_context.items():
        header = context[0] if len(context) == 1 else " ".join(context)
        lines.append(f"{header} {{")
        for rule in rules:
            lines.append(f"  {rule.normalized_selector_group} {{")
            for row in rule.declarations.splitlines():
                row = row.rstrip()
                if row:
                    lines.append(f"    {row.strip()}")
            lines.append("  }")
            lines.append("")
        lines.append("}")
        lines.append("")

    lines.append(END)
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    if not FF_CSS.exists() or not ABOVE_CSS.exists():
        raise SystemExit("❌ Missing ff.css or ff-above-main-premium.css")

    ff_text = FF_CSS.read_text(encoding="utf-8")
    above_text = ABOVE_CSS.read_text(encoding="utf-8")
    rules = parse_css_rules(above_text)
    targets = build_targets()

    index = {(rule.context, rule.normalized_selector_group): rule for rule in rules}
    found: list[Rule] = []
    missing: list[dict] = []

    for context, selector in targets:
        rule = index.get((context, selector))
        if rule:
            found.append(rule)
        else:
            missing.append(
                {
                    "context": "(top-level)" if not context else " | ".join(context),
                    "selector_group": selector,
                }
            )

    if not found:
        print("== FF CSS AUTHORITY CONSOLIDATION V3B ==")
        print("❌ matcher found 0 migratable rules")
        print("candidate targets checked:")
        for item in missing[:20]:
            print(f" - {item['context']} :: {item['selector_group']}")
        return

    authority_block = build_authority_block(found)

    if START in ff_text and END in ff_text:
        ff_updated = re.sub(
            re.escape(START) + r".*?" + re.escape(END),
            authority_block.strip(),
            ff_text,
            flags=re.S,
        )
    else:
        ff_updated = ff_text.rstrip() + "\n\n" + authority_block

    removals: list[tuple[int, int, str]] = []
    moved_rules: list[dict] = []

    for rule in found:
        removals.append(
            (
                rule.start,
                rule.end,
                f"\n/* FF_CSS_AUTHORITY_CONSOLIDATION_V3B moved to ff.css authority block: {rule.normalized_selector_group} */\n",
            )
        )
        moved_rules.append(
            {
                "context": "(top-level)" if not rule.context else " | ".join(rule.context),
                "selector_group": rule.normalized_selector_group,
                "from_file": rel(ABOVE_CSS),
                "from_line": rule.line,
                "to_file": rel(FF_CSS),
            }
        )

    above_updated = above_text
    for start, end, replacement in sorted(removals, key=lambda x: x[0], reverse=True):
        above_updated = above_updated[:start] + replacement + above_updated[end:]

    ff_bak = backup(FF_CSS)
    above_bak = backup(ABOVE_CSS)
    FF_CSS.write_text(ff_updated, encoding="utf-8")
    ABOVE_CSS.write_text(above_updated, encoding="utf-8")

    report = {
        "files": {
            "ff_css": rel(FF_CSS),
            "above_css": rel(ABOVE_CSS),
            "ff_backup": rel(ff_bak),
            "above_backup": rel(above_bak),
        },
        "counts": {
            "candidate_targets": len(targets),
            "moved_rules": len(moved_rules),
            "missing_targets": len(missing),
        },
        "moved_rules": moved_rules,
        "missing_targets": missing,
    }

    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md: list[str] = []
    md.append("# FF CSS Authority Consolidation V3B")
    md.append("")
    md.append("## Summary")
    md.append("")
    for k, v in report["counts"].items():
        md.append(f"- **{k}**: {v}")
    md.append("")
    md.append("## Moved rules")
    md.append("")
    for item in moved_rules:
        md.append(f"- `{item['selector_group']}`")
        md.append(f"  - Context: `{item['context']}`")
        md.append(f"  - From: `{item['from_file']}:{item['from_line']}`")
        md.append(f"  - To: `{item['to_file']}`")
    md.append("")
    md.append("## Missing targets")
    md.append("")
    for item in missing:
        md.append(f"- `{item['context']}` :: `{item['selector_group']}`")
    md.append("")
    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    print("== FF CSS AUTHORITY CONSOLIDATION V3B ==")
    print(f"ff.css backup      : {rel(ff_bak)}")
    print(f"shim backup        : {rel(above_bak)}")
    print(f"candidate targets  : {len(targets)}")
    print(f"moved rules        : {len(moved_rules)}")
    print(f"missing targets    : {len(missing)}")
    print(f"json report        : {rel(OUT_JSON)}")
    print(f"md report          : {rel(OUT_MD)}")

    print("\n== MOVED RULES (sample) ==")
    for item in moved_rules[:20]:
        print(f" - {item['selector_group']}")
        print(f"   context: {item['context']}")
        print(f"   from   : {item['from_file']}:{item['from_line']}")
        print(f"   to     : {item['to_file']}")

    if missing:
        print("\n== MISSING TARGETS (sample) ==")
        for item in missing[:20]:
            print(f" - {item['context']} :: {item['selector_group']}")


if __name__ == "__main__":
    main()
