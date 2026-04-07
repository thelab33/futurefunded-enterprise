from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path.home() / "futurefunded-enterprise"

ROUTES = ROOT / "apps/web/app/routes/platform.py"
CSS = ROOT / "apps/web/app/static/css/platform-pages.css"

FILES = [
    ("apps/web/app/templates/platform/pages/home.html", "TRACE_PLATFORM_PAGES_HOME", "canonical"),
    ("apps/web/app/templates/platform/home.html", "TRACE_PLATFORM_HOME_LEGACY", "legacy"),

    ("apps/web/app/templates/platform/pages/pricing.html", "TRACE_PLATFORM_PAGES_PRICING", "canonical"),
    ("apps/web/app/templates/platform/pricing.html", "TRACE_PLATFORM_PRICING_LEGACY", "legacy"),

    ("apps/web/app/templates/platform/pages/demo.html", "TRACE_PLATFORM_PAGES_DEMO", "canonical"),
    ("apps/web/app/templates/platform/demo.html", "TRACE_PLATFORM_DEMO_LEGACY", "legacy"),

    ("apps/web/app/templates/platform/pages/dashboard.html", "TRACE_PLATFORM_PAGES_DASHBOARD", "canonical"),
    ("apps/web/app/templates/platform/dashboard.html", "TRACE_PLATFORM_DASHBOARD_LEGACY", "legacy"),

    ("apps/web/app/templates/platform/pages/onboarding.html", "TRACE_PLATFORM_PAGES_ONBOARDING", "canonical"),
    ("apps/web/app/templates/platform/onboarding.html", "TRACE_PLATFORM_ONBOARDING_LEGACY", "legacy"),

    ("apps/web/app/templates/campaign/index.html", "TRACE_CAMPAIGN_INDEX", "campaign"),
]

FOUNDERS_INCLUDE = '{% include "platform/partials/_founder_demo_flow_strip.html" %}'
DASH_INCLUDE = '{% include "platform/partials/_dashboard_operator_premium_strip.html" %}'
FOUNDERS_MARKER = "FF_PLATFORM_FOUNDER_DEMO_FLOW_V1"
DASH_MARKER = "FF_PLATFORM_DASHBOARD_OPERATOR_PREMIUM_V1"

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def grep1(pattern: str, text: str):
    m = re.search(pattern, text, re.S | re.M)
    return m.group(0) if m else None

def first_line_matching(text: str, needle: str):
    for i, line in enumerate(text.splitlines(), 1):
        if needle in line:
            return i, line.strip()
    return None, None

routes_text = read_text(ROUTES)
css_text = read_text(CSS)

print("== FF PLATFORM SURFACE CANONICALITY AUDIT ==")
print()

print("[route bindings]")
if ROUTES.exists():
    for needle in [
        'template_name="platform/pages/home.html"',
        'template_name="platform/pages/pricing.html"',
        'template_name="platform/pages/demo.html"',
        'template_name="platform/pages/dashboard.html"',
        'template_name="platform/pages/onboarding.html"',
        'template_name="platform/home.html"',
        'template_name="platform/pricing.html"',
        'template_name="platform/demo.html"',
        'template_name="platform/dashboard.html"',
        'template_name="platform/onboarding.html"',
    ]:
        count = routes_text.count(needle)
        if count:
            print(f"  {needle} -> {count}")
else:
    print(f"  missing routes file: {ROUTES}")

print()
print("[css markers]")
print(f"  {FOUNDERS_MARKER}: {css_text.count(FOUNDERS_MARKER)}")
print(f"  {DASH_MARKER}: {css_text.count(DASH_MARKER)}")

print()
print("[template files]")
for rel, trace, family in FILES:
    path = ROOT / rel
    text = read_text(path)

    exists = path.exists()
    founder_count = text.count(FOUNDERS_INCLUDE)
    dash_count = text.count(DASH_INCLUDE)
    trace_line_no, trace_line = first_line_matching(text, trace)

    extends_line = None
    include_lines = []
    if exists:
        for i, line in enumerate(text.splitlines(), 1):
            s = line.strip()
            if s.startswith("{% extends "):
                extends_line = (i, s)
            if "_founder_demo_flow_strip.html" in s or "_dashboard_operator_premium_strip.html" in s:
                include_lines.append((i, s))

    print(f"- {rel}")
    print(f"    family: {family}")
    print(f"    exists: {exists}")
    print(f"    trace_present: {bool(trace_line_no)}")
    if trace_line_no:
        print(f"    trace_line: {trace_line_no}: {trace_line}")
    else:
        print(f"    trace_line: MISSING ({trace})")

    if extends_line:
        print(f"    extends: {extends_line[0]}: {extends_line[1]}")
    else:
        print("    extends: none")

    print(f"    founder_include_count: {founder_count}")
    print(f"    dashboard_include_count: {dash_count}")

    if include_lines:
        for ln, content in include_lines:
            print(f"    include_line: {ln}: {content}")
    else:
        print("    include_line: none")

print()
print("[summary flags]")

def route_bound(template_name: str) -> bool:
    return f'template_name="{template_name}"' in routes_text

canonical_expected = {
    "platform/pages/home.html": route_bound("platform/pages/home.html"),
    "platform/pages/pricing.html": route_bound("platform/pages/pricing.html"),
    "platform/pages/demo.html": route_bound("platform/pages/demo.html"),
    "platform/pages/dashboard.html": route_bound("platform/pages/dashboard.html"),
    "platform/pages/onboarding.html": route_bound("platform/pages/onboarding.html"),
}

legacy_expected = {
    "platform/home.html": route_bound("platform/home.html"),
    "platform/pricing.html": route_bound("platform/pricing.html"),
    "platform/demo.html": route_bound("platform/demo.html"),
    "platform/dashboard.html": route_bound("platform/dashboard.html"),
    "platform/onboarding.html": route_bound("platform/onboarding.html"),
}

for key, val in canonical_expected.items():
    print(f"  canonical_route_bound[{key}] = {val}")

for key, val in legacy_expected.items():
    print(f"  legacy_route_bound[{key}] = {val}")

print()
print("RESULT GUIDE:")
print("  - If canonical_route_bound is True and legacy_route_bound is False, patch only pages/*")
print("  - If both are True, audit both carefully before any combined patch")
print("  - If founder/dashboard include counts are >1 in any live-bound file, duplication exists")
