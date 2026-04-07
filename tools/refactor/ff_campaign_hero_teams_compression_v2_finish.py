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

def replace_if_present(old: str, new: str, label: str) -> None:
    global updated
    if old in updated:
        updated = updated.replace(old, new, 1)
        applied.append(label)

# ------------------------------------------------------------------
# Remaining HERO copy cleanup
# ------------------------------------------------------------------

replace_if_present(
    """{% set _campaign_tagline = (campaign_tagline|default('Support travel, training, and season costs with one secure gift.', true))|string|trim %}
{% if not _campaign_tagline %}
  {% set _campaign_tagline = 'Support travel, training, and season costs with one secure gift.' %}
{% endif %}""",
    """{% set _campaign_tagline = (campaign_tagline|default('Back travel, training, and season costs with one secure gift.', true))|string|trim %}
{% if not _campaign_tagline %}
  {% set _campaign_tagline = 'Back travel, training, and season costs with one secure gift.' %}
{% endif %}""",
    "campaign tagline default"
)

replace_if_present(
    """                      Sponsor the program""",
    """                      Sponsor the season""",
    "hero sponsor CTA label"
)

replace_if_present(
    """                  Secure checkout • Email receipt • Sponsor follow-up by email.""",
    """                  Secure checkout • Email receipt • Sponsor-friendly follow-up.""",
    "hero trust cue"
)

replace_if_present(
    """                Start with a quick amount, then confirm in checkout.""",
    """                Choose an amount, then confirm in checkout.""",
    "hero panel helper copy"
)

replace_if_present(
    """                Travel, tournaments, gym time, and the season costs that keep the program moving.""",
    """                Travel, tournaments, gym time, and core season costs.""",
    "hero donation note"
)

replace_if_present(
    """                  Businesses can support through a dedicated sponsor path.""",
    """                  Businesses can support through a clean sponsor path.""",
    "hero sponsorship note"
)

if updated == src:
    print("== FF CAMPAIGN HERO + TEAMS COMPRESSION V2 FINISH ==")
    print(f"backup: {backup}")
    print("No remaining hero/team text changes were needed.")
    raise SystemExit(0)

TEMPLATE.write_text(updated, encoding="utf-8")

print("== FF CAMPAIGN HERO + TEAMS COMPRESSION V2 FINISH ==")
print(f"backup: {backup}")
print("applied:")
for item in applied:
    print(f" - {item}")
print("done.")
