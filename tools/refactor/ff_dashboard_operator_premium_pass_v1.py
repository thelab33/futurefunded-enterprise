from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"

PARTIAL = ROOT / "apps/web/app/templates/platform/partials/_dashboard_operator_premium_strip.html"
CSS = ROOT / "apps/web/app/static/css/platform-pages.css"
TARGET = ROOT / "apps/web/app/templates/platform/pages/dashboard.html"

if not TARGET.exists():
    raise SystemExit(f"Missing dashboard template: {TARGET}")

def backup(path: Path) -> None:
    if path.exists():
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        shutil.copy2(path, path.with_name(f"{path.name}.{ts}.bak"))

backup(TARGET)
backup(CSS)

PARTIAL_TEXT = r'''<section class="ff-operatorPremium" aria-labelledby="ffOperatorPremiumTitle">
  <div class="ff-operatorPremium__inner">
    <div class="ff-operatorPremium__intro">
      <p class="ff-operatorPremium__eyebrow">Operator control</p>
      <h2 id="ffOperatorPremiumTitle" class="ff-operatorPremium__title">
        Run fundraising, sponsors, and launch operations from one cleaner command surface
      </h2>
      <p class="ff-operatorPremium__body">
        FutureFunded works best when founders can move from launch into confident day-to-day operation.
        This dashboard is where campaign progress, sponsor momentum, and rollout activity should feel visible,
        organized, and premium — not scattered across five tools and a group chat.
      </p>
    </div>

    <div class="ff-operatorPremium__grid" aria-label="Operator management areas">
      <article class="ff-operatorPremium__card">
        <p class="ff-operatorPremium__kicker">Fundraising</p>
        <h3>Track momentum clearly</h3>
        <p>
          Keep raised totals, campaign progress, and active momentum visible so founders can make
          quicker decisions without hunting through clutter.
        </p>
      </article>

      <article class="ff-operatorPremium__card">
        <p class="ff-operatorPremium__kicker">Sponsors</p>
        <h3>Manage sponsor visibility</h3>
        <p>
          Treat sponsor support like a real revenue lane with cleaner package awareness,
          placement confidence, and follow-through.
        </p>
      </article>

      <article class="ff-operatorPremium__card">
        <p class="ff-operatorPremium__kicker">Operations</p>
        <h3>Launch with less chaos</h3>
        <p>
          Give operators one place to understand what is live, what needs attention,
          and what the next action should be.
        </p>
      </article>
    </div>

    <div class="ff-operatorPremium__rail">
      <div class="ff-operatorPremium__railMain">
        <p class="ff-operatorPremium__railEyebrow">Operator checklist</p>
        <h3 class="ff-operatorPremium__railTitle">What a founder should feel after launch</h3>
        <ul class="ff-operatorPremium__list">
          <li>Campaign is live and easy to understand</li>
          <li>Sponsor packages are visible and sellable</li>
          <li>Core performance and momentum are easy to check</li>
          <li>The next operator action is obvious</li>
        </ul>
      </div>

      <div class="ff-operatorPremium__railActions">
        <a class="ff-operatorPremium__button ff-operatorPremium__button--secondary" href="/platform/demo">
          Open guided demo
        </a>
        <a class="ff-operatorPremium__button ff-operatorPremium__button--primary" href="/platform/pricing">
          Review growth plan
        </a>
      </div>
    </div>
  </div>
</section>
'''

