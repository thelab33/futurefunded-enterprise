from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path.home() / "futurefunded-enterprise"
TROOT = ROOT / "apps/web/app/templates"
CAMPAIGN = TROOT / "campaign" / "index.html"
JS = ROOT / "apps/web/app/static/js/ff-app.js"

DISCOVERY = {
    "home": "Give Connect ATX Elite a premium fundraising home.",
    "onboarding": "Step 1 · Launch Connect ATX Elite",
    "dashboard": "FutureFunded command center",
    "pricing": "Launch a sponsor-ready fundraiser in minutes.",
    "demo": "See FutureFunded in action.",
}

REQUIRED_CAMPAIGN_HOOKS = [
    'data-ff-open-checkout',
    'data-ff-close-checkout',
    'data-ff-sponsor-modal',
    'data-ff-close-sponsor',
    'data-ff-share',
    'data-ff-checkout-status',
    'data-ff-checkout-sheet',
    'sponsorInterestTitle',
    'Terms',
    'Privacy',
]

REQUIRED_JS_STRINGS = [
    'openCheckout',
    'closeCheckout',
    'checkoutSheet',
    'share',
    'sponsor',
]

def find_template(needle: str) -> Path:
    for path in TROOT.rglob("*.html"):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        if needle in text:
            return path
    raise SystemExit(f"❌ Could not find template containing: {needle!r}")

def ok(label: str, passed: bool, detail: str = "") -> bool:
    icon = "✅" if passed else "❌"
    print(f"{icon} {label}" + (f" — {detail}" if detail else ""))
    return passed

def main() -> int:
    status = True

    print("== FOUNDER LAUNCH SMOKE V1 ==")

    targets = {name: find_template(needle) for name, needle in DISCOVERY.items()}
    for name, path in targets.items():
        status &= ok(f"{name} template discovered", path.exists(), str(path))

    status &= ok("campaign template exists", CAMPAIGN.exists(), str(CAMPAIGN))
    status &= ok("ff-app.js exists", JS.exists(), str(JS))

    if CAMPAIGN.exists():
        campaign = CAMPAIGN.read_text(encoding="utf-8")
        for hook in REQUIRED_CAMPAIGN_HOOKS:
            status &= ok(f"campaign contains {hook}", hook in campaign)

        for expected_copy in [
            "Start guided launch",
            "Become a sponsor",
            "Donate",
            "Support completed",
        ]:
            status &= ok(f"campaign copy contains {expected_copy}", expected_copy in campaign)

    if JS.exists():
        js = JS.read_text(encoding="utf-8")
        for needle in REQUIRED_JS_STRINGS:
            status &= ok(f"ff-app.js contains {needle}", needle in js)

    # Platform copy proofs
    for name, path in targets.items():
        text = path.read_text(encoding="utf-8")
        if name == "pricing":
            status &= ok("pricing has Start guided launch", "Start guided launch" in text)
            status &= ok("pricing has Open founder demo", "Open founder demo" in text)
        if name == "dashboard":
            status &= ok("dashboard has Partner Sponsor or VIP Sponsor", ("Partner Sponsor" in text) or ("VIP Sponsor" in text))
        if name == "home":
            status &= ok("home has optional support-plan expansion", "optional support-plan expansion" in text)

    return 0 if status else 1

if __name__ == "__main__":
    raise SystemExit(main())
