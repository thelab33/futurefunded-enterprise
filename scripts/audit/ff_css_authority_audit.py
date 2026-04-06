from __future__ import annotations

from pathlib import Path
from collections import Counter
import re

CSS = Path("apps/web/app/static/css/ff.css")
SHIM = Path("apps/web/app/static/css/ff-above-main-premium.css")

if not CSS.exists():
    raise SystemExit(f"❌ Missing CSS authority file: {CSS}")

css = CSS.read_text(encoding="utf-8", errors="replace")
shim = SHIM.read_text(encoding="utf-8", errors="replace") if SHIM.exists() else ""
css_no_comments = re.sub(r"/\*.*?\*/", "", css, flags=re.S)

high_risk = [
    ".ff-checkoutShell",
    ".ff-backtotop",
    ".ff-onboardStepper",
    ".ff-sponsorModal__head",
    ".ff-videoModal__head",
    "#checkout .ff-checkoutShell",
    "[data-ff-backtotop]",
]

print("== FF CSS AUTHORITY AUDIT ==")
print(f"Authority file: {CSS}")
print(f"Shim file: {SHIM if SHIM else 'missing'}")
print()

print("== FILE SIZE ==")
print(f"ff.css bytes: {len(css)}")
if shim:
    print(f"ff-above-main-premium.css bytes: {len(shim)}")
print()

print("== BALANCE ==")
print("Braces:", "✅" if css.count("{") == css.count("}") else "❌", css.count("{"), css.count("}"))
print("Parens :", "✅" if css.count("(") == css.count(")") else "❌", css.count("("), css.count(")"))
print()

print("== !important COUNT ==")
important_count = css.count("!important")
print(f"!important: {important_count}")
print()

print("== DUPLICATE KEYFRAMES ==")
keyframes = re.findall(r'@keyframes\s+([a-zA-Z0-9_-]+)', css)
dupe_keyframes = [k for k, v in Counter(keyframes).items() if v > 1]
if dupe_keyframes:
    for k in dupe_keyframes:
        print("❌", k, Counter(keyframes)[k])
else:
    print("✅ none")
print()

print("== HIGH-RISK SELECTOR COUNTS ==")
for sel in high_risk:
    count = css_no_comments.count(sel)
    print(f"{sel}: {count}")
print()

print("== SHIM CONTENT ==")
if not shim:
    print("ℹ️ shim file missing")
else:
    if "residual bridge only" in (Path(__file__).resolve().parents[2] / "apps/web/app/static/css/ff-above-main-premium.css").read_text(encoding="utf-8").lower():
        print("✅ shim labeled residual bridge only")
    else:
        print("⚠️ shim not labeled residual bridge only")

    onboarding_needles = [
        "#ff-onboarding",
        "#ffOnboardPanel2",
        "[data-ff-open-onboarding]",
    ]
    for needle in onboarding_needles:
        print(f"{needle}: {'✅' if needle in shim else '❌'}")
print()

print("== WAVE / POLISH MARKERS ==")
markers = [
    "FF_WAVE1_AUTHORITY_CONSOLIDATION_V1",
    "FF_WAVE2_AUTHORITY_CONSOLIDATION_V1",
    "FF_WAVE3_AUTHORITY_CONSOLIDATION_V1",
    "FF_LAUNCH_POLISH_V1_START",
    "FF_LAUNCH_POLISH_V1_END",
]
for m in markers:
    print(f"{m}: {'✅' if m in css else '❌'}")
