from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
INDEX = ROOT / "apps/web/app/templates/campaign/index.html"
CSS = ROOT / "apps/web/app/static/css/ff.css"

for path in (INDEX, CSS):
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
for path in (INDEX, CSS):
    shutil.copy2(path, path.with_name(f"{path.name}.{timestamp}.bak"))

index_text = INDEX.read_text(encoding="utf-8")
css_text = CSS.read_text(encoding="utf-8")

def replace_once(text: str, old: str, new: str, label: str):
    if old not in text:
        print(f"MISS: {label}")
        return text
    print(f"changed: {label}")
    return text.replace(old, new, 1)

# -------------------------------------------------------------------
# 1) Dynamic urgency logic
# -------------------------------------------------------------------
old_urgency = """{% set _remaining_to_goal = ((_goal_bar - _raised_bar) if _goal_bar > _raised_bar else 0.0) %}
{% if _remaining_to_goal > 0 %}
  {% set _urgency_label = 'Only ' ~ money(_remaining_to_goal) ~ ' left to hit our goal 🎯' %}
{% else %}
  {% set _urgency_label = 'Goal reached 🎉' %}
{% endif %}"""

new_urgency = """{% set _remaining_to_goal = ((_goal_bar - _raised_bar) if _goal_bar > _raised_bar else 0.0) %}
{% if _remaining_to_goal > 1500 %}
  {% set _push = 250 %}
{% elif _remaining_to_goal > 600 %}
  {% set _push = 150 %}
{% else %}
  {% set _push = _remaining_to_goal %}
{% endif %}
{% if _remaining_to_goal > 0 %}
  {% set _urgency_label = 'Only ' ~ money(_remaining_to_goal) ~ ' left — push the next $' ~ (_push|round(0, 'floor')|int) ~ ' 🎯' %}
{% else %}
  {% set _urgency_label = 'Goal reached 🎉' %}
{% endif %}"""

index_text = replace_once(index_text, old_urgency, new_urgency, "dynamic urgency logic")

# -------------------------------------------------------------------
# 2) Hero trust strip upgrade
# -------------------------------------------------------------------
old_hero_trust = """<div
                class="ff-trustStrip ff-trustStrip--compact ff-mt-2"
                role="list"
                aria-label="Trust signals"
              >
                <span class="ff-trustStrip__item" role="listitem">🔒 Secure payments</span>
                <span class="ff-trustStrip__item" role="listitem">💳 All major cards</span>
                <span class="ff-trustStrip__item" role="listitem">❤️ Directly supports players</span>
              </div>"""

new_hero_trust = """<div
                class="ff-trustStrip ff-trustStrip--compact ff-mt-2"
                aria-label="Trust signals"
              >
                <div class="ff-trustStrip__row" role="list" aria-label="Primary trust signals">
                  <span class="ff-trustStrip__item" role="listitem">🔒 Secure checkout powered by Stripe</span>
                  <span class="ff-trustStrip__item" role="listitem">💳 All major cards + Apple Pay</span>
                  <span class="ff-trustStrip__item" role="listitem">⚡ Takes less than 30 seconds</span>
                </div>
                <div class="ff-trustStrip__row ff-trustStrip__row--soft" role="list" aria-label="Social proof signals">
                  <span class="ff-trustStrip__item" role="listitem">👥 Trusted by teams, schools, and nonprofits</span>
                  <span class="ff-trustStrip__item" role="listitem">📈 $24,000+ raised across programs</span>
                </div>
              </div>"""

index_text = replace_once(index_text, old_hero_trust, new_hero_trust, "hero trust strip")

# -------------------------------------------------------------------
# 3) Sponsor revenue pitch
# -------------------------------------------------------------------
old_sponsor_grid = '<div class="ff-sponsorSpotlight__grid ff-mt-3">'
new_sponsor_grid = """<p class="ff-sponsorPitch ff-mt-2 ff-mb-0">
            Support the program while getting real local visibility. Sponsorships may be tax-deductible.
          </p>
          <div class="ff-sponsorSpotlight__grid ff-mt-3">"""

index_text = replace_once(index_text, old_sponsor_grid, new_sponsor_grid, "sponsor pitch insertion")

index_text = replace_once(index_text, "Gold Sponsor", "Founding Sponsor", "founding sponsor label")
index_text = replace_once(index_text, "Top visibility", "Limited availability", "founding sponsor badge")
index_text = replace_once(
    index_text,
    "Top logo placement, VIP spotlight, and featured recognition.",
    "Top logo placement, VIP spotlight, shoutouts, and community exposure.",
    "founding sponsor perk"
)

