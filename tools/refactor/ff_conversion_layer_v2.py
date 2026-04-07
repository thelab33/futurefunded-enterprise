from __future__ import annotations
from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATE = ROOT / "apps/web/app/templates/campaign/index.html"
CSS = ROOT / "apps/web/app/static/css/ff.css"
JS = ROOT / "apps/web/app/static/js/ff-app.js"

STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

def backup(path: Path) -> None:
    shutil.copy2(path, path.with_suffix(path.suffix + f".bak.{STAMP}"))

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")

def replace_once(text: str, needle: str, insert: str) -> str:
    if insert in text:
        return text
    if needle not in text:
        raise SystemExit(f"Needle not found:\\n{needle[:180]}")
    return text.replace(needle, insert + needle, 1)

def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.strip() + "\n"

for p in (TEMPLATE, CSS, JS):
    if not p.exists():
        raise SystemExit(f"Missing required file: {p}")

backup(TEMPLATE)
backup(CSS)
backup(JS)

template = read(TEMPLATE)
css = read(CSS)
js = read(JS)

# -------------------------------------------------------------------
# 1) Jinja vars: urgency + sponsor spotlight data
# -------------------------------------------------------------------
vars_anchor = """{% set _quick_amounts = _quick_amounts|default([
  (35, 'Quick support'),
  (75, 'Most common'),
  (150, 'Travel help'),
  (250, 'Big lift')
], true) %}"""

vars_block = """{% set _remaining_to_goal = ((_goal_bar - _raised_bar) if _goal_bar > _raised_bar else 0.0) %}
{% if _remaining_to_goal > 0 %}
  {% set _urgency_label = 'Only ' ~ money(_remaining_to_goal) ~ ' left to hit our goal 🎯' %}
{% else %}
  {% set _urgency_label = 'Goal reached 🎉' %}
{% endif %}

{% set _conversion_sponsor_spotlight = _conversion_sponsor_spotlight|default([
  {
    'label': 'Gold Sponsor',
    'amount_label': '$1,000+',
    'amount_value': 1000,
    'badge': 'Top visibility',
    'perk': 'Top logo placement, VIP spotlight, and featured recognition.',
    'tone': 'gold'
  },
  {
    'label': 'Silver Sponsor',
    'amount_label': '$500+',
    'amount_value': 500,
    'badge': 'Strong local visibility',
    'perk': 'Logo placement, shoutouts, and featured sponsor presence.',
    'tone': 'silver'
  },
  {
    'label': 'Community Sponsor',
    'amount_label': '$250+',
    'amount_value': 250,
    'badge': 'Easy first step',
    'perk': 'Business name placement and community appreciation visibility.',
    'tone': 'community'
  }
], true) %}

"""

template = replace_once(template, vars_anchor, vars_block)

# -------------------------------------------------------------------
# 2) Hero panel conversion band
# -------------------------------------------------------------------
hero_anchor = """            <div
              class="ff-grid ff-grid--2 ff-gap-2 ff-mt-3"
              role="group"
              aria-label="Quick donation amounts"
            >
              {% for amount, meta in _quick_amounts %}
                <button
                  type="button"
                  class="ff-chip ff-chip--pill"
                  data-ff-amount="{{ amount }}"
                  aria-label="Preload {{ amount }} dollars"
                >
                  <span class="ff-chip__amt">${{ amount }}</span>
                  <span class="ff-chip__meta">{{ meta }}</span>
                </button>
              {% endfor %}
            </div>
"""

hero_insert = """            <div
              class="ff-grid ff-grid--2 ff-gap-2 ff-mt-3"
              role="group"
              aria-label="Quick donation amounts"
            >
              {% for amount, meta in _quick_amounts %}
                <button
                  type="button"
                  class="ff-chip ff-chip--pill"
                  data-ff-amount="{{ amount }}"
                  aria-label="Preload {{ amount }} dollars"
                >
                  <span class="ff-chip__amt">${{ amount }}</span>
                  <span class="ff-chip__meta">{{ meta }}</span>
                </button>
              {% endfor %}
            </div>

            <section
              class="ff-conversionBand ff-conversionBand--hero ff-mt-3"
              aria-label="Urgency and trust"
            >
              <p class="ff-conversionBand__urgency ff-m-0">{{ _urgency_label }}</p>

              <div
                class="ff-trustStrip ff-trustStrip--compact ff-mt-2"
                role="list"
                aria-label="Trust signals"
              >
                <span class="ff-trustStrip__item" role="listitem">🔒 Secure payments</span>
                <span class="ff-trustStrip__item" role="listitem">💳 All major cards</span>
                <span class="ff-trustStrip__item" role="listitem">❤️ Directly supports players</span>
              </div>
            </section>
"""

