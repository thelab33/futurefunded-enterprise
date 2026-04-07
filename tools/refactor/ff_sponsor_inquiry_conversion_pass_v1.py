from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"

PARTIAL = ROOT / "apps/web/app/templates/platform/partials/_sponsor_packages_merchandising.html"
CSS = ROOT / "apps/web/app/static/css/platform-pages.css"

if not PARTIAL.exists():
    raise SystemExit(f"Missing partial: {PARTIAL}")

def backup(path: Path) -> None:
    if path.exists():
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        shutil.copy2(path, path.with_name(f"{path.name}.{ts}.bak"))

backup(PARTIAL)
backup(CSS)

PARTIAL_TEXT = r'''{% set sponsor_packages = [
  {
    "name": "Community Sponsor",
    "price": "$500",
    "badge": "Starter lane",
    "best_for": "Best for local shops, family businesses, solo operators, and community supporters",
    "visibility": "Sponsor wall presence + dependable entry visibility",
    "proof": "A cleaner option than a one-time thank-you post or a casual mention.",
    "fit_examples": "Coffee shops, salons, small retail, family services, training studios",
    "benefits": [
      "Logo placement on the live fundraiser sponsor wall",
      "Supporter-facing visibility on a premium fundraising surface",
      "Simple first-step package for businesses wanting community presence",
      "Easy lane for local brands that want to start supporting quickly"
    ],
    "cta_href": "/platform/demo",
    "cta_label": "See sponsor demo"
  },
  {
    "name": "Featured Partner",
    "price": "$1,500",
    "badge": "Most popular",
    "best_for": "Best for local brands that want stronger repeat visibility and clearer premium positioning",
    "visibility": "Priority placement + featured treatment across sponsor moments",
    "proof": "Strong middle lane for sponsors who want more than a donation receipt and less than a custom enterprise-style deal.",
    "fit_examples": "Realtors, orthodontists, clinics, restaurants, gyms, law offices",
    "benefits": [
      "Priority logo placement and featured sponsor treatment",
      "Higher visibility across proof areas, package sections, and sponsor panels",
      "More premium positioning for event traffic, families, and supporters",
      "Best value lane for businesses that want a meaningful local presence"
    ],
    "cta_href": "/platform/pricing",
    "cta_label": "Review package"
  },
  {
    "name": "Founding Partner",
    "price": "$3,000+",
    "badge": "Premium lane",
    "best_for": "Best for flagship local businesses that want top-tier visibility and a white-glove sponsor conversation",
    "visibility": "Top-tier visibility + founder-level partner framing",
    "proof": "Designed for anchor sponsors who want to look serious, supportive, and visibly aligned with the program.",
    "fit_examples": "Flagship restaurants, medical groups, real estate teams, regional businesses, lead community partners",
    "benefits": [
      "Top-tier sponsor visibility and premium placement",
      "Founder-level positioning across the fundraising story",
      "Flexible white-glove package conversation and custom support",
      "Invoice-friendly setup for larger supporters and serious local partners"
    ],
    "cta_href": "/platform/onboarding?intent=sponsor",
    "cta_label": "Start sponsor setup"
  }
] %}

<section class="ff-platformSponsorMerch" aria-labelledby="ffSponsorPackagesTitle">
  <div class="ff-platformSponsorMerch__inner">
    <div class="ff-platformSponsorMerch__intro">
      <p class="ff-platformSponsorMerch__eyebrow">Sponsor packages</p>
      <h2 id="ffSponsorPackagesTitle" class="ff-platformSponsorMerch__title">
        Package sponsor support like a real premium offer
      </h2>
      <p class="ff-platformSponsorMerch__body">
        FutureFunded helps founders explain sponsorship with more confidence.
        Instead of vague support asks, these lanes give local businesses a cleaner
        reason to say yes: better presentation, better visibility framing, and a
        more premium community-facing surface.
      </p>

      <div class="ff-platformSponsorMerch__chips" aria-label="Sponsor package highlights">
        <span class="ff-platformSponsorMerch__chip">Seen by families and supporters</span>
        <span class="ff-platformSponsorMerch__chip">Premium sponsor placement</span>
        <span class="ff-platformSponsorMerch__chip">Invoice-friendly larger deals</span>
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

        <dl class="ff-platformSponsorMerch__meta">
          <div>
            <dt>Visibility</dt>
            <dd>{{ pkg.visibility }}</dd>
          </div>
          <div>
            <dt>Why it sells</dt>
            <dd>{{ pkg.proof }}</dd>
          </div>
          <div>
            <dt>Best-fit examples</dt>
            <dd>{{ pkg.fit_examples }}</dd>
          </div>
        </dl>

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

    <div class="ff-platformSponsorProof" aria-labelledby="ffSponsorProofTitle">
      <div class="ff-platformSponsorProof__head">
        <p class="ff-platformSponsorProof__eyebrow">Why sponsors say yes</p>
        <h3 id="ffSponsorProofTitle" class="ff-platformSponsorProof__title">
          Better than a one-off shoutout. Cleaner than an improvised ask.
        </h3>
      </div>

      <div class="ff-platformSponsorProof__grid">
        <article class="ff-platformSponsorProof__card">
          <h4>Premium visibility</h4>
          <p>
            Sponsors are positioned on a cleaner public fundraising surface that families,
            supporters, and local visitors actually see.
          </p>
        </article>

        <article class="ff-platformSponsorProof__card">
          <h4>Clear package framing</h4>
          <p>
            Businesses understand what they are saying yes to faster when sponsorship is
            packaged into simple, named lanes with visible value.
          </p>
        </article>

        <article class="ff-platformSponsorProof__card">
          <h4>Stronger close path</h4>
          <p>
            Larger supporters can move into invoice-friendly and white-glove conversations
            without the founder having to improvise everything from scratch.
          </p>
        </article>
      </div>
    </div>

    <div class="ff-platformSponsorConvert" aria-labelledby="ffSponsorConvertTitle">
      <div class="ff-platformSponsorConvert__main">
        <div class="ff-platformSponsorConvert__content">
          <p class="ff-platformSponsorConvert__eyebrow">Sponsor inquiry path</p>
          <h3 id="ffSponsorConvertTitle" class="ff-platformSponsorConvert__title">
            Ready to move forward with a sponsor package?
          </h3>
          <p class="ff-platformSponsorConvert__body">
            Start with a package review, request a sponsor packet, or open a guided
            setup path for larger partnerships. This keeps the next step clear for
            both founders and local businesses.
          </p>

          <div class="ff-platformSponsorConvert__chips" aria-label="Sponsor inquiry reassurances">
            <span class="ff-platformSponsorConvert__chip">Custom packages available</span>
            <span class="ff-platformSponsorConvert__chip">Invoice-friendly setup</span>
            <span class="ff-platformSponsorConvert__chip">White-glove support for larger partners</span>
          </div>
        </div>

        <div class="ff-platformSponsorConvert__actions">
          <a class="ff-platformSponsorConvert__button ff-platformSponsorConvert__button--primary" href="/platform/onboarding?intent=sponsor">
            Become a sponsor
          </a>
          <a class="ff-platformSponsorConvert__button ff-platformSponsorConvert__button--secondary" href="/platform/demo?sponsor_packet=1">
            Request sponsor packet
          </a>
        </div>
      </div>

      <div class="ff-platformSponsorConvert__footer">
        <p>
          Best for founders who want a cleaner sponsor close, and for businesses that want
          a more professional path than a casual DM or one-off ask.
        </p>
      </div>
    </div>
  </div>
</section>
'''

