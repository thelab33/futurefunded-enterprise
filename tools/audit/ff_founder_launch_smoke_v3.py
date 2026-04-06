from __future__ import annotations

from pathlib import Path

ROOT = Path.home() / "futurefunded-enterprise"
TROOT = ROOT / "apps/web/app/templates"
CAMPAIGN = TROOT / "campaign" / "index.html"
JS = ROOT / "apps/web/app/static/js" / "ff-app.js"

TARGETS = {
    "home": [
        TROOT / "platform" / "home.html",
        TROOT / "platform" / "pages" / "home.html",
    ],
    "onboarding": [
        TROOT / "platform" / "onboarding.html",
        TROOT / "platform" / "pages" / "onboarding.html",
    ],
    "dashboard": [
        TROOT / "platform" / "dashboard.html",
        TROOT / "platform" / "pages" / "dashboard.html",
    ],
    "pricing": [
        TROOT / "platform" / "pricing.html",
        TROOT / "platform" / "pages" / "pricing.html",
    ],
    "demo": [
        TROOT / "platform" / "demo.html",
        TROOT / "platform" / "pages" / "demo.html",
    ],
}

REQUIRED_CAMPAIGN_HOOKS = [
    "data-ff-open-checkout",
    "data-ff-close-checkout",
    "data-ff-sponsor-modal",
    "data-ff-share",
    "data-ff-checkout-sheet",
    "Support completed",
    "Become a sponsor",
    "Donate",
]

REQUIRED_JS_STRINGS = [
    "openCheckout",
    "closeCheckout",
    "checkoutSheet",
    "share",
]

def existing_paths(paths: list[Path]) -> list[Path]:
    return [p for p in paths if p.exists()]

def ok(label: str, passed: bool, detail: str = "") -> bool:
    icon = "✅" if passed else "❌"
    print(f"{icon} {label}" + (f" — {detail}" if detail else ""))
    return passed

def group_text(paths: list[Path]) -> str:
    buf = []
    for path in paths:
        if path.exists():
            buf.append(path.read_text(encoding="utf-8"))
    return "\n".join(buf)

status = True
print("== FOUNDER LAUNCH SMOKE V3 ==")

for name, candidates in TARGETS.items():
    paths = existing_paths(candidates)
    if paths:
        for path in paths:
            status &= ok(f"{name} template exists", path.exists(), str(path))
    else:
        print(f"⚠ {name} template missing — skipped")

status &= ok("campaign template exists", CAMPAIGN.exists(), str(CAMPAIGN))
status &= ok("ff-app.js exists", JS.exists(), str(JS))

if CAMPAIGN.exists():
    campaign = CAMPAIGN.read_text(encoding="utf-8")
    for hook in REQUIRED_CAMPAIGN_HOOKS:
        status &= ok(f"campaign contains {hook}", hook in campaign)

if JS.exists():
    js = JS.read_text(encoding="utf-8")
    for needle in REQUIRED_JS_STRINGS:
        status &= ok(f"ff-app.js contains {needle}", needle in js)

home_text = group_text(existing_paths(TARGETS["home"]))
dashboard_text = group_text(existing_paths(TARGETS["dashboard"]))
pricing_text = group_text(existing_paths(TARGETS["pricing"]))

status &= ok(
    "home group has optional support-plan expansion",
    "optional support-plan expansion" in home_text
)

status &= ok(
    "dashboard group has Partner Sponsor or VIP Sponsor",
    ("Partner Sponsor" in dashboard_text) or ("VIP Sponsor" in dashboard_text)
)

status &= ok(
    "pricing group has Start guided launch",
    "Start guided launch" in pricing_text
)

status &= ok(
    "pricing group has Open founder demo",
    "Open founder demo" in pricing_text
)

raise SystemExit(0 if status else 1)