if "ff-conversionBand--hero" not in template:
    template = template.replace(hero_anchor, hero_insert, 1)

# -------------------------------------------------------------------
# 3) Checkout conversion rail above amount chooser
# -------------------------------------------------------------------
checkout_anchor = """<fieldset class="ff-checkoutCard ff-checkoutCard--amount" aria-describedby="donationAmountHelp donationAmountNote" >
<legend class="ff-label ff-m-0" id="donationAmountLegend"> Choose an amount </legend>"""

checkout_insert = """<section
class="ff-checkoutCard ff-checkoutCard--conversion"
aria-labelledby="ffCheckoutConversionTitle"
aria-describedby="ffCheckoutConversionDesc"
>
<div class="ff-checkoutConversion__head">
<div class="ff-minw-0">
<p class="ff-kicker ff-m-0">Give faster</p>
<h3 class="ff-label ff-mt-1 ff-mb-0" id="ffCheckoutConversionTitle">Smart donation presets</h3>
<p class="ff-help ff-muted ff-mt-1 ff-mb-0" id="ffCheckoutConversionDesc">
Tap a preset to preload the donation amount instantly.
</p>
</div>
<p class="ff-checkoutConversion__urgency ff-m-0">{{ _urgency_label }}</p>
</div>

<div
class="ff-donation-presets ff-mt-3"
role="group"
aria-label="Smart donation presets"
>
<button type="button" class="ff-donation-presets__btn" data-ff-amount="25" aria-label="Choose 25 dollars">$25</button>
<button type="button" class="ff-donation-presets__btn" data-ff-amount="50" aria-label="Choose 50 dollars">$50</button>
<button type="button" class="ff-donation-presets__btn" data-ff-amount="100" aria-label="Choose 100 dollars">$100</button>
<button type="button" class="ff-donation-presets__btn ff-donation-presets__btn--feature" data-ff-amount="250" aria-label="Choose 250 dollars">$250</button>
</div>

<div
class="ff-trustStrip ff-trustStrip--checkout ff-mt-3"
role="list"
aria-label="Checkout trust signals"
>
<span class="ff-trustStrip__item" role="listitem">🔒 Secure payments (Stripe)</span>
<span class="ff-trustStrip__item" role="listitem">💳 All major cards</span>
<span class="ff-trustStrip__item" role="listitem">❤️ Directly supports players</span>
</div>
</section>

<fieldset class="ff-checkoutCard ff-checkoutCard--amount" aria-describedby="donationAmountHelp donationAmountNote" >
<legend class="ff-label ff-m-0" id="donationAmountLegend"> Choose an amount </legend>"""

if "ff-checkoutCard--conversion" not in template:
    if checkout_anchor not in template:
        raise SystemExit("Checkout anchor not found.")
    template = template.replace(checkout_anchor, checkout_insert, 1)

# -------------------------------------------------------------------
# 4) Sponsor spotlight strip above sponsor tier grid
# -------------------------------------------------------------------
sponsor_anchor = """        <ul
          class="ff-impactTierGrid ff-impactTierGrid--flagship ff-sponsorTierGrid"
          role="list"
          aria-label="Sponsor tier options"
        >"""