CSS_BLOCK = r'''
/* ==========================================================================
   FF_PLATFORM_SPONSOR_INQUIRY_CONVERSION_V1
   Sponsor close-path / inquiry conversion layer
   ========================================================================== */

body[data-ff-platform="true"] .ff-platformSponsorConvert {
  display: grid;
  gap: 1rem;
  margin-top: 0.35rem;
  padding: 1rem;
  border-radius: 24px;
  background:
    linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03)),
    rgba(9, 14, 24, 0.58);
  border: 1px solid rgba(255,255,255,0.09);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.05),
    0 16px 32px rgba(0,0,0,0.16);
}

body[data-ff-platform="true"] .ff-platformSponsorConvert__main {
  display: grid;
  gap: 1rem;
  grid-template-columns: minmax(0, 1.3fr) minmax(260px, 0.7fr);
  align-items: center;
}

body[data-ff-platform="true"] .ff-platformSponsorConvert__content {
  display: grid;
  gap: 0.7rem;
}

body[data-ff-platform="true"] .ff-platformSponsorConvert__eyebrow {
  margin: 0;
  font-size: 0.72rem;
  font-weight: 900;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  opacity: 0.72;
}

body[data-ff-platform="true"] .ff-platformSponsorConvert__title {
  margin: 0;
  font-size: clamp(1.1rem, 2vw, 1.5rem);
  line-height: 1.16;
  font-weight: 900;
}

body[data-ff-platform="true"] .ff-platformSponsorConvert__body {
  margin: 0;
  font-size: 0.98rem;
  line-height: 1.65;
  opacity: 0.92;
  max-width: 62ch;
}

body[data-ff-platform="true"] .ff-platformSponsorConvert__chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

body[data-ff-platform="true"] .ff-platformSponsorConvert__chip {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 0.55rem 0.82rem;
  font-size: 0.8rem;
  font-weight: 800;
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.11);
}

body[data-ff-platform="true"] .ff-platformSponsorConvert__actions {
  display: grid;
  gap: 0.75rem;
}

body[data-ff-platform="true"] .ff-platformSponsorConvert__button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  border-radius: 15px;
  text-decoration: none;
  font-weight: 900;
  transition: transform 140ms ease, border-color 140ms ease, opacity 140ms ease;
}

body[data-ff-platform="true"] .ff-platformSponsorConvert__button:hover {
  transform: translateY(-1px);
}

body[data-ff-platform="true"] .ff-platformSponsorConvert__button--primary {
  color: inherit;
  background: linear-gradient(180deg, rgba(255,255,255,0.18), rgba(255,255,255,0.09));
  border: 1px solid rgba(255,255,255,0.16);
}

body[data-ff-platform="true"] .ff-platformSponsorConvert__button--secondary {
  color: inherit;
  background: transparent;
  border: 1px solid rgba(255,255,255,0.12);
}

body[data-ff-platform="true"] .ff-platformSponsorConvert__footer {
  padding-top: 0.15rem;
  border-top: 1px solid rgba(255,255,255,0.08);
}

body[data-ff-platform="true"] .ff-platformSponsorConvert__footer p {
  margin: 0;
  font-size: 0.92rem;
  line-height: 1.6;
  opacity: 0.88;
}

@media (max-width: 980px) {
  body[data-ff-platform="true"] .ff-platformSponsorConvert__main {
    grid-template-columns: 1fr;
  }
}

@media (prefers-color-scheme: light) {
  body[data-ff-platform="true"] .ff-platformSponsorConvert {
    background:
      linear-gradient(180deg, rgba(255,255,255,0.94), rgba(248,250,252,0.96)),
      #ffffff;
    border-color: rgba(15, 23, 42, 0.08);
    box-shadow: 0 18px 34px rgba(15, 23, 42, 0.08);
  }

  body[data-ff-platform="true"] .ff-platformSponsorConvert__chip {
    background: rgba(15,23,42,0.04);
    border-color: rgba(15,23,42,0.08);
  }

  body[data-ff-platform="true"] .ff-platformSponsorConvert__button--primary,
  body[data-ff-platform="true"] .ff-platformSponsorConvert__button--secondary {
    border-color: rgba(15,23,42,0.10);
  }

  body[data-ff-platform="true"] .ff-platformSponsorConvert__button--primary {
    background: rgba(15,23,42,0.05);
  }

  body[data-ff-platform="true"] .ff-platformSponsorConvert__footer {
    border-top-color: rgba(15,23,42,0.08);
  }
}
'''

PARTIAL.write_text(PARTIAL_TEXT, encoding="utf-8")
print("changed: sponsor merchandising partial upgraded with inquiry conversion close")

css_text = CSS.read_text(encoding="utf-8") if CSS.exists() else ""
if "FF_PLATFORM_SPONSOR_INQUIRY_CONVERSION_V1" not in css_text:
    if css_text and not css_text.endswith("\n"):
        css_text += "\n"
    css_text += "\n" + CSS_BLOCK.strip() + "\n"
    CSS.write_text(css_text, encoding="utf-8")
    print("changed: platform-pages.css sponsor inquiry conversion block appended")
else:
    print("skip: sponsor inquiry conversion css block already present")

print("done.")
