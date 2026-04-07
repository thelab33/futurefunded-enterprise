from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"

PARTIAL = ROOT / "apps/web/app/templates/platform/partials/_sponsor_packages_merchandising.html"
CSS = ROOT / "apps/web/app/static/css/platform-pages.css"
TARGETS = [
    ROOT / "apps/web/app/templates/platform/pages/pricing.html",
    ROOT / "apps/web/app/templates/platform/pages/demo.html",
]

PARTIAL_TEXT = r'''{% set sponsor_packages = [
  {
    "name": "Community Sponsor",
    "price": "$500",
    "badge": "Entry visibility",
    "best_for": "Best for local shops, solo operators, and family businesses",
    "benefits": [
      "Logo placement on campaign sponsor wall",
      "Thank-you mention in sponsor rotation",
      "Visibility on the live fundraiser surface",
      "Good first step for local community support"
    ],
    "cta_href": "/platform/demo",
    "cta_label": "See sponsor demo"
  },
  {
    "name": "Featured Partner",
    "price": "$1,500",
    "badge": "Best value",
    "best_for": "Best for growth-minded local brands that want more repeat visibility",
    "benefits": [
      "Priority logo placement and featured sponsor treatment",
      "Higher visibility across sponsor panels and proof sections",
      "Better positioning for event-night and campaign traffic",
      "Strong option for businesses wanting meaningful local presence"
    ],
    "cta_href": "/platform/pricing",
    "cta_label": "Review package"
  },
  {
    "name": "Founding Partner",
    "price": "$3,000+",
    "badge": "Premium lane",
    "best_for": "Best for flagship partners, clinics, realtors, restaurants, and community anchors",
    "benefits": [
      "Top-tier sponsor visibility and premium placement",
      "Founder-level positioning across the fundraising story",
      "Flexible white-glove package conversation",
      "Invoice-friendly setup for larger supporters"
    ],
    "cta_href": "/platform/onboarding",
    "cta_label": "Start sponsor setup"
  }
] %}

<section class="ff-platformSponsorMerch" aria-labelledby="ffSponsorPackagesTitle">
  <div class="ff-platformSponsorMerch__inner">
    <div class="ff-platformSponsorMerch__intro">
      <p class="ff-platformSponsorMerch__eyebrow">Sponsor packages</p>
      <h2 id="ffSponsorPackagesTitle" class="ff-platformSponsorMerch__title">
        Turn sponsor interest into a package a founder can actually sell
      </h2>
      <p class="ff-platformSponsorMerch__body">
        FutureFunded is stronger when sponsorship feels productized, not improvised.
        These package lanes help founders explain value clearly, price it confidently,
        and move local businesses from “maybe” to “send me the link.”
      </p>

      <div class="ff-platformSponsorMerch__chips" aria-label="Package use cases">
        <span class="ff-platformSponsorMerch__chip">Local business visibility</span>
        <span class="ff-platformSponsorMerch__chip">Invoice-friendly sponsorships</span>
        <span class="ff-platformSponsorMerch__chip">Premium partner positioning</span>
      </div>
    </div>

    <div class="ff-platformSponsorMerch__grid">
      {% for pkg in sponsor_packages %}
      <article class="ff-platformSponsorMerch__card{% if loop.index == 2 %} is-featured{% endif %}">
        <div class="ff-platformSponsorMerch__cardTop">
          <p class="ff-platformSponsorMerch__badge">{{ pkg.badge }}</p>
          <h3 class="ff-platformSponsorMerch__name">{{ pkg.name }}</h3>
          <p class="ff-platformSponsorMerch__price">{{ pkg.price }}</p>
          <p class="ff-platformSponsorMerch__bestFor">{{ pkg.best_for }}</p>
        </div>

        <ul class="ff-platformSponsorMerch__list" aria-label="{{ pkg.name }} benefits">
          {% for benefit in pkg.benefits %}
          <li>{{ benefit }}</li>
          {% endfor %}
        </ul>

        <div class="ff-platformSponsorMerch__actions">
          <a class="ff-platformSponsorMerch__button ff-platformSponsorMerch__button--primary" href="{{ pkg.cta_href }}">
            {{ pkg.cta_label }}
          </a>
          <a class="ff-platformSponsorMerch__button ff-platformSponsorMerch__button--secondary" href="/platform/demo">
            Open guided demo
          </a>
        </div>
      </article>
      {% endfor %}
    </div>
  </div>
</section>
'''

