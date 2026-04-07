from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
PRICING = ROOT / "apps/web/app/templates/platform/pages/pricing.html"
CAMPAIGN = ROOT / "apps/web/app/templates/campaign/index.html"

for path in (PRICING, CAMPAIGN):
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
for path in (PRICING, CAMPAIGN):
    shutil.copy2(path, path.with_name(f"{path.name}.{timestamp}.bak"))

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old in text:
        print(f"changed: {label}")
        return text.replace(old, new, 1)
    print(f"MISS: {label}")
    return text

pricing_text = PRICING.read_text(encoding="utf-8")
campaign_text = CAMPAIGN.read_text(encoding="utf-8")

# -------------------------------------------------------------------
# PRICING: make Growth the smart default and White-label feel premium
# -------------------------------------------------------------------
pricing_replacements = [
    (
        "Perfect for first launches and founder-led setup offers.",
        "Best for first launches, fast founder-led closes, and getting a real buyer-facing example live.",
        "starter fit",
    ),
    (
        "Best for programs ready to add sponsor packages and recurring support.",
        "Best for programs ready to monetize sponsor packages and recurring support.",
        "growth body",
    ),
    (
        "Great for schools, clubs, and growing youth programs.",
        "The smart default once the fundraiser becomes part of your operating system.",
        "growth fit",
    ),
    (
        "Start Growth setup",
        "Choose Growth",
        "growth cta",
    ),
    (
        "Best for schools, nonprofits, and larger organizations that want a fuller branded operating system.",
        "Best for schools, nonprofits, and institutions that want a fuller branded operating system with stronger approvals-ready presentation.",
        "white-label body",
    ),
    (
        "Best when you want the platform to feel like your organization’s own system.",
        "Best when you need a premium institution-facing rollout, procurement-ready feel, and more hands-on support.",
        "white-label fit",
    ),
    (
        "Request white-label path",
        "Talk to founder",
        "white-label cta",
    ),
    (
        "Most programs should start on Starter, prove the fundraiser, then upgrade to Growth when sponsor packages and recurring support start driving revenue.",
        "Most programs should start on Starter, prove the fundraiser, then upgrade to Growth once sponsor packages and recurring support start paying for the platform.",
        "pricing close body",
    ),
]

for old, new, label in pricing_replacements:
    pricing_text = replace_once(pricing_text, old, new, label)

# -------------------------------------------------------------------
# CAMPAIGN: make sponsor lane feel custom + invoice-ready
# -------------------------------------------------------------------
campaign_replacements = [
    (
        "Support the program while getting real local visibility. Sponsorships may be tax-deductible.",
        "Support the program while getting real local visibility. Sponsorships may be tax-deductible, custom packages are available, and invoices can be arranged for larger supporters.",
        "sponsor pitch",
    ),
    (
        "Top logo placement, VIP spotlight, shoutouts, and community exposure.",
        "Top logo placement, VIP spotlight, shoutouts, community exposure, and first-right visibility for premium supporters.",
        "founding sponsor perk",
    ),
    (
        "Logo placement, shoutouts, and featured sponsor presence.",
        "Logo placement, shoutouts, and featured sponsor presence for businesses that want a strong local footprint.",
        "silver sponsor perk",
    ),
    (
        "Business name placement and community appreciation visibility.",
        "Business name placement, community appreciation visibility, and an easy first step for local supporters.",
        "community sponsor perk",
    ),
]

for old, new, label in campaign_replacements:
    campaign_text = replace_once(campaign_text, old, new, label)

PRICING.write_text(pricing_text, encoding="utf-8")
CAMPAIGN.write_text(campaign_text, encoding="utf-8")

print("done.")
