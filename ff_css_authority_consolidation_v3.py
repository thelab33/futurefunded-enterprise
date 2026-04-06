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
OUT_JSON = ROOT / "tools/audit/ff_css_authority_consolidation_v3.json"
OUT_MD = ROOT / "tools/audit/ff_css_authority_consolidation_v3.md"

START = "/* FF_FUNDRAISER_AUTHORITY_V3_START */"
END = "/* FF_FUNDRAISER_AUTHORITY_V3_END */"
COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)

MOVE_TOP_LEVEL = [
    'body[data-ff-page="fundraiser"] .ff-topbarGoal',
    'body[data-ff-page="fundraiser"] .ff-topbarGoal__summary',
    'body[data-ff-page="fundraiser"] .ff-sponsorGhost',
    'body[data-ff-page="fundraiser"] .ff-footerMeta',
    'body[data-ff-page="fundraiser"] .ff-heroAccent',
    'body[data-ff-page="fundraiser"] .ff-heroName',
    'body[data-ff-page="fundraiser"] .ff-themeToggle--desktop',
    'body[data-ff-page="fundraiser"] .ff-topbarGoal__progressWrap .ff-help',
]

MOVE_CONTEXTUAL = [
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


def build_authority_block(found: dict[tuple[str, str], Rule]) -> str:
    lines: list[str] = [START]
    lines.append("/* Canonical fundraiser component ownership migrated from ff-above-main-premium.css */")
    lines.append("")

    for selector in MOVE_TOP_LEVEL:
        key = ("", selector)
        rule = found.get(key)
        if not rule:
            continue
        lines.append(f"{selector} {{")
        for row in rule.declarations.splitlines():
            row = row.rstrip()
            if row:
                lines.append(f"  {row.strip()}")
        lines.append("}")
        lines.append("")

    by_context: dict[str, list[Rule]] = defaultdict(list)
    for context, selector in MOVE_CONTEXTUAL:
        rule = found.get((context, selector))
        if rule:
            by_context[context].append(rule)

    for context, rules in by_context.items():
        lines.append(f"{context} {{")
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

    found: dict[tuple[str, str], Rule] = {}
    moved_rules: list[dict] = []
    removals: list[tuple[int, int, str]] = []

    target_keys = {("", s) for s in MOVE_TOP_LEVEL} | {(ctx, s) for ctx, s in MOVE_CONTEXTUAL}

    for rule in rules:
        key = ("\n".join(rule.context), rule.normalized_selector_group)
        if key in target_keys:
            found[key] = rule

    if not found:
        print("== FF CSS AUTHORITY CONSOLIDATION V3 ==")
        print("✔ no eligible canonical fundraiser rules found to migrate")
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

    for key, rule in found.items():
        removals.append(
            (
                rule.start,
                rule.end,
                f"\n/* FF_CSS_AUTHORITY_CONSOLIDATION_V3 moved to ff.css authority block: {rule.normalized_selector_group} */\n",
            )
        )
        moved_rules.append(
            {
                "context": "(top-level)" if not key[0] else key[0].replace("\n", " | "),
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
            "moved_rules": len(moved_rules),
        },
        "moved_rules": moved_rules,
    }

    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md: list[str] = []
    md.append("# FF CSS Authority Consolidation V3")
    md.append("")
    md.append("## Files")
    md.append("")
    for k, v in report["files"].items():
        md.append(f"- **{k}**: `{v}`")
    md.append("")
    md.append("## Moved rules")
    md.append("")
    for item in moved_rules:
        md.append(f"- `{item['selector_group']}`")
        md.append(f"  - Context: `{item['context']}`")
        md.append(f"  - From: `{item['from_file']}:{item['from_line']}`")
        md.append(f"  - To: `{item['to_file']}`")
    md.append("")
    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    print("== FF CSS AUTHORITY CONSOLIDATION V3 ==")
    print(f"ff.css backup      : {rel(ff_bak)}")
    print(f"shim backup        : {rel(above_bak)}")
    print(f"moved rules        : {len(moved_rules)}")
    print(f"json report        : {rel(OUT_JSON)}")
    print(f"md report          : {rel(OUT_MD)}")
    print("\n== MOVED RULES (sample) ==")
    for item in moved_rules[:20]:
        print(f" - {item['selector_group']}")
        print(f"   context: {item['context']}")
        print(f"   from   : {item['from_file']}:{item['from_line']}")
        print(f"   to     : {item['to_file']}")


if __name__ == "__main__":
    main()
