from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json
import re

ROOT = Path.home() / "futurefunded-enterprise"
ABOVE_CSS = ROOT / "apps/web/app/static/css/ff-above-main-premium.css"
OUT_JSON = ROOT / "tools/audit/ff_css_authority_consolidation_v2.json"
OUT_MD = ROOT / "tools/audit/ff_css_authority_consolidation_v2.md"

COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)


@dataclass
class Rule:
    file: Path
    context: tuple[str, ...]
    selector_group: str
    declarations: str
    normalized_selector_group: str
    start: int
    end: int
    open_brace: int
    close_brace: int
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


def parse_css_rules(path: Path) -> list[Rule]:
    original = path.read_text(encoding="utf-8")
    masked = mask_comments(original)
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

            block_body = original[open_idx + 1:close_idx]
            line = line_number(original, i)

            if prelude.startswith(recursive_context_headers):
                walk(open_idx + 1, close_idx, context + (prelude,))
            elif prelude.startswith(skip_at_headers):
                pass
            elif prelude.startswith("@"):
                pass
            else:
                rules.append(
                    Rule(
                        file=path,
                        context=context,
                        selector_group=prelude,
                        declarations=block_body,
                        normalized_selector_group=normalize_selector_group(prelude),
                        start=i,
                        end=close_idx + 1,
                        open_brace=open_idx,
                        close_brace=close_idx,
                        line=line,
                    )
                )

            i = close_idx + 1

    walk(0, len(masked), tuple())
    return rules


def context_key(rule: Rule) -> str:
    return " | ".join(rule.context) if rule.context else "(top-level)"


def line_indent(text: str, offset: int) -> str:
    line_start = text.rfind("\n", 0, offset) + 1
    indent = []
    i = line_start
    while i < len(text) and text[i] in (" ", "\t"):
        indent.append(text[i])
        i += 1
    return "".join(indent)


def split_declarations(text: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    depth_round = 0
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

        if ch == ";" and depth_round == 0:
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


def parse_declaration_block(text: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for raw in split_declarations(COMMENT_RE.sub("", text)):
        if ":" not in raw:
            continue
        prop, value = raw.split(":", 1)
        prop = prop.strip()
        value = value.strip()
        if not prop or not value:
            continue
        pairs.append((prop, value))
    return pairs


def merge_declarations(rules: list[Rule]) -> str:
    ordered_props: list[str] = []
    values: dict[str, str] = {}

    for rule in sorted(rules, key=lambda r: r.start):
        for prop, value in parse_declaration_block(rule.declarations):
            if prop in ordered_props:
                ordered_props.remove(prop)
            ordered_props.append(prop)
            values[prop] = value

    lines = [f"  {prop}: {values[prop]};" for prop in ordered_props]
    return "\n".join(lines)


def main() -> None:
    if not ABOVE_CSS.exists():
        raise SystemExit(f"❌ Missing file: {ABOVE_CSS}")

    original = ABOVE_CSS.read_text(encoding="utf-8")
    rules = parse_css_rules(ABOVE_CSS)

    groups: dict[tuple[str, str], list[Rule]] = defaultdict(list)
    for rule in rules:
        groups[("\n".join(rule.context), rule.normalized_selector_group)].append(rule)

    collision_groups: list[tuple[tuple[str, str], list[Rule]]] = []
    for key, bucket in groups.items():
        if len(bucket) > 1:
            collision_groups.append((key, sorted(bucket, key=lambda r: r.start)))

    if not collision_groups:
        print("== FF CSS AUTHORITY CONSOLIDATION V2 ==")
        print("✔ no same-selector collisions found inside ff-above-main-premium.css")
        return

    ops: list[tuple[int, int, str]] = []
    merged_report: list[dict] = []

    for (_ctx, selector_group), bucket in collision_groups:
        keep_rule = bucket[-1]
        earlier = bucket[:-1]
        merged_decl = merge_declarations(bucket)
        indent = line_indent(original, keep_rule.start)
        rebuilt = f"{indent}{keep_rule.normalized_selector_group} {{\n{merged_decl}\n{indent}}}"

        # replace last rule with merged canonical rule
        ops.append((keep_rule.start, keep_rule.end, rebuilt))

        # comment out earlier rules
        for rule in earlier:
            note = (
                f"\n/* FF_CSS_AUTHORITY_CONSOLIDATION_V2 merged into later canonical rule: "
                f"{keep_rule.normalized_selector_group} */\n"
            )
            ops.append((rule.start, rule.end, note))

        merged_report.append(
            {
                "context": "(top-level)" if not _ctx else _ctx.replace("\n", " | "),
                "selector_group": selector_group,
                "kept": {
                    "file": rel(keep_rule.file),
                    "line": keep_rule.line,
                },
                "merged_from": [
                    {"file": rel(rule.file), "line": rule.line} for rule in bucket
                ],
            }
        )

    bak = backup(ABOVE_CSS)
    updated = original
    for start, end, replacement in sorted(ops, key=lambda x: x[0], reverse=True):
        updated = updated[:start] + replacement + updated[end:]

    ABOVE_CSS.write_text(updated, encoding="utf-8")

    report = {
        "target": rel(ABOVE_CSS),
        "backup": rel(bak),
        "counts": {
            "rules_scanned": len(rules),
            "collision_groups_merged": len(merged_report),
        },
        "merged_groups": merged_report,
    }

    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md: list[str] = []
    md.append("# FF CSS Authority Consolidation V2")
    md.append("")
    md.append(f"**Target:** `{rel(ABOVE_CSS)}`")
    md.append(f"**Backup:** `{rel(bak)}`")
    md.append("")
    md.append("## Summary")
    md.append("")
    for k, v in report["counts"].items():
        md.append(f"- **{k}**: {v}")
    md.append("")
    md.append("## Merged groups")
    md.append("")
    for item in merged_report:
        md.append(f"- **Selector group:** `{item['selector_group']}`")
        md.append(f"  - Context: `{item['context']}`")
        md.append(f"  - Kept: `{item['kept']['file']}:{item['kept']['line']}`")
        for src in item["merged_from"]:
            md.append(f"  - Source: `{src['file']}:{src['line']}`")
    md.append("")
    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    print("== FF CSS AUTHORITY CONSOLIDATION V2 ==")
    print(f"target file     : {rel(ABOVE_CSS)}")
    print(f"backup          : {rel(bak)}")
    print(f"rules scanned   : {report['counts']['rules_scanned']}")
    print(f"groups merged   : {report['counts']['collision_groups_merged']}")
    print(f"json report     : {rel(OUT_JSON)}")
    print(f"md report       : {rel(OUT_MD)}")

    print("\n== MERGED GROUPS (sample) ==")
    for item in merged_report[:20]:
        print(f" - {item['selector_group']}")
        print(f"   context: {item['context']}")
        print(f"   kept   : {item['kept']['file']}:{item['kept']['line']}")
        for src in item['merged_from'][:6]:
            print(f"   source : {src['file']}:{src['line']}")


if __name__ == "__main__":
    main()