sponsor_insert = """        <section
          class="ff-sponsorSpotlight ff-mb-3"
          aria-labelledby="ffSponsorSpotlightTitle"
          aria-describedby="ffSponsorSpotlightDesc"
        >
          <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
            <div class="ff-minw-0">
              <p class="ff-kicker ff-m-0">Fast sponsor path</p>
              <h3 class="ff-h3 ff-mt-1 ff-mb-0" id="ffSponsorSpotlightTitle">
                Sponsor tiers built to upsell cleanly
              </h3>
              <p class="ff-help ff-muted ff-mt-1 ff-mb-0" id="ffSponsorSpotlightDesc">
                Choose a recognition level with practical visibility and an easy next step.
              </p>
            </div>

            <span class="ff-pill ff-pill--accent">Limited local sponsor spots</span>
          </div>

          <div class="ff-sponsorSpotlight__grid ff-mt-3">
            {% for tier in _conversion_sponsor_spotlight %}
              <a
                class="ff-sponsorSpotlight__card ff-sponsorSpotlight__card--{{ tier.tone }}"
                href="#sponsor-interest"
                data-ff-open-sponsor=""
                data-ff-sponsor-tier-choice="{{ tier.label }}"
                data-ff-sponsor-amount-value="{{ tier.amount_value }}"
                aria-label="Choose {{ tier.label }} sponsorship"
              >
                <span class="ff-sponsorSpotlight__badge">{{ tier.badge }}</span>
                <strong class="ff-sponsorSpotlight__title">{{ tier.label }}</strong>
                <span class="ff-sponsorSpotlight__amount">{{ tier.amount_label }}</span>
                <span class="ff-sponsorSpotlight__perk">{{ tier.perk }}</span>
              </a>
            {% endfor %}
          </div>
        </section>

        <ul
          class="ff-impactTierGrid ff-impactTierGrid--flagship ff-sponsorTierGrid"
          role="list"
          aria-label="Sponsor tier options"
        >"""

if "ff-sponsorSpotlight__grid" not in template:
    if sponsor_anchor not in template:
        raise SystemExit("Sponsor anchor not found.")
    template = template.replace(sponsor_anchor, sponsor_insert, 1)

write(TEMPLATE, template)

