from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import hashlib
import json
import re

ROOT = Path.home() / "futurefunded-enterprise"

FF_CSS = ROOT / "apps/web/app/static/css/ff.css"
ABOVE_CSS = ROOT / "apps/web/app/static/css/ff-above-main-premium.css"
PLATFORM_CSS = ROOT / "apps/web/app/static/css/platform-pages.css"

TARGETS = [p for p in [FF_CSS, ABOVE_CSS, PLATFORM_CSS] if p.exists()]

OUT_JSON = ROOT / "tools/audit/ff_css_authority_consolidation_v1.json"
OUT_MD = ROOT / "tools/audit/ff_css_authority_consolidation_v1.md"

COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)


@dataclass
class Rule:
    file: Path
    context: tuple[str, ...]
    selector_group: str
    declarations: str
    normalized_selector_group: str
    normalized_declarations: str
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
    parts = split_selector_group(text)
    return ", ".join(parts)


def normalize_declarations(text: str) -> str:
    s = COMMENT_RE.sub("", text)
    s = normalize_spaces(s)
    s = re.sub(r"\s*([:;,{}>+~])\s*", r"\1", s)
    s = s.strip().rstrip(";")
    return s


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
            if i >= end:
                return
            if masked[i] == "}":
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
                        normalized_declarations=normalize_declarations(block_body),
                        start=i,
                        end=close_idx + 1,
                        line=line,
                    )
                )

            i = close_idx + 1

    walk(0, len(masked), tuple())
    return rules


def owner_for_rule(rule: Rule) -> Path:
    haystack = " ".join(rule.context) + " " + rule.normalized_selector_group

    if 'body[data-ff-template="platform"]' in haystack:
        return PLATFORM_CSS if PLATFORM_CSS.exists() else FF_CSS

    if 'body[data-ff-page="fundraiser"]' in haystack:
        return ABOVE_CSS if ABOVE_CSS.exists() else FF_CSS

    return FF_CSS


def context_key(rule: Rule) -> str:
    return " | ".join(rule.context) if rule.context else "(top-level)"


def hash_rule(rule: Rule) -> str:
    raw = "\n".join(
        [
            "\n".join(rule.context),
            rule.normalized_selector_group,
            rule.normalized_declarations,
        ]
    ).encode("utf-8")
    return hashlib.sha1(raw).hexdigest()


