from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"

PARTIAL = ROOT / "apps/web/app/templates/platform/partials/_founder_demo_flow_strip.html"
CSS = ROOT / "apps/web/app/static/css/platform-pages.css"
TARGETS = [
    ROOT / "apps/web/app/templates/platform/pages/home.html",
    ROOT / "apps/web/app/templates/platform/pages/demo.html",
    ROOT / "apps/web/app/templates/platform/pages/pricing.html",
    ROOT / "apps/web/app/templates/platform/pages/onboarding.html",
]

def backup(path: Path) -> None:
    if path.exists():
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        shutil.copy2(path, path.with_name(f"{path.name}.{ts}.bak"))

PARTIAL_TEXT = r'''<section class="ff-founderFlow" aria-labelledby="ffFounderFlowTitle">
  <div class="ff-founderFlow__inner">
    <div class="ff-founderFlow__intro">
      <p class="ff-founderFlow__eyebrow">Founder flow</p>
      <h2 id="ffFounderFlowTitle" class="ff-founderFlow__title">
        Walk founders from interest to launch in one clean sequence
      </h2>
      <p class="ff-founderFlow__body">
        FutureFunded sells best when the story feels guided. Show the live fundraiser,
        explain the sponsor and pricing logic, then move the founder into setup with a
        clear next step instead of a scattered tour.
      </p>
    </div>

    <div class="ff-founderFlow__steps" aria-label="Founder demo flow steps">
      <article class="ff-founderFlow__step">
        <p class="ff-founderFlow__stepNumber">01</p>
        <h3>Open the live fundraiser</h3>
        <p>Start with the public surface so the founder immediately sees polish, momentum, and sponsor credibility.</p>
      </article>

      <article class="ff-founderFlow__step">
        <p class="ff-founderFlow__stepNumber">02</p>
        <h3>Show sponsor + pricing logic</h3>
        <p>Use pricing and sponsor packages to explain how the platform helps organizations raise more and sell support more clearly.</p>
      </article>

      <article class="ff-founderFlow__step">
        <p class="ff-founderFlow__stepNumber">03</p>
        <h3>Move into guided launch</h3>
        <p>Shift from “what this is” into “how fast we can get you live” with a simple onboarding path.</p>
      </article>

      <article class="ff-founderFlow__step">
        <p class="ff-founderFlow__stepNumber">04</p>
        <h3>Reinforce operator confidence</h3>
        <p>Close with the platform story: founders are not buying a page, they are buying a cleaner operating system for fundraising.</p>
      </article>
    </div>

    <div class="ff-founderFlow__close">
      <div class="ff-founderFlow__closeCopy">
        <p class="ff-founderFlow__closeEyebrow">Demo close</p>
        <h3 class="ff-founderFlow__closeTitle">Show the product. Explain the value. Give the launch step.</h3>
        <p class="ff-founderFlow__closeBody">
          This is the sequence that makes demos feel tighter and helps warm leads understand exactly what to do next.
        </p>
      </div>

      <div class="ff-founderFlow__actions">
        <a class="ff-founderFlow__button ff-founderFlow__button--secondary" href="/c/spring-fundraiser">
          Open live fundraiser
        </a>
        <a class="ff-founderFlow__button ff-founderFlow__button--primary" href="/platform/onboarding">
          Start guided launch
        </a>
      </div>
    </div>
  </div>
</section>
'''

