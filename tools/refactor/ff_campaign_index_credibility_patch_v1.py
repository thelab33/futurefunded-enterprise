from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
TARGET = ROOT / "apps/web/app/templates/campaign/index.html"

text = TARGET.read_text(encoding="utf-8")

def replace_once(old: str, new: str, label: str) -> None:
    global text
    if old not in text:
        raise SystemExit(f"missing block for {label}")
    text = text.replace(old, new, 1)
    print(f"patched: {label}")

story_sponsor_old = """            <a
              class="ff-btn ff-btn--secondary ff-btn--pill"
              href="#sponsors"
            >
              Sponsor
            </a>"""

story_sponsor_new = """            <a
              class="ff-btn ff-btn--secondary ff-btn--pill"
              href="#sponsor-interest"
              aria-controls="sponsor-interest"
              aria-haspopup="dialog"
              data-ff-open-sponsor=""
            >
              Sponsor
            </a>"""

teams_actions_old = """      <div
        class="ff-sectionhead__actions ff-row ff-wrap ff-gap-2"
        role="group"
        aria-label="Teams actions"
      >
        <a
          class="ff-btn ff-btn--sm ff-btn--primary ff-btn--pill ff-donate-btn"
          href="#checkout"
          aria-controls="checkout"
          aria-haspopup="dialog"
          data-ff-donate=""
          data-ff-open-checkout=""
        >
          Donate
        </a>
      </div>"""

teams_actions_new = """      <div
        class="ff-sectionhead__actions ff-row ff-wrap ff-gap-2"
        role="group"
        aria-label="Teams actions"
      >
        <a
          class="ff-btn ff-btn--sm ff-btn--primary ff-btn--pill ff-donate-btn"
          href="#checkout"
          aria-controls="checkout"
          aria-haspopup="dialog"
          data-ff-donate=""
          data-ff-open-checkout=""
        >
          Donate
        </a>

        <a
          class="ff-btn ff-btn--sm ff-btn--secondary ff-btn--pill"
          href="#sponsor-interest"
          aria-controls="sponsor-interest"
          aria-haspopup="dialog"
          data-ff-open-sponsor=""
        >
          Sponsor the season
        </a>
      </div>"""

teams_note_old = """      <div class="ff-proofMini ff-proofMini--teams" role="note" aria-label="Shared fund note">
        <p class="ff-kicker ff-m-0">Shared season fund</p>
        <p class="ff-help ff-muted ff-mt-1 ff-mb-0">
          Every gift still supports the full program, even when someone gives through one team.
        </p>
      </div>"""

teams_note_new = """      <div class="ff-proofMini ff-proofMini--teams" role="note" aria-label="Shared fund note">
        <div
          class="ff-row ff-wrap ff-gap-2"
          role="list"
          aria-label="Shared fund highlights"
        >
          <span class="ff-pill ff-pill--soft" role="listitem">One shared season fund</span>
          <span class="ff-pill ff-pill--ghost" role="listitem">Team-preselect checkout</span>
          <span class="ff-pill ff-pill--ghost" role="listitem">Sponsor-ready</span>
        </div>

        <p class="ff-help ff-muted ff-mt-2 ff-mb-0">
          Support can start from a team card for a more personal path, but gifts still support the full program unless a campaign is clearly marked restricted.
        </p>

        <p class="ff-help ff-muted ff-mt-1 ff-mb-0">
          {{ money(_teams_shared_raised) }} raised toward {{ money(_teams_shared_goal) }} • {{ _teams_shared_pct }}% of the shared season goal.
        </p>
      </div>"""

team_stats_old = """                  <div
                    class="ff-teamCard__stats ff-mt-3"
                    aria-label="{{ tname|e }} fundraising snapshot"
                  >
                    <span class="ff-teamStat">
                      <span class="ff-teamStat__label">Raised</span>
                      <strong class="ff-teamStat__value">{{ money(_teams_shared_raised) }}</strong>
                    </span>

                    <span class="ff-teamStat">
                      <span class="ff-teamStat__label">Goal</span>
                      <strong class="ff-teamStat__value">{{ money(_teams_shared_goal) }}</strong>
                    </span>

                    <span class="ff-teamStat">
                      <span class="ff-teamStat__label">Progress</span>
                      <strong class="ff-teamStat__value">{{ _teams_shared_pct }}%</strong>
                    </span>
                  </div>

                  <div class="ff-teamCard__meter" aria-label="{{ tname|e }} progress meter">
                    <progress
                      class="ff-teamCard__meterBar"
                      max="100"
                      value="{{ _teams_shared_pct }}"
                    >
                      {{ _teams_shared_pct }}%
                    </progress>
                    <span class="ff-teamCard__meterText">
                      Shared season progress
                    </span>
                  </div>

                  <div class="ff-proofMini ff-mt-3 ff-teamCard__ask">
                    <p class="ff-kicker ff-m-0">Current focus</p>
                    <p class="ff-help ff-muted ff-mt-1 ff-mb-0">{{ task|e }}</p>
                  </div>"""

team_stats_new = """                  <div
                    class="ff-proofMini ff-mt-3"
                    role="note"
                    aria-label="{{ tname|e }} support routing"
                  >
                    <p class="ff-kicker ff-m-0">How support routes</p>
                    <p class="ff-help ff-muted ff-mt-1 ff-mb-0">
                      This action preloads checkout for {{ tname|e }}, while gifts still support the shared season fund unless a campaign is clearly marked restricted.
                    </p>
                  </div>

                  <div
                    class="ff-row ff-wrap ff-gap-2 ff-mt-3"
                    role="list"
                    aria-label="{{ tname|e }} team signals"
                  >
                    <span class="ff-pill ff-pill--ghost" role="listitem">Shared fund</span>

                    {% if t.tier %}
                      <span class="ff-pill ff-pill--ghost" role="listitem">{{ t.tier|e }}</span>
                    {% endif %}

                    {% if t.featured|default(false, true) %}
                      <span class="ff-pill ff-pill--accent" role="listitem">Featured team</span>
                    {% elif t.needs|default(false, true) %}
                      <span class="ff-pill ff-pill--soft" role="listitem">Current push</span>
                    {% else %}
                      <span class="ff-pill ff-pill--soft" role="listitem">Active roster</span>
                    {% endif %}
                  </div>

                  <div class="ff-proofMini ff-mt-3 ff-teamCard__ask">
                    <p class="ff-kicker ff-m-0">Current focus</p>
                    <p class="ff-help ff-muted ff-mt-1 ff-mb-0">{{ task|e }}</p>
                  </div>"""

replace_once(story_sponsor_old, story_sponsor_new, "story sponsor CTA -> modal sponsor path")
replace_once(teams_actions_old, teams_actions_new, "teams header sponsor entry")
replace_once(teams_note_old, teams_note_new, "teams shared-fund note upgrade")
replace_once(team_stats_old, team_stats_new, "team card repeated totals -> routing note")

ts = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = TARGET.with_name(f"{TARGET.name}.{ts}.bak")
shutil.copy2(TARGET, backup)
TARGET.write_text(text, encoding="utf-8")

print(f"changed: {TARGET}")
print(f"backup:  {backup}")
