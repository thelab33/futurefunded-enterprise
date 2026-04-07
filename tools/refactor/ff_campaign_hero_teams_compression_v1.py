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

def replace_once(old: str, new: str, label: str) -> None:
    global updated
    if old not in updated:
        raise SystemExit(f"Could not find expected block for: {label}")
    updated = updated.replace(old, new, 1)

# ------------------------------------------------------------------
# PATCH 03 — HERO COPY COMPRESSION
# ------------------------------------------------------------------

replace_once(
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

replace_once(
    """                    Clear progress, fast checkout, and a fundraising surface designed to feel credible from the first glance.""",
    """                    Clear progress, fast checkout, and a page donors can trust right away.""",
    "hero donor trust copy"
)

replace_once(
    """                    Structured recognition, clean community alignment, and a presentation businesses can comfortably support.""",
    """                    Structured recognition and clean placement for local businesses and community partners.""",
    "hero sponsor proof copy"
)

replace_once(
    """                      Sponsor the program""",
    """                      Sponsor the season""",
    "hero sponsor CTA label"
)

replace_once(
    """                  Secure checkout • Email receipt • Sponsor follow-up by email.""",
    """                  Secure checkout • Email receipt • Sponsor-friendly follow-up.""",
    "hero trust cue"
)

replace_once(
    """                Start with a quick amount, then confirm in checkout.""",
    """                Choose an amount, then confirm in checkout.""",
    "hero panel helper copy"
)

replace_once(
    """                Travel, tournaments, gym time, and the season costs that keep the program moving.""",
    """                Travel, tournaments, gym time, and core season costs.""",
    "hero donation note"
)

replace_once(
    """                  Businesses can support through a dedicated sponsor path.""",
    """                  Businesses can support through a clean sponsor path.""",
    "hero sponsorship note"
)

# ------------------------------------------------------------------
# PATCH 04 — TEAMS DENSITY CLEANUP
# ------------------------------------------------------------------

replace_once(
    """          Back the team you know best while every gift still helps the full program.""",
    """          Support the team you know while every gift still helps the full program.""",
    "teams section lead"
)

replace_once(
    """          Every donation supports the full program, even when a supporter gives through one specific team.""",
    """          Every gift still supports the full program, even when someone gives through one team.""",
    "shared fund note"
)

replace_once(
    """                  <div class="ff-row ff-row--between ff-ais ff-gap-2 ff-wrap ff-mt-2">
                    <div class="ff-minw-0">
                      <h3
                        class="ff-h3 ff-m-0 ff-teamCard__title"
                        id="team-{{ tid|e }}-name"
                        data-ff-team-name="{{ tid|e }}"
                        data-team-name="{{ tid|e }}"
                      >
                        {{ tname|e }}
                      </h3>

                      {% if tmeta %}
                        <p
                          class="ff-help ff-muted ff-mt-1 ff-mb-0 ff-teamCard__meta"
                          data-team-meta="{{ tid|e }}"
                        >
                          {{ tmeta|e }}
                        </p>
                      {% endif %}
                    </div>

                    <div class="ff-proofMini ff-teamCard__summary">
                      <p class="ff-kicker ff-m-0">Progress</p>
                      <p class="ff-h3 ff-mt-1 ff-mb-0 ff-num">{{ _teams_shared_pct }}%</p>
                    </div>
                  </div>""",
    """                  <div class="ff-row ff-ais ff-gap-2 ff-wrap ff-mt-2">
                    <div class="ff-minw-0">
                      <h3
                        class="ff-h3 ff-m-0 ff-teamCard__title"
                        id="team-{{ tid|e }}-name"
                        data-ff-team-name="{{ tname|e }}"
                        data-team-name="{{ tname|e }}"
                      >
                        {{ tname|e }}
                      </h3>

                      {% if tmeta %}
                        <p
                          class="ff-help ff-muted ff-mt-1 ff-mb-0 ff-teamCard__meta"
                          data-team-meta="{{ tid|e }}"
                        >
                          {{ tmeta|e }}
                        </p>
                      {% endif %}
                    </div>
                  </div>""",
    "team card title row density cleanup"
)

replace_once(
    """                      {{ _teams_shared_pct }}% of the shared goal funded""",
    """                      Shared season progress""",
    "team card meter helper"
)

if updated == src:
    raise SystemExit("No changes applied; template may already be patched")

TEMPLATE.write_text(updated, encoding="utf-8")

print("== FF CAMPAIGN HERO + TEAMS COMPRESSION V1 ==")
print(f"backup: {backup}")
print("done.")