CSS_BLOCK = r'''
/* ==========================================================================
   FF_PLATFORM_FOUNDER_DEMO_FLOW_V1
   Founder demo sequence strip across platform pages
   ========================================================================== */

body[data-ff-platform="true"] .ff-founderFlow {
  margin-top: clamp(2.5rem, 5vw, 4.5rem);
  padding: clamp(1.25rem, 2vw, 1.75rem);
}

body[data-ff-platform="true"] .ff-founderFlow__inner {
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

body[data-ff-platform="true"] .ff-founderFlow__intro {
  display: grid;
  gap: 0.7rem;
  max-width: 72ch;
}

body[data-ff-platform="true"] .ff-founderFlow__eyebrow,
body[data-ff-platform="true"] .ff-founderFlow__closeEyebrow {
  margin: 0;
  font-size: 0.74rem;
  font-weight: 900;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  opacity: 0.72;
}

body[data-ff-platform="true"] .ff-founderFlow__title {
  margin: 0;
  font-size: clamp(1.45rem, 2.5vw, 2.15rem);
  line-height: 1.08;
  font-weight: 950;
}

body[data-ff-platform="true"] .ff-founderFlow__body,
body[data-ff-platform="true"] .ff-founderFlow__closeBody {
  margin: 0;
  font-size: 1rem;
  line-height: 1.7;
  opacity: 0.92;
}

body[data-ff-platform="true"] .ff-founderFlow__steps {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

body[data-ff-platform="true"] .ff-founderFlow__step {
  display: grid;
  gap: 0.55rem;
  min-height: 100%;
  padding: 1rem;
  border-radius: 20px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
}

body[data-ff-platform="true"] .ff-founderFlow__stepNumber {
  margin: 0;
  font-size: 0.8rem;
  font-weight: 950;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  opacity: 0.68;
}

body[data-ff-platform="true"] .ff-founderFlow__step h3,
body[data-ff-platform="true"] .ff-founderFlow__closeTitle {
  margin: 0;
  font-size: 1.02rem;
  line-height: 1.2;
  font-weight: 900;
}

body[data-ff-platform="true"] .ff-founderFlow__step p {
  margin: 0;
  font-size: 0.94rem;
  line-height: 1.6;
  opacity: 0.92;
}

body[data-ff-platform="true"] .ff-founderFlow__close {
  display: grid;
  gap: 1rem;
  grid-template-columns: minmax(0, 1.25fr) minmax(250px, 0.75fr);
  align-items: center;
  padding: 1rem;
  border-radius: 22px;
  background: rgba(255,255,255,0.035);
  border: 1px solid rgba(255,255,255,0.08);
}

body[data-ff-platform="true"] .ff-founderFlow__closeCopy {
  display: grid;
  gap: 0.5rem;
}

body[data-ff-platform="true"] .ff-founderFlow__actions {
  display: grid;
  gap: 0.75rem;
}

body[data-ff-platform="true"] .ff-founderFlow__button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  border-radius: 15px;
  text-decoration: none;
  font-weight: 900;
  transition: transform 140ms ease, opacity 140ms ease, border-color 140ms ease;
}

body[data-ff-platform="true"] .ff-founderFlow__button:hover {
  transform: translateY(-1px);
}

body[data-ff-platform="true"] .ff-founderFlow__button--primary {
  color: inherit;
  background: linear-gradient(180deg, rgba(255,255,255,0.18), rgba(255,255,255,0.09));
  border: 1px solid rgba(255,255,255,0.16);
}

body[data-ff-platform="true"] .ff-founderFlow__button--secondary {
  color: inherit;
  background: transparent;
  border: 1px solid rgba(255,255,255,0.12);
}

@media (max-width: 1100px) {
  body[data-ff-platform="true"] .ff-founderFlow__steps {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  body[data-ff-platform="true"] .ff-founderFlow__close {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 720px) {
  body[data-ff-platform="true"] .ff-founderFlow__steps {
    grid-template-columns: 1fr;
  }
}

@media (prefers-color-scheme: light) {
  body[data-ff-platform="true"] .ff-founderFlow__inner {
    background:
      linear-gradient(180deg, rgba(255,255,255,0.94), rgba(248,250,252,0.96)),
      #ffffff;
    border-color: rgba(15,23,42,0.08);
    box-shadow:
      0 20px 48px rgba(15,23,42,0.08),
      inset 0 1px 0 rgba(255,255,255,0.7);
  }

  body[data-ff-platform="true"] .ff-founderFlow__step,
  body[data-ff-platform="true"] .ff-founderFlow__close {
    background: rgba(15,23,42,0.03);
    border-color: rgba(15,23,42,0.08);
  }

  body[data-ff-platform="true"] .ff-founderFlow__button--primary,
  body[data-ff-platform="true"] .ff-founderFlow__button--secondary {
    border-color: rgba(15,23,42,0.10);
  }

  body[data-ff-platform="true"] .ff-founderFlow__button--primary {
    background: rgba(15,23,42,0.05);
  }
}
'''

include_line = '{% include "platform/partials/_founder_demo_flow_strip.html" %}'

PARTIAL.parent.mkdir(parents=True, exist_ok=True)
PARTIAL.write_text(PARTIAL_TEXT, encoding="utf-8")
print(f"wrote: {PARTIAL}")

backup(CSS)
css_text = CSS.read_text(encoding="utf-8") if CSS.exists() else ""
if "FF_PLATFORM_FOUNDER_DEMO_FLOW_V1" not in css_text:
    if css_text and not css_text.endswith("\n"):
        css_text += "\n"
    css_text += "\n" + CSS_BLOCK.strip() + "\n"
    CSS.write_text(css_text, encoding="utf-8")
    print("changed: platform-pages.css founder demo flow block")
else:
    print("skip: founder demo flow css block already present")

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
        print(f"changed: inserted founder flow include into {target.name}")
    elif "{% endblock %}" in text:
        replacement = "\n" + include_line + "\n{% endblock %}"
        text = text.replace("{% endblock %}", replacement, 1)
        target.write_text(text, encoding="utf-8")
        print(f"changed: inserted founder flow include before endblock in {target.name}")
    else:
        print(f"MISS: no insertion anchor in {target.name}")

print("done.")