def main() -> None:
    missing = [str(p) for p in [FF_CSS, ABOVE_CSS, PLATFORM_CSS] if not p.exists()]
    if missing:
        print("⚠ missing css files:")
        for m in missing:
            print(f" - {m}")

    if not TARGETS:
        raise SystemExit("❌ No target CSS files found")

    all_rules: list[Rule] = []
    rules_by_file: dict[Path, list[Rule]] = {}

    for path in TARGETS:
        parsed = parse_css_rules(path)
        rules_by_file[path] = parsed
        all_rules.extend(parsed)

    exact_groups: dict[tuple[str, str, str], list[Rule]] = defaultdict(list)
    selector_groups: dict[tuple[str, str], list[Rule]] = defaultdict(list)

    for rule in all_rules:
        key_exact = (
            "\n".join(rule.context),
            rule.normalized_selector_group,
            rule.normalized_declarations,
        )
        exact_groups[key_exact].append(rule)

        key_selector = (
            "\n".join(rule.context),
            rule.normalized_selector_group,
        )
        selector_groups[key_selector].append(rule)

    removals: dict[Path, list[tuple[int, int, str]]] = defaultdict(list)
    kept: dict[str, dict] = {}
    exact_duplicate_report: list[dict] = []
    collisions_report: list[dict] = []

    # Pass 1: remove only EXACT duplicate rules
    for (_ctx, selector_group, _decls), rules in exact_groups.items():
        if len(rules) < 2:
            continue

        owner = owner_for_rule(rules[0])
        owner_candidates = [r for r in rules if r.file == owner]
        keep_rule = owner_candidates[0] if owner_candidates else rules[0]

        keep_hash = hash_rule(keep_rule)
        kept[keep_hash] = {
            "owner_file": rel(keep_rule.file),
            "line": keep_rule.line,
            "context": context_key(keep_rule),
            "selector_group": keep_rule.normalized_selector_group,
        }

        removed_items = []

        for rule in rules:
            same_as_keep = (
                rule.file == keep_rule.file
                and rule.start == keep_rule.start
                and rule.end == keep_rule.end
            )
            if same_as_keep:
                continue

            removals[rule.file].append(
                (
                    rule.start,
                    rule.end,
                    f"FF_CSS_AUTHORITY_CONSOLIDATION_V1 removed exact duplicate of {keep_rule.normalized_selector_group}",
                )
            )
            removed_items.append(
                {
                    "file": rel(rule.file),
                    "line": rule.line,
                }
            )

        if removed_items:
            exact_duplicate_report.append(
                {
                    "context": context_key(rules[0]),
                    "selector_group": selector_group,
                    "owner_file": rel(keep_rule.file),
                    "owner_line": keep_rule.line,
                    "removed": removed_items,
                }
            )

    # Pass 2: same selector group but different declarations => report only
    for (_ctx, selector_group), rules in selector_groups.items():
        if len(rules) < 2:
            continue

        declaration_variants: dict[str, list[Rule]] = defaultdict(list)
        for rule in rules:
            declaration_variants[rule.normalized_declarations].append(rule)

        if len(declaration_variants) <= 1:
            continue

        collisions_report.append(
            {
                "context": context_key(rules[0]),
                "selector_group": selector_group,
                "variants": [
                    {
                        "declaration_hash": hashlib.sha1(decl.encode("utf-8")).hexdigest()[:12],
                        "occurrences": [
                            {
                                "file": rel(rule.file),
                                "line": rule.line,
                            }
                            for rule in variant_rules
                        ],
                    }
                    for decl, variant_rules in declaration_variants.items()
                ],
            }
        )

    touched_files: list[str] = []
    backups: dict[str, str] = {}

    for path, spans in removals.items():
        if not spans:
            continue

        original = path.read_text(encoding="utf-8")
        updated = original

        spans = sorted(spans, key=lambda x: x[0], reverse=True)

        bak = backup(path)
        backups[rel(path)] = rel(bak)

        for start, end, note in spans:
            updated = updated[:start] + f"\n/* {note} */\n" + updated[end:]

        path.write_text(updated, encoding="utf-8")
        touched_files.append(rel(path))

    report = {
        "targets": [rel(p) for p in TARGETS],
        "touched_files": touched_files,
        "backups": backups,
        "counts": {
            "files_scanned": len(TARGETS),
            "rules_scanned": len(all_rules),
            "exact_duplicate_groups_removed": len(exact_duplicate_report),
            "same_selector_collisions_reported": len(collisions_report),
            "files_touched": len(touched_files),
        },
        "exact_duplicates_removed": exact_duplicate_report,
        "same_selector_collisions": collisions_report,
    }

    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md: list[str] = []
    md.append("# FF CSS Authority Consolidation V1")
    md.append("")
    md.append("## Summary")
    md.append("")
    for k, v in report["counts"].items():
        md.append(f"- **{k}**: {v}")
    md.append("")
    md.append("## Files touched")
    md.append("")
    for p in touched_files:
        md.append(f"- `{p}`")
    md.append("")
    md.append("## Backups")
    md.append("")
    for src, bak in backups.items():
        md.append(f"- `{src}` -> `{bak}`")
    md.append("")
    md.append("## Exact duplicate groups removed")
    md.append("")
    for item in exact_duplicate_report[:200]:
        md.append(f"- **Selector group:** `{item['selector_group']}`")
        md.append(f"  - Context: `{item['context']}`")
        md.append(f"  - Owner: `{item['owner_file']}:{item['owner_line']}`")
        for removed in item["removed"]:
            md.append(f"  - Removed: `{removed['file']}:{removed['line']}`")
    md.append("")
    md.append("## Same selector collisions (manual review)")
    md.append("")
    for item in collisions_report[:200]:
        md.append(f"- **Selector group:** `{item['selector_group']}`")
        md.append(f"  - Context: `{item['context']}`")
        for variant in item["variants"]:
            md.append(f"  - Variant `{variant['declaration_hash']}`")
            for occ in variant["occurrences"]:
                md.append(f"    - `{occ['file']}:{occ['line']}`")
    md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    print("== FF CSS AUTHORITY CONSOLIDATION V1 ==")
    print(f"files scanned   : {report['counts']['files_scanned']}")
    print(f"rules scanned   : {report['counts']['rules_scanned']}")
    print(f"exact removed   : {report['counts']['exact_duplicate_groups_removed']}")
    print(f"collisions found: {report['counts']['same_selector_collisions_reported']}")
    print(f"files touched   : {report['counts']['files_touched']}")
    print(f"json report     : {rel(OUT_JSON)}")
    print(f"md report       : {rel(OUT_MD)}")

    if touched_files:
        print("\n== TOUCHED FILES ==")
        for p in touched_files:
            print(f" - {p}")

    if exact_duplicate_report:
        print("\n== EXACT DUPLICATE GROUPS REMOVED (sample) ==")
        for item in exact_duplicate_report[:20]:
            print(f" - {item['selector_group']}")
            print(f"   owner: {item['owner_file']}:{item['owner_line']}")
            for removed in item['removed'][:5]:
                print(f"   removed: {removed['file']}:{removed['line']}")

    if collisions_report:
        print("\n== SAME SELECTOR COLLISIONS (sample) ==")
        for item in collisions_report[:20]:
            print(f" - {item['selector_group']}")
            print(f"   context: {item['context']}")
            for variant in item['variants'][:4]:
                locs = ", ".join(
                    f"{o['file']}:{o['line']}" for o in variant['occurrences'][:4]
                )
                print(f"   variant {variant['declaration_hash']}: {locs}")


if __name__ == "__main__":
    main()