# -------------------------------------------------------------------
# 5) CSS append
# -------------------------------------------------------------------
css_block = r"""
/* ==========================================================================
   FF_CONVERSION_LAYER_V2
   Donate + sponsor conversion upgrades
   ========================================================================== */

.ff-conversionBand,
.ff-checkoutCard--conversion,
.ff-sponsorSpotlight {
  position: relative;
  overflow: clip;
  border: 1px solid color-mix(in srgb, var(--ff-line, rgba(255,255,255,.10)) 86%, transparent);
  background:
    linear-gradient(180deg, color-mix(in srgb, var(--ff-surface-2, rgba(255,255,255,.06)) 92%, transparent), color-mix(in srgb, var(--ff-surface-1, rgba(255,255,255,.04)) 94%, transparent));
  border-radius: 22px;
  box-shadow:
    0 12px 36px rgba(0,0,0,.18),
    inset 0 1px 0 rgba(255,255,255,.06);
}

.ff-conversionBand {
  padding: 14px 16px;
}

.ff-conversionBand__urgency,
.ff-checkoutConversion__urgency {
  font-weight: 800;
  letter-spacing: -.01em;
  color: var(--ff-text, #fff);
}

.ff-checkoutCard--conversion {
  padding: 18px;
}

.ff-checkoutConversion__head {
  display: grid;
  gap: 10px;
}

.ff-donation-presets {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.ff-donation-presets__btn {
  appearance: none;
  border: 1px solid color-mix(in srgb, var(--ff-line, rgba(255,255,255,.12)) 86%, transparent);
  background: color-mix(in srgb, var(--ff-surface-2, rgba(255,255,255,.08)) 92%, transparent);
  color: var(--ff-text, #fff);
  border-radius: 999px;
  min-height: 48px;
  padding: 0 16px;
  font-weight: 800;
  letter-spacing: -.01em;
  cursor: pointer;
  transition:
    transform .18s ease,
    border-color .18s ease,
    background .18s ease,
    box-shadow .18s ease;
}

.ff-donation-presets__btn:hover,
.ff-donation-presets__btn:focus-visible,
.ff-donation-presets__btn.is-active {
  transform: translateY(-1px);
  border-color: color-mix(in srgb, var(--ff-accent, #f97316) 46%, rgba(255,255,255,.22));
  background: color-mix(in srgb, var(--ff-accent, #f97316) 14%, var(--ff-surface-2, rgba(255,255,255,.08)));
  box-shadow: 0 10px 26px rgba(0,0,0,.18);
  outline: none;
}

.ff-donation-presets__btn--feature {
  background: color-mix(in srgb, var(--ff-accent, #f97316) 18%, var(--ff-surface-2, rgba(255,255,255,.08)));
}

.ff-trustStrip {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.ff-trustStrip__item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 38px;
  padding: 0 12px;
  border-radius: 999px;
  border: 1px solid color-mix(in srgb, var(--ff-line, rgba(255,255,255,.10)) 88%, transparent);
  background: color-mix(in srgb, var(--ff-surface-2, rgba(255,255,255,.06)) 94%, transparent);
  font-size: .92rem;
  font-weight: 700;
  color: var(--ff-text, #fff);
}

.ff-sponsorSpotlight__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.ff-sponsorSpotlight__card {
  display: grid;
  gap: 8px;
  text-decoration: none;
  color: inherit;
  padding: 16px;
  border-radius: 20px;
  min-height: 170px;
  border: 1px solid color-mix(in srgb, var(--ff-line, rgba(255,255,255,.12)) 86%, transparent);
  background:
    radial-gradient(circle at top right, rgba(255,255,255,.14), transparent 42%),
    color-mix(in srgb, var(--ff-surface-2, rgba(255,255,255,.08)) 94%, transparent);
  transition:
    transform .18s ease,
    border-color .18s ease,
    box-shadow .18s ease;
}

.ff-sponsorSpotlight__card:hover,
.ff-sponsorSpotlight__card:focus-visible {
  transform: translateY(-2px);
  border-color: color-mix(in srgb, var(--ff-accent, #f97316) 44%, rgba(255,255,255,.22));
  box-shadow: 0 14px 34px rgba(0,0,0,.20);
  outline: none;
}

.ff-sponsorSpotlight__badge {
  display: inline-flex;
  width: fit-content;
  padding: 6px 10px;
  border-radius: 999px;
  font-size: .78rem;
  font-weight: 800;
  border: 1px solid rgba(255,255,255,.10);
  background: rgba(255,255,255,.06);
}

.ff-sponsorSpotlight__title {
  font-size: 1.05rem;
  line-height: 1.2;
}

.ff-sponsorSpotlight__amount {
  font-size: 1.35rem;
  font-weight: 900;
  letter-spacing: -.02em;
}

.ff-sponsorSpotlight__perk {
  font-size: .94rem;
  color: var(--ff-text-muted, rgba(255,255,255,.74));
}

.ff-sponsorSpotlight__card--gold {
  background:
    radial-gradient(circle at top right, rgba(255,210,84,.20), transparent 42%),
    color-mix(in srgb, var(--ff-surface-2, rgba(255,255,255,.08)) 94%, transparent);
}

.ff-sponsorSpotlight__card--silver {
  background:
    radial-gradient(circle at top right, rgba(205,214,224,.18), transparent 42%),
    color-mix(in srgb, var(--ff-surface-2, rgba(255,255,255,.08)) 94%, transparent);
}

.ff-sponsorSpotlight__card--community {
  background:
    radial-gradient(circle at top right, rgba(249,115,22,.18), transparent 42%),
    color-mix(in srgb, var(--ff-surface-2, rgba(255,255,255,.08)) 94%, transparent);
}

.ff-sheet--checkout .ff-sheet__panel--flagship {
  transition:
    transform .22s cubic-bezier(.2,.9,.22,1),
    opacity .22s ease;
  will-change: transform, opacity;
}

.ff-sheet--checkout[data-open="true"] .ff-sheet__panel--flagship,
.ff-sheet--checkout[aria-hidden="false"] .ff-sheet__panel--flagship {
  box-shadow:
    0 28px 90px rgba(0,0,0,.44),
    inset 0 1px 0 rgba(255,255,255,.06);
}

.ff-checkoutShell {
  border: 1px solid color-mix(in srgb, var(--ff-line, rgba(255,255,255,.10)) 86%, transparent);
  backdrop-filter: blur(18px);
}

.ff-checkoutCard--conversion + .ff-checkoutCard--amount {
  margin-top: 14px;
}

@media (max-width: 920px) {
  .ff-sponsorSpotlight__grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .ff-donation-presets {
    grid-template-columns: 1fr 1fr;
  }

  .ff-trustStrip__item {
    width: 100%;
    justify-content: center;
  }

  .ff-checkoutCard--conversion {
    padding: 16px;
  }
}
"""
css = append_once(css, "FF_CONVERSION_LAYER_V2", css_block)
write(CSS, css)