CSS_BLOCK = r'''
/* ==========================================================================
   FF_PLATFORM_DASHBOARD_OPERATOR_PREMIUM_V1
   Operator/dashboard premium framing layer
   ========================================================================== */

body[data-ff-platform="true"] .ff-operatorPremium {
  margin-top: clamp(2.5rem, 5vw, 4.5rem);
  padding: clamp(1.25rem, 2vw, 1.75rem);
}

body[data-ff-platform="true"] .ff-operatorPremium__inner {
  display: grid;
  gap: clamp(1.125rem, 2vw, 1.75rem);
  padding: clamp(1.25rem, 3vw, 2rem);
  border-radius: 28px;
  border: 1px solid rgba(255,255,255,0.09);
  background:
    linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03)),
    rgba(10, 14, 24, 0.62);
  box-shadow:
    0 24px 54px rgba(0,0,0,0.22),
    inset 0 1px 0 rgba(255,255,255,0.05);
  backdrop-filter: blur(14px);
}

body[data-ff-platform="true"] .ff-operatorPremium__intro {
  display: grid;
  gap: 0.7rem;
  max-width: 72ch;
}

body[data-ff-platform="true"] .ff-operatorPremium__eyebrow,
body[data-ff-platform="true"] .ff-operatorPremium__railEyebrow,
body[data-ff-platform="true"] .ff-operatorPremium__kicker {
  margin: 0;
  font-size: 0.74rem;
  font-weight: 900;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  opacity: 0.72;
}

body[data-ff-platform="true"] .ff-operatorPremium__title {
  margin: 0;
  font-size: clamp(1.45rem, 2.5vw, 2.15rem);
  line-height: 1.08;
  font-weight: 950;
}

body[data-ff-platform="true"] .ff-operatorPremium__body {
  margin: 0;
  font-size: 1rem;
  line-height: 1.7;
  opacity: 0.92;
}

body[data-ff-platform="true"] .ff-operatorPremium__grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

body[data-ff-platform="true"] .ff-operatorPremium__card {
  display: grid;
  gap: 0.55rem;
  min-height: 100%;
  padding: 1rem;
  border-radius: 20px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
}

body[data-ff-platform="true"] .ff-operatorPremium__card h3,
body[data-ff-platform="true"] .ff-operatorPremium__railTitle {
  margin: 0;
  font-size: 1.02rem;
  line-height: 1.2;
  font-weight: 900;
}

body[data-ff-platform="true"] .ff-operatorPremium__card p {
  margin: 0;
  font-size: 0.94rem;
  line-height: 1.6;
  opacity: 0.92;
}

body[data-ff-platform="true"] .ff-operatorPremium__rail {
  display: grid;
  gap: 1rem;
  grid-template-columns: minmax(0, 1.25fr) minmax(250px, 0.75fr);
  align-items: center;
  padding: 1rem;
  border-radius: 22px;
  background: rgba(255,255,255,0.035);
  border: 1px solid rgba(255,255,255,0.08);
}

body[data-ff-platform="true"] .ff-operatorPremium__railMain {
  display: grid;
  gap: 0.55rem;
}

body[data-ff-platform="true"] .ff-operatorPremium__list {
  margin: 0;
  padding-left: 1.2rem;
  display: grid;
  gap: 0.55rem;
  line-height: 1.6;
  opacity: 0.92;
}

body[data-ff-platform="true"] .ff-operatorPremium__railActions {
  display: grid;
  gap: 0.75rem;
}

body[data-ff-platform="true"] .ff-operatorPremium__button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  border-radius: 15px;
  text-decoration: none;
  font-weight: 900;
  transition: transform 140ms ease, opacity 140ms ease, border-color 140ms ease;
}

body[data-ff-platform="true"] .ff-operatorPremium__button:hover {
  transform: translateY(-1px);
}

body[data-ff-platform="true"] .ff-operatorPremium__button--primary {
  color: inherit;
  background: linear-gradient(180deg, rgba(255,255,255,0.18), rgba(255,255,255,0.09));
  border: 1px solid rgba(255,255,255,0.16);
}

body[data-ff-platform="true"] .ff-operatorPremium__button--secondary {
  color: inherit;
  background: transparent;
  border: 1px solid rgba(255,255,255,0.12);
}

@media (max-width: 1100px) {
  body[data-ff-platform="true"] .ff-operatorPremium__grid {
    grid-template-columns: 1fr;
  }

  body[data-ff-platform="true"] .ff-operatorPremium__rail {
    grid-template-columns: 1fr;
  }
}

@media (prefers-color-scheme: light) {
  body[data-ff-platform="true"] .ff-operatorPremium__inner {
    background:
      linear-gradient(180deg, rgba(255,255,255,0.94), rgba(248,250,252,0.96)),
      #ffffff;
    border-color: rgba(15,23,42,0.08);
    box-shadow:
      0 20px 48px rgba(15,23,42,0.08),
      inset 0 1px 0 rgba(255,255,255,0.7);
  }

  body[data-ff-platform="true"] .ff-operatorPremium__card,
  body[data-ff-platform="true"] .ff-operatorPremium__rail {
    background: rgba(15,23,42,0.03);
    border-color: rgba(15,23,42,0.08);
  }

  body[data-ff-platform="true"] .ff-operatorPremium__button--primary,
  body[data-ff-platform="true"] .ff-operatorPremium__button--secondary {
    border-color: rgba(15,23,42,0.10);
  }

  body[data-ff-platform="true"] .ff-operatorPremium__button--primary {
    background: rgba(15,23,42,0.05);
  }
}
'''

include_line = '{% include "platform/partials/_dashboard_operator_premium_strip.html" %}'

PARTIAL.parent.mkdir(parents=True, exist_ok=True)
PARTIAL.write_text(PARTIAL_TEXT, encoding="utf-8")
print(f"wrote: {PARTIAL}")

css_text = CSS.read_text(encoding="utf-8") if CSS.exists() else ""
if "FF_PLATFORM_DASHBOARD_OPERATOR_PREMIUM_V1" not in css_text:
    if css_text and not css_text.endswith("\n"):
        css_text += "\n"
    css_text += "\n" + CSS_BLOCK.strip() + "\n"
    CSS.write_text(css_text, encoding="utf-8")
    print("changed: platform-pages.css dashboard operator premium block")
else:
    print("skip: dashboard operator premium css block already present")

text = TARGET.read_text(encoding="utf-8")
if include_line in text:
    print("skip: dashboard premium include already present")
elif "</main>" in text:
    replacement = "\n  " + include_line + "\n</main>"
    text = text.replace("</main>", replacement, 1)
    TARGET.write_text(text, encoding="utf-8")
    print("changed: inserted dashboard premium include before </main>")
elif "{% endblock %}" in text:
    replacement = "\n" + include_line + "\n{% endblock %}"
    text = text.replace("{% endblock %}", replacement, 1)
    TARGET.write_text(text, encoding="utf-8")
    print("changed: inserted dashboard premium include before endblock")
else:
    print("MISS: no insertion anchor in dashboard.html")

print("done.")
