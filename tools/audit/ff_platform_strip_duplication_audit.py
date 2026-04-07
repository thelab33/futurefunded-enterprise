from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path.home() / "futurefunded-enterprise"

CSS = ROOT / "apps/web/app/static/css/platform-pages.css"

FILES = {
    "home": ROOT / "apps/web/app/templates/platform/pages/home.html",
    "demo": ROOT / "apps/web/app/templates/platform/pages/demo.html",
    "pricing": ROOT / "apps/web/app/templates/platform/pages/pricing.html",
    "onboarding": ROOT / "apps/web/app/templates/platform/pages/onboarding.html",
    "dashboard": ROOT / "apps/web/app/templates/platform/pages/dashboard.html",
}

PARTIALS = {
    "founder_flow": ROOT / "apps/web/app/templates/platform/partials/_founder_demo_flow_strip.html",
    "dashboard_operator": ROOT / "apps/web/app/templates/platform/partials/_dashboard_operator_premium_strip.html",
}

CHECKS = {
    "founder_flow": {
        "css_marker": "FF_PLATFORM_FOUNDER_DEMO_FLOW_V1",
        "include": '{% include "platform/partials/_founder_demo_flow_strip.html" %}',
        "expected_pages": ["home", "demo", "pricing", "onboarding"],
        "partial_classes": [
            "ff-founderFlow",
            "ff-founderFlow__inner",
            "ff-founderFlow__steps",
            "ff-founderFlow__close",
        ],
    },
    "dashboard_operator": {
        "css_marker": "FF_PLATFORM_DASHBOARD_OPERATOR_PREMIUM_V1",
        "include": '{% include "platform/partials/_dashboard_operator_premium_strip.html" %}',
        "expected_pages": ["dashboard"],
        "partial_classes": [
            "ff-operatorPremium",
            "ff-operatorPremium__inner",
            "ff-operatorPremium__grid",
            "ff-operatorPremium__rail",
        ],
    },
}

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def count_literal(text: str, needle: str) -> int:
    return text.count(needle)

def count_class_tokens(text: str, class_name: str) -> int:
    pattern = re.compile(r'(?<![A-Za-z0-9_-])' + re.escape(class_name) + r'(?![A-Za-z0-9_-])')
    return len(pattern.findall(text))

def status(ok: bool) -> str:
    return "OK" if ok else "MISS"

css_text = read_text(CSS)

print("== FF PLATFORM STRIP DUPLICATION AUDIT ==")
print()

overall_fail = False

for key, cfg in CHECKS.items():
    print(f"[{key}]")
    partial_path = PARTIALS[key]
    partial_text = read_text(partial_path)

    partial_exists = partial_path.exists()
    css_marker_count = count_literal(css_text, cfg["css_marker"])
    include_total = 0

    print(f"  partial: {partial_path}")
    print(f"  partial_exists: {status(partial_exists)}")

    print(f"  css_marker: {cfg['css_marker']}")
    print(f"  css_marker_count: {css_marker_count}")

    if css_marker_count == 0:
        overall_fail = True
        print("  -> missing CSS block")
    elif css_marker_count > 1:
        overall_fail = True
        print("  -> DUPLICATE CSS marker found")

    if partial_exists:
        for cls in cfg["partial_classes"]:
            n = count_class_tokens(partial_text, cls)
            print(f"  partial_class {cls}: {n}")
            if n == 0:
                overall_fail = True
                print(f"  -> missing expected class in partial: {cls}")

    for page_name in cfg["expected_pages"]:
        page_path = FILES[page_name]
        page_text = read_text(page_path)
        include_count = count_literal(page_text, cfg["include"])
        include_total += include_count
        print(f"  include_count[{page_name}]: {include_count}")

        if include_count == 0:
            overall_fail = True
            print(f"  -> missing include in {page_name}")
        elif include_count > 1:
            overall_fail = True
            print(f"  -> DUPLICATE include in {page_name}")

    print(f"  include_total_expected_pages: {include_total}")
    expected_total = len(cfg["expected_pages"])
    if include_total != expected_total:
        overall_fail = True
        print(f"  -> expected total include count {expected_total}, got {include_total}")

    print()

print("[cross-check]")
for page_name, path in FILES.items():
    text = read_text(path)
    ff_count = text.count("ff-founderFlow")
    op_count = text.count("ff-operatorPremium")
    print(f"  {page_name}: ff-founderFlow={ff_count} ff-operatorPremium={op_count}")

print()
print("== SUMMARY ==")
if overall_fail:
    print("RESULT: REVIEW NEEDED")
    sys.exit(1)
else:
    print("RESULT: CLEAN")
