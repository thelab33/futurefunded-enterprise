from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATE = ROOT / "apps/web/app/templates/campaign/index.html"

if not TEMPLATE.exists():
    raise SystemExit(f"Missing template: {TEMPLATE}")

src = TEMPLATE.read_text(encoding="utf-8")
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = TEMPLATE.with_name(f"{TEMPLATE.name}.{timestamp}.bak")
shutil.copy2(TEMPLATE, backup)

updated = src
applied = []

def replace_if_present(old: str, new: str, label: str, replace_all: bool = False) -> None:
    global updated
    if old in updated:
        if replace_all:
            updated = updated.replace(old, new)
        else:
            updated = updated.replace(old, new, 1)
        applied.append(label)

replace_if_present(
    """{% set _safe_campaign_tagline = (_campaign_tagline|default('Support travel, training, and season costs with one secure gift.', true)|string|trim) %}""",
    """{% set _safe_campaign_tagline = (_campaign_tagline|default('Back travel, training, and season costs with one secure gift.', true)|string|trim) %}""",
    "_safe_campaign_tagline fallback"
)

replace_if_present(
    """Secure checkout • Email receipt • Sponsor follow-up by email.""",
    """Secure checkout • Email receipt • Sponsor-friendly follow-up.""",
    "residual trust cue copy",
    replace_all=True
)

if updated == src:
    print("== FF CAMPAIGN HERO + TEAMS CLOSEOUT MOPUP V1 ==")
    print(f"backup: {backup}")
    print("No remaining residue strings found.")
    raise SystemExit(0)

TEMPLATE.write_text(updated, encoding="utf-8")

print("== FF CAMPAIGN HERO + TEAMS CLOSEOUT MOPUP V1 ==")
print(f"backup: {backup}")
print("applied:")
for item in applied:
    print(f" - {item}")
print("done.")