CSS_BLOCK = r'''
/* ==========================================================================
   FF_PLATFORM_SPONSOR_MERCHANDISING_V2
   Additive sponsor/package merchandising lane for pricing + demo pages
   ========================================================================== */

body[data-ff-platform="true"] .ff-platformSponsorMerch {
  margin-top: clamp(2.5rem, 5vw, 4.5rem);
  padding: clamp(1.25rem, 2vw, 1.75rem);
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__inner {
  display: grid;
  gap: clamp(1.125rem, 2vw, 1.75rem);
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 28px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.03)),
    rgba(10, 15, 26, 0.62);
  box-shadow:
    0 28px 64px rgba(0, 0, 0, 0.28),
    inset 0 1px 0 rgba(255, 255, 255, 0.06);
  padding: clamp(1.25rem, 3vw, 2rem);
  backdrop-filter: blur(14px);
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__intro {
  display: grid;
  gap: 0.75rem;
  max-width: 72ch;
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__eyebrow {
  margin: 0;
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  opacity: 0.72;
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__title {
  margin: 0;
  font-size: clamp(1.5rem, 2.6vw, 2.3rem);
  line-height: 1.08;
  font-weight: 900;
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__body {
  margin: 0;
  font-size: 1rem;
  line-height: 1.7;
  opacity: 0.9;
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.625rem;
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__chip {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 0.55rem 0.85rem;
  font-size: 0.8rem;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__card {
  display: grid;
  gap: 1rem;
  min-height: 100%;
  border-radius: 24px;
  padding: 1.1rem;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.07), rgba(255, 255, 255, 0.03)),
    rgba(8, 12, 22, 0.72);
  border: 1px solid rgba(255, 255, 255, 0.09);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__card.is-featured {
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.18);
  box-shadow:
    0 16px 34px rgba(0, 0, 0, 0.24),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__cardTop {
  display: grid;
  gap: 0.45rem;
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__badge {
  margin: 0;
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  opacity: 0.74;
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__name {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 900;
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__price {
  margin: 0;
  font-size: 1.55rem;
  font-weight: 950;
  line-height: 1;
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__bestFor {
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.55;
  opacity: 0.88;
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__list {
  margin: 0;
  padding-left: 1.15rem;
  display: grid;
  gap: 0.55rem;
  line-height: 1.55;
  opacity: 0.94;
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__actions {
  display: grid;
  gap: 0.65rem;
  margin-top: auto;
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 46px;
  border-radius: 14px;
  text-decoration: none;
  font-weight: 800;
  transition: transform 140ms ease, opacity 140ms ease, border-color 140ms ease;
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__button:hover {
  transform: translateY(-1px);
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__button--primary {
  color: inherit;
  background: linear-gradient(180deg, rgba(255,255,255,0.16), rgba(255,255,255,0.08));
  border: 1px solid rgba(255,255,255,0.16);
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__button--secondary {
  color: inherit;
  background: transparent;
  border: 1px solid rgba(255,255,255,0.12);
}

@media (max-width: 980px) {
  body[data-ff-platform="true"] .ff-platformSponsorMerch__grid {
    grid-template-columns: 1fr;
  }

  body[data-ff-platform="true"] .ff-platformSponsorMerch__card.is-featured {
    transform: none;
  }
}

@media (prefers-color-scheme: light) {
  body[data-ff-platform="true"] .ff-platformSponsorMerch__inner {
    background:
      linear-gradient(180deg, rgba(255,255,255,0.9), rgba(249,250,252,0.92)),
      #ffffff;
    border-color: rgba(15, 23, 42, 0.08);
    box-shadow:
      0 20px 50px rgba(15, 23, 42, 0.10),
      inset 0 1px 0 rgba(255,255,255,0.8);
  }

  body[data-ff-platform="true"] .ff-platformSponsorMerch__card {
    background:
      linear-gradient(180deg, rgba(255,255,255,0.96), rgba(247,248,251,0.95)),
      #ffffff;
    border-color: rgba(15, 23, 42, 0.08);
    box-shadow: 0 10px 26px rgba(15, 23, 42, 0.08);
  }

  body[data-ff-platform="true"] .ff-platformSponsorMerch__chip,
  body[data-ff-platform="true"] .ff-platformSponsorMerch__button--primary {
    border-color: rgba(15, 23, 42, 0.10);
    background: rgba(15, 23, 42, 0.04);
  }

  body[data-ff-platform="true"] .ff-platformSponsorMerch__button--secondary {
    border-color: rgba(15, 23, 42, 0.10);
  }
}
'''

def backup(path: Path) -> None:
    if path.exists():
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        shutil.copy2(path, path.with_name(f"{path.name}.{ts}.bak"))

PARTIAL.parent.mkdir(parents=True, exist_ok=True)
PARTIAL.write_text(PARTIAL_TEXT, encoding="utf-8")
print(f"wrote: {PARTIAL}")

backup(CSS)
css_text = CSS.read_text(encoding="utf-8") if CSS.exists() else ""
if "FF_PLATFORM_SPONSOR_MERCHANDISING_V2" not in css_text:
    if css_text and not css_text.endswith("\n"):
        css_text += "\n"
    css_text += "\n" + CSS_BLOCK.strip() + "\n"
    CSS.write_text(css_text, encoding="utf-8")
    print("changed: platform-pages.css sponsor merchandising block")
else:
    print("skip: css block already present")

include_line = '{% include "platform/partials/_sponsor_packages_merchandising.html" %}'

for target in TARGETS:
    if not target.exists():
        print(f"SKIP: missing target {target}")
        continue

    backup(target)
    text = target.read_text(encoding="utf-8")

    if include_line in text:
        print(f"skip: include already present in {target.name}")
        continue

    if "</main>" in text:
        replacement = "\n  " + include_line + "\n</main>"
        text = text.replace("</main>", replacement, 1)
        target.write_text(text, encoding="utf-8")
        print(f"changed: inserted sponsor merchandising include into {target.name}")
    elif "{% endblock %}" in text:
        replacement = "\n" + include_line + "\n{% endblock %}"
        text = text.replace("{% endblock %}", replacement, 1)
        target.write_text(text, encoding="utf-8")
        print(f"changed: inserted sponsor merchandising include before endblock in {target.name}")
    else:
        print(f"MISS: no insertion anchor in {target.name}")

print("done.")
