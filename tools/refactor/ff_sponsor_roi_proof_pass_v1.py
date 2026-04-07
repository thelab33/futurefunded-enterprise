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
    "cta_href": "/platform/onboarding",
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
  </div>
</section>
'''

CSS_BLOCK = r'''
/* ==========================================================================
   FF_PLATFORM_SPONSOR_ROI_PROOF_V1
   Sponsor proof + ROI framing upgrade for package lane
   ========================================================================== */

body[data-ff-platform="true"] .ff-platformSponsorMerch__meta {
  display: grid;
  gap: 0.75rem;
  margin: 0;
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__meta > div {
  display: grid;
  gap: 0.28rem;
  padding: 0.8rem 0.9rem;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__meta dt {
  margin: 0;
  font-size: 0.72rem;
  font-weight: 900;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  opacity: 0.68;
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__meta dd {
  margin: 0;
  font-size: 0.92rem;
  line-height: 1.55;
  opacity: 0.95;
}

body[data-ff-platform="true"] .ff-platformSponsorProof {
  display: grid;
  gap: 1rem;
  margin-top: 0.25rem;
  padding: 1rem;
  border-radius: 24px;
  background:
    linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.025)),
    rgba(7, 11, 20, 0.52);
  border: 1px solid rgba(255,255,255,0.08);
}

body[data-ff-platform="true"] .ff-platformSponsorProof__head {
  display: grid;
  gap: 0.35rem;
}

body[data-ff-platform="true"] .ff-platformSponsorProof__eyebrow {
  margin: 0;
  font-size: 0.72rem;
  font-weight: 900;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  opacity: 0.7;
}

body[data-ff-platform="true"] .ff-platformSponsorProof__title {
  margin: 0;
  font-size: clamp(1.05rem, 1.8vw, 1.35rem);
  line-height: 1.2;
  font-weight: 900;
}

body[data-ff-platform="true"] .ff-platformSponsorProof__grid {
  display: grid;
  gap: 0.9rem;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

body[data-ff-platform="true"] .ff-platformSponsorProof__card {
  display: grid;
  gap: 0.45rem;
  min-height: 100%;
  padding: 1rem;
  border-radius: 18px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
}

body[data-ff-platform="true"] .ff-platformSponsorProof__card h4 {
  margin: 0;
  font-size: 0.98rem;
  font-weight: 900;
}

body[data-ff-platform="true"] .ff-platformSponsorProof__card p {
  margin: 0;
  font-size: 0.93rem;
  line-height: 1.6;
  opacity: 0.92;
}

body[data-ff-platform="true"] .ff-platformSponsorMerch__card.is-featured .ff-platformSponsorMerch__badge {
  opacity: 1;
}

@media (max-width: 980px) {
  body[data-ff-platform="true"] .ff-platformSponsorProof__grid {
    grid-template-columns: 1fr;
  }
}

@media (prefers-color-scheme: light) {
  body[data-ff-platform="true"] .ff-platformSponsorMerch__meta > div,
  body[data-ff-platform="true"] .ff-platformSponsorProof__card {
    background: rgba(15, 23, 42, 0.03);
    border-color: rgba(15, 23, 42, 0.08);
  }

  body[data-ff-platform="true"] .ff-platformSponsorProof {
    background:
      linear-gradient(180deg, rgba(255,255,255,0.92), rgba(248,250,252,0.94)),
      #ffffff;
    border-color: rgba(15, 23, 42, 0.08);
    box-shadow: 0 16px 34px rgba(15, 23, 42, 0.08);
  }
}
'''

PARTIAL.write_text(PARTIAL_TEXT, encoding="utf-8")
print("changed: sponsor merchandising partial upgraded to ROI/proof version")

css_text = CSS.read_text(encoding="utf-8") if CSS.exists() else ""
if "FF_PLATFORM_SPONSOR_ROI_PROOF_V1" not in css_text:
    if css_text and not css_text.endswith("\n"):
        css_text += "\n"
    css_text += "\n" + CSS_BLOCK.strip() + "\n"
    CSS.write_text(css_text, encoding="utf-8")
    print("changed: platform-pages.css roi/proof block appended")
else:
    print("skip: roi/proof css block already present")

print("done.")
