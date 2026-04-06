#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import json
import re

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "apps/web/app/templates/campaign/index.html"
CSS_FILES = [
    ROOT / "apps/web/app/static/css/ff.css",
    ROOT / "apps/web/app/static/css/ff-above-main-premium.css",
]
SCRIPT_ID = "ffSelectors"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def print_header(title: str) -> None:
    print(f"\n== {title} ==")


def find_script_payload(html: str) -> str | None:
    match = re.search(
        r'<script[^>]*id=["\']ffSelectors["\'][^>]*>([\s\S]*?)</script>',
        html,
        re.IGNORECASE,
    )
    return match.group(1).strip() if match else None


def parse_ffselectors(payload: str | None) -> tuple[dict[str, str], str | None]:
    if not payload:
        return {}, f'Missing <script id="{SCRIPT_ID}"> payload'

    try:
        parsed = json.loads(payload)
    except Exception as exc:
        return {}, f"Could not parse {SCRIPT_ID} JSON: {exc}"

    if not isinstance(parsed, dict):
        return {}, f"{SCRIPT_ID} payload is not a JSON object"

    normalized: dict[str, str] = {}
    for key, value in parsed.items():
        if isinstance(key, str) and isinstance(value, str):
            normalized[key] = value

    return normalized, None


def duplicate_values(values: list[str]) -> list[tuple[str, int]]:
    counts = Counter(values)
    return sorted(
        [(k, v) for k, v in counts.items() if v > 1],
        key=lambda x: (-x[1], x[0]),
    )


def missing_targets(refs: list[str], available_ids: set[str]) -> list[str]:
    return sorted([ref for ref in refs if ref not in available_ids])


def selector_parts(selector: str) -> list[str]:
    return [part.strip() for part in selector.split(",") if part.strip()]


def main() -> int:
    if not TEMPLATE.exists():
        print(f"❌ Missing template: {TEMPLATE}")
        return 1

    html = read_text(TEMPLATE)
    css_blob = "\n".join(read_text(path) for path in CSS_FILES if path.exists())

    ids = re.findall(r'id=["\']([^"\']+)["\']', html)

    class_values = re.findall(r'class=["\']([^"\']+)["\']', html)
    classes: list[str] = []
    for raw in class_values:
        classes.extend(raw.split())

    data_ff_hooks = re.findall(r'(data-ff-[a-zA-Z0-9_-]+)', html)
    aria_controls_refs = re.findall(r'aria-controls=["\']([^"\']+)["\']', html)
    href_hash_refs = [
        h for h in re.findall(r'href=["\']#([^"\']+)["\']', html)
        if h and not h.startswith("{")
    ]

    ffselectors_payload = find_script_payload(html)
    ffselectors_map, ffselectors_error = parse_ffselectors(ffselectors_payload)

    if ffselectors_error:
        print(f"❌ {ffselectors_error}")

    print("== FF SELECTOR CONTRACT AUDIT ==")
    print(f"Template: {TEMPLATE.relative_to(ROOT)}")
    print(f"IDs: {len(ids)}")
    print(f"Classes: {len(classes)}")
    print(f"Unique classes: {len(set(classes))}")
    print(f"data-ff hooks: {len(data_ff_hooks)}")
    print(f"Unique data-ff hooks: {len(set(data_ff_hooks))}")
    print(f"aria-controls refs: {len(aria_controls_refs)}")
    print(f"href hash refs: {len(href_hash_refs)}")
    print(f"ffSelectors hooks: {len(ffselectors_map)}")

    print_header("DUPLICATE IDS")
    dup_ids = duplicate_values(ids)
    if dup_ids:
        for value, count in dup_ids:
            print(f"{value}: {count}")
    else:
        print("✅ none")

    print_header("MISSING aria-controls TARGETS")
    missing_aria = missing_targets(aria_controls_refs, set(ids))
    if missing_aria:
        for value in missing_aria:
            print(value)
    else:
        print("✅ none")

    print_header('MISSING href="#..." TARGETS')
    missing_hash = missing_targets(href_hash_refs, set(ids))
    if missing_hash:
        for value in missing_hash:
            print(value)
    else:
        print("✅ none")

    print_header("ffSelectors HOOKS")
    if ffselectors_map:
        for key, selector in sorted(ffselectors_map.items()):
            print(f"{key}: {selector}")
    else:
        print("⚠️ none detected")

    print_header("ffSelectors PRESENCE IN HTML")
    if ffselectors_map:
        for key, selector in sorted(ffselectors_map.items()):
            parts = selector_parts(selector)
            statuses = []
            for part in parts:
                statuses.append(f"{part} => {'✅' if part in html else '❌'}")
            print(f"{key}: " + " | ".join(statuses))
    else:
        print("⚠️ skipped — no parsed ffSelectors hooks")

    print_header("ffSelectors PRESENCE IN CSS")
    if ffselectors_map:
        for key, selector in sorted(ffselectors_map.items()):
            parts = selector_parts(selector)
            statuses = []
            for part in parts:
                statuses.append(f"{part} => {'✅' if part in css_blob else '❌'}")
            print(f"{key}: " + " | ".join(statuses))
    else:
        print("⚠️ skipped — no parsed ffSelectors hooks")

    print_header("TOP data-ff HOOKS")
    for hook, count in Counter(data_ff_hooks).most_common(40):
        print(f"{hook}: {count}")

    print_header("TOP CLASSES")
    for class_name, count in Counter(classes).most_common(50):
        print(f"{class_name}: {count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
