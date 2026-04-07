from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path.home() / "futurefunded-enterprise"

FILES = [
    ROOT / "apps/web/app/templates/campaign/index.html",
    ROOT / "apps/web/app/templates/platform/pages/home.html",
    ROOT / "apps/web/app/templates/platform/pages/pricing.html",
]

for path in FILES:
    if path.exists():
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        shutil.copy2(path, path.with_name(f"{path.name}.{ts}.bak"))

def write_if_changed(path: Path, text: str, original: str, label: str):
    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"changed: {label}")
    else:
        print(f"MISS: {label}")

# ------------------------------------------------------------
# campaign shared-fund clarification insert
# ------------------------------------------------------------
campaign = ROOT / "apps/web/app/templates/campaign/index.html"
if campaign.exists():
    original = campaign.read_text(encoding="utf-8")
    text = original

    if "shared program fund unless a restricted campaign is clearly marked" not in text:
        text = re.sub(
            r"(Support the teams you know while every gift still helps the .*?program\.)",
            r"\1 Team cards show who the program serves, while support still feeds the shared program fund unless a restricted campaign is clearly marked.",
            text,
            count=1,
            flags=re.S,
        )

    write_if_changed(campaign, text, original, "campaign shared-fund clarification insert")

# ------------------------------------------------------------
# home fallback CTA normalization
# ------------------------------------------------------------
home = ROOT / "apps/web/app/templates/platform/pages/home.html"
if home.exists():
    original = home.read_text(encoding="utf-8")
    text = original

    text = text.replace('"primary_cta_label": "Start founder setup"', '"primary_cta_label": "Start guided launch"')
    text = text.replace('"secondary_cta_label": "Open dashboard"', '"secondary_cta_label": "Open operator dashboard"')
    text = text.replace('"close_primary_label": "Start founder setup"', '"close_primary_label": "Start guided launch"')
    text = text.replace('"close_secondary_label": "Open operator dashboard"', '"close_secondary_label": "Open operator dashboard"')

    write_if_changed(home, text, original, "home cta normalization")

# ------------------------------------------------------------
# pricing CTA normalization
# ------------------------------------------------------------
pricing = ROOT / "apps/web/app/templates/platform/pages/pricing.html"
if pricing.exists():
    original = pricing.read_text(encoding="utf-8")
    text = original

    text = text.replace('"cta_label": "Talk to founder"', '"cta_label": "Talk to founder"')
    text = text.replace('{"label": "Start guided launch", "href": "/platform/onboarding"}', '{"label": "Start guided launch", "href": "/platform/onboarding"}')
    text = text.replace('{"label": "Open live fundraiser", "href": "/c/spring-fundraiser"}', '{"label": "Open live fundraiser", "href": "/c/spring-fundraiser"}')

    if '"secondary_cta_label": "Open live fundraiser"' not in text:
        text = text.replace('"primary_cta_label": "Start guided launch"', '"primary_cta_label": "Start guided launch"')

    write_if_changed(pricing, text, original, "pricing cta normalization")

print("done.")