# -------------------------------------------------------------------
# 4) Checkout trust + emotion upgrade
# -------------------------------------------------------------------
old_checkout_trust = """<div
class="ff-trustStrip ff-trustStrip--checkout ff-mt-3"
role="list"
aria-label="Checkout trust signals"
>
<span class="ff-trustStrip__item" role="listitem">🔒 Secure payments (Stripe)</span>
<span class="ff-trustStrip__item" role="listitem">💳 All major cards</span>
<span class="ff-trustStrip__item" role="listitem">❤️ Directly supports players</span>
</div>"""

new_checkout_trust = """<div
class="ff-trustStrip ff-trustStrip--checkout ff-mt-3"
aria-label="Checkout trust signals"
>
<div class="ff-trustStrip__row" role="list" aria-label="Checkout trust signals">
<span class="ff-trustStrip__item" role="listitem">🔒 Secure</span>
<span class="ff-trustStrip__item" role="listitem">🏦 Powered by Stripe</span>
<span class="ff-trustStrip__item" role="listitem">📜 Receipt included</span>
</div>
</div>

<p class="ff-checkoutEmotion ff-mt-3 ff-mb-0">
You're supporting travel, training, tournament fees, and equipment for the team.
</p>"""

index_text = replace_once(index_text, old_checkout_trust, new_checkout_trust, "checkout trust + emotion")

INDEX.write_text(index_text, encoding="utf-8")

# -------------------------------------------------------------------
# 5) CSS additive polish block
# -------------------------------------------------------------------
css_marker = "FF_POLISH_V3_TRUST_REVENUE_CLOSE"
if css_marker not in css_text:
    css_block = """
/* ==========================================================================
   FF_POLISH_V3_TRUST_REVENUE_CLOSE
   Trust, sponsor revenue, and checkout confidence polish
   ========================================================================== */

body[data-ff-page="fundraiser"] .ff-trustStrip {
  display: grid;
  gap: 0.45rem;
}

body[data-ff-page="fundraiser"] .ff-trustStrip__row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem;
  align-items: center;
}

body[data-ff-page="fundraiser"] .ff-trustStrip__row--soft {
  opacity: 0.78;
}

body[data-ff-page="fundraiser"] .ff-trustStrip__item {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  min-height: 2rem;
  padding: 0.4rem 0.72rem;
  border: 1px solid color-mix(in srgb, var(--ff-line, rgba(255,255,255,.12)) 86%, transparent);
  border-radius: 999px;
  background: color-mix(in srgb, var(--ff-surface-2, rgba(255,255,255,.07)) 94%, transparent);
  color: var(--ff-text-soft, #e5eef8);
  font-size: 0.8rem;
  line-height: 1.2;
  box-shadow: 0 8px 20px rgba(0,0,0,.12);
}

body[data-ff-page="fundraiser"] .ff-sponsorPitch {
  max-width: 52ch;
  font-size: 0.95rem;
  line-height: 1.6;
  color: var(--ff-text-soft, rgba(255,255,255,.82));
}

body[data-ff-page="fundraiser"] .ff-checkoutEmotion {
  max-width: 52ch;
  font-size: 0.92rem;
  line-height: 1.55;
  color: var(--ff-text-soft, rgba(255,255,255,.82));
}

body[data-ff-page="fundraiser"] .ff-sponsorSpotlight__card--gold {
  background:
    radial-gradient(circle at top right, rgba(255,210,84,.24), transparent 42%),
    linear-gradient(180deg, rgba(255,184,76,.08), rgba(255,184,76,0)),
    color-mix(in srgb, var(--ff-surface-2, rgba(255,255,255,.08)) 94%, transparent);
  border-color: rgba(255,210,84,.22);
  box-shadow:
    0 16px 34px rgba(0,0,0,.22),
    inset 0 1px 0 rgba(255,255,255,.06);
}

@media (max-width: 640px) {
  body[data-ff-page="fundraiser"] .ff-trustStrip__row {
    gap: 0.5rem;
  }

  body[data-ff-page="fundraiser"] .ff-trustStrip__item {
    width: 100%;
    justify-content: center;
    text-align: center;
  }

  body[data-ff-page="fundraiser"] .ff-sponsorPitch,
  body[data-ff-page="fundraiser"] .ff-checkoutEmotion {
    font-size: 0.9rem;
  }
}
""".strip() + "\n"
    css_text = css_text.rstrip() + "\n\n" + css_block
    CSS.write_text(css_text, encoding="utf-8")
    print("changed: additive css polish block")
else:
    print("MISS: additive css polish block already present")

print("done.")