# -------------------------------------------------------------------
# 6) JS append
# -------------------------------------------------------------------
js_block = r"""
/* ==========================================================================
   FF_CONVERSION_LAYER_V2
   Conversion polish + preset + sponsor helpers
   ========================================================================== */
(function () {
  "use strict";

  if (window.__FF_CONVERSION_LAYER_V2__) return;
  window.__FF_CONVERSION_LAYER_V2__ = true;

  const doc = document;

  function q(sel, root) {
    return (root || doc).querySelector(sel);
  }

  function qa(sel, root) {
    return Array.from((root || doc).querySelectorAll(sel));
  }

  function fire(el, type) {
    if (!el) return;
    el.dispatchEvent(new Event(type, { bubbles: true }));
  }

  function getAmountInput() {
    return q('[data-ff-amount-input]') || q('#donationAmount');
  }

  function setAmount(value) {
    const input = getAmountInput();
    if (!input) return;
    input.value = String(value);
    fire(input, "input");
    fire(input, "change");
  }

  function markActivePreset(value) {
    qa('[data-ff-amount]').forEach((el) => {
      const v = Number(el.getAttribute('data-ff-amount') || '');
      const active = Number(value) === v;
      el.classList.toggle('is-active', active);
      if (el.classList.contains('ff-donation-presets__btn')) {
        el.setAttribute('aria-pressed', active ? 'true' : 'false');
      }
    });
  }

  function preloadSponsorChoice(link) {
    const sponsorAmount = q('input[data-ff-sponsor-amount][name="sponsor_amount"]');
    const sponsorTierLabel = link.getAttribute('data-ff-sponsor-tier-choice') || '';
    const sponsorAmountValue = link.getAttribute('data-ff-sponsor-amount-value') || '';

    if (sponsorAmount && sponsorAmountValue) {
      sponsorAmount.value = sponsorAmountValue;
      fire(sponsorAmount, "input");
      fire(sponsorAmount, "change");
    }

    const sponsorSelected = q('[data-ff-sponsor-tier-selected]');
    if (sponsorSelected && sponsorTierLabel) {
      sponsorSelected.textContent = sponsorTierLabel;
    }
  }

  doc.addEventListener('click', function (event) {
    const amountEl = event.target.closest('[data-ff-amount]');
    if (amountEl) {
      const raw = amountEl.getAttribute('data-ff-amount');
      const value = Number(raw || '');
      if (Number.isFinite(value) && value > 0) {
        setAmount(value);
        markActivePreset(value);
      }
    }

    const sponsorChoice = event.target.closest('[data-ff-sponsor-tier-choice]');
    if (sponsorChoice) {
      preloadSponsorChoice(sponsorChoice);
    }

    const shareBtn = event.target.closest('[data-ff-success-share]');
    if (shareBtn) {
      const shareUrl =
        document.body?.getAttribute('data-ff-share-url') ||
        document.querySelector('meta[name="ff-share-url"]')?.getAttribute('content') ||
        window.location.href;

      if (navigator.share) {
        navigator.share({
          title: document.title,
          text: 'Support this fundraiser',
          url: shareUrl
        }).catch(() => {});
      } else if (navigator.clipboard?.writeText) {
        navigator.clipboard.writeText(shareUrl).catch(() => {});
      }
    }

    const copyBtn = event.target.closest('[data-ff-success-copy]');
    if (copyBtn) {
      const shareUrl =
        document.body?.getAttribute('data-ff-share-url') ||
        document.querySelector('meta[name="ff-share-url"]')?.getAttribute('content') ||
        window.location.href;

      if (navigator.clipboard?.writeText) {
        navigator.clipboard.writeText(shareUrl).then(() => {
          copyBtn.textContent = 'Copied';
          window.setTimeout(() => {
            copyBtn.textContent = 'Copy link';
          }, 1600);
        }).catch(() => {});
      }
    }

    const openCheckout = event.target.closest('[data-ff-open-checkout]');
    if (openCheckout) {
      const raw = openCheckout.getAttribute('data-ff-amount');
      const value = Number(raw || '');
      if (Number.isFinite(value) && value > 0) {
        setAmount(value);
        markActivePreset(value);
      }

      window.setTimeout(() => {
        const input = getAmountInput();
        if (input && !input.value) {
          input.focus({ preventScroll: true });
        }
      }, 180);
    }
  });

  const input = getAmountInput();
  if (input) {
    input.addEventListener('input', function () {
      const value = Number(input.value || '');
      if (Number.isFinite(value) && value > 0) {
        markActivePreset(value);
      } else {
        markActivePreset(NaN);
      }
    });
  }
})();
"""
js = append_once(js, "FF_CONVERSION_LAYER_V2", js_block)
write(JS, js)

print("✅ Conversion Layer V2 applied")
print(f" - Template backup: {TEMPLATE}.bak.{STAMP}")
print(f" - CSS backup:      {CSS}.bak.{STAMP}")
print(f" - JS backup:       {JS}.bak.{STAMP}")
