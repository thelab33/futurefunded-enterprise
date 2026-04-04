from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(".").resolve()
CSS = ROOT / "apps/web/app/static/css/ff.css"

if not CSS.exists():
    print(f"❌ missing css: {CSS}")
    raise SystemExit(1)

text = CSS.read_text(encoding="utf-8")
lines = text.splitlines()

def find_real_merge_markers(src_lines: list[str]) -> list[tuple[int, str]]:
    hits = []
    pattern = re.compile(r'^\s*(?:<{7}|={7}|>{7})(?:\s.*)?\s*$')
    for idx, line in enumerate(src_lines, 1):
        if pattern.match(line):
            hits.append((idx, line.rstrip()))
    return hits

def analyze_braces(src: str) -> tuple[list[int], list[int]]:
    open_lines: list[int] = []
    unmatched_close: list[int] = []

    in_comment = False
    in_string: str | None = None
    escape = False
    line = 1
    i = 0
    n = len(src)

    while i < n:
        ch = src[i]
        nxt = src[i + 1] if i + 1 < n else ""

        if in_comment:
            if ch == "*" and nxt == "/":
                in_comment = False
                i += 2
                continue
            if ch == "\n":
                line += 1
            i += 1
            continue

        if in_string is not None:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == in_string:
                in_string = None

            if ch == "\n":
                line += 1
            i += 1
            continue

        if ch == "/" and nxt == "*":
            in_comment = True
            i += 2
            continue

        if ch in ('"', "'"):
            in_string = ch
            i += 1
            continue

        if ch == "{":
            open_lines.append(line)
        elif ch == "}":
            if open_lines:
                open_lines.pop()
            else:
                unmatched_close.append(line)

        if ch == "\n":
            line += 1

        i += 1

    return open_lines, unmatched_close

def print_context(src_lines: list[str], line_no: int, radius: int = 2) -> None:
    start = max(1, line_no - radius)
    end = min(len(src_lines), line_no + radius)
    print(f"\n--- context around line {line_no} ---")
    for i in range(start, end + 1):
        prefix = ">>" if i == line_no else "  "
        print(f"{prefix} {i:>5}: {src_lines[i - 1]}")

merge_hits = find_real_merge_markers(lines)
open_stack, unmatched_close = analyze_braces(text)

checks = [
    ("CSS file exists and is non-empty", len(text.strip()) > 0),
    ("No real merge conflict markers", len(merge_hits) == 0),
    ("Campaign system polish marker present", "FF_CAMPAIGN_SYSTEM_POLISH_V1_START" in text),
    ("Campaign layout composition marker present", "FF_CAMPAIGN_LAYOUT_COMPOSITION_V1_START" in text),
    ("Brace balance looks sane", len(open_stack) == 0 and len(unmatched_close) == 0),
    ("No inline style strings accidentally copied into CSS", 'style="' not in text),
]

failed = [name for name, ok in checks if not ok]

print("== FF CSS GATE LITE V2 ==")
for name, ok in checks:
    print(f"{'✅' if ok else '❌'} {name}")

if merge_hits:
    print("\nREAL MERGE MARKERS FOUND:")
    for line_no, line in merge_hits[:12]:
        print(f" - line {line_no}: {line}")

if unmatched_close:
    print("\nUNMATCHED CLOSING BRACES:")
    for line_no in unmatched_close[:12]:
        print(f" - line {line_no}")
        print_context(lines, line_no)

if open_stack:
    print("\nUNMATCHED OPENING BRACES (most likely missing a closing brace after these):")
    for line_no in open_stack[-12:]:
        print(f" - line {line_no}")
        print_context(lines, line_no)

if failed:
    print("\nFAILED:")
    for name in failed:
        print(f" - {name}")
    raise SystemExit(1)

print("\nPASS")
