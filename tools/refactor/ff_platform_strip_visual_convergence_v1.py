from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/platform-pages.css"

BLOCK = r'''
/* ==========================================================================
   FF_PLATFORM_STRIP_VISUAL_CONVERGENCE_V1
   Founder flow + operator strip visual convergence
   - darkens strip surfaces to match platform chrome
   - improves heading/body contrast
   - upgrades CTA styling
   - tightens card depth and premium hierarchy
   ========================================================================== */

body[data-ff-platform="true"] .ff-founderFlow,
body[data-ff-platform="true"] .ff-operatorPremium {
  margin-top: clamp(2.25rem, 4vw, 4rem);
}

body[data-ff-platform="true"] .ff-founderFlow__inner,
body[data-ff-platform="true"] .ff-operatorPremium__inner {
  position: relative;
  overflow: hidden;
  border-radius: 30px;
  border: 1px solid rgba(120, 146, 191, 0.14);
  background:
    radial-gradient(1200px 420px at 0% -10%, rgba(43, 122, 255, 0.14), transparent 58%),
    radial-gradient(760px 300px at 100% 0%, rgba(255, 122, 38, 0.10), transparent 52%),
    linear-gradient(180deg, rgba(8, 18, 35, 0.96), rgba(3, 10, 22, 0.985));
  box-shadow:
    0 24px 56px rgba(0, 0, 0, 0.30),
    inset 0 1px 0 rgba(255,255,255,0.05),
    inset 0 -1px 0 rgba(255,255,255,0.02);
  backdrop-filter: blur(16px);
}

body[data-ff-platform="true"] .ff-founderFlow__inner::before,
body[data-ff-platform="true"] .ff-operatorPremium__inner::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    linear-gradient(180deg, rgba(255,255,255,0.035), transparent 18%, transparent 82%, rgba(255,255,255,0.02));
  opacity: 0.9;
}

body[data-ff-platform="true"] .ff-founderFlow__intro,
body[data-ff-platform="true"] .ff-operatorPremium__intro,
body[data-ff-platform="true"] .ff-founderFlow__closeCopy,
body[data-ff-platform="true"] .ff-operatorPremium__railMain {
  position: relative;
  z-index: 1;
}

body[data-ff-platform="true"] .ff-founderFlow__eyebrow,
body[data-ff-platform="true"] .ff-founderFlow__closeEyebrow,
body[data-ff-platform="true"] .ff-founderFlow__stepNumber,
body[data-ff-platform="true"] .ff-operatorPremium__eyebrow,
body[data-ff-platform="true"] .ff-operatorPremium__railEyebrow,
body[data-ff-platform="true"] .ff-operatorPremium__kicker {
  color: rgba(191, 216, 255, 0.82);
  opacity: 1;
  letter-spacing: 0.15em;
}

body[data-ff-platform="true"] .ff-founderFlow__title,
body[data-ff-platform="true"] .ff-operatorPremium__title,
body[data-ff-platform="true"] .ff-founderFlow__closeTitle,
body[data-ff-platform="true"] .ff-operatorPremium__railTitle,
body[data-ff-platform="true"] .ff-founderFlow__step h3,
body[data-ff-platform="true"] .ff-operatorPremium__card h3 {
  color: #f5f9ff;
  text-shadow: 0 1px 0 rgba(0,0,0,0.18);
}

body[data-ff-platform="true"] .ff-founderFlow__body,
body[data-ff-platform="true"] .ff-founderFlow__closeBody,
body[data-ff-platform="true"] .ff-founderFlow__step p,
body[data-ff-platform="true"] .ff-operatorPremium__body,
body[data-ff-platform="true"] .ff-operatorPremium__card p,
body[data-ff-platform="true"] .ff-operatorPremium__list {
  color: rgba(219, 231, 248, 0.92);
  opacity: 1;
}

body[data-ff-platform="true"] .ff-founderFlow__steps,
body[data-ff-platform="true"] .ff-operatorPremium__grid,
body[data-ff-platform="true"] .ff-founderFlow__close,
body[data-ff-platform="true"] .ff-operatorPremium__rail {
  position: relative;
  z-index: 1;
}

body[data-ff-platform="true"] .ff-founderFlow__step,
body[data-ff-platform="true"] .ff-founderFlow__close,
body[data-ff-platform="true"] .ff-operatorPremium__card,
body[data-ff-platform="true"] .ff-operatorPremium__rail {
  border-radius: 22px;
  border: 1px solid rgba(120, 146, 191, 0.16);
  background:
    linear-gradient(180deg, rgba(10, 19, 36, 0.94), rgba(6, 13, 26, 0.98));
  box-shadow:
    0 16px 34px rgba(0,0,0,0.22),
    inset 0 1px 0 rgba(255,255,255,0.04);
}

body[data-ff-platform="true"] .ff-founderFlow__step:hover,
body[data-ff-platform="true"] .ff-operatorPremium__card:hover {
  transform: translateY(-2px);
  border-color: rgba(255, 146, 71, 0.24);
  box-shadow:
    0 20px 42px rgba(0,0,0,0.26),
    0 0 0 1px rgba(255, 146, 71, 0.08),
    inset 0 1px 0 rgba(255,255,255,0.05);
}

body[data-ff-platform="true"] .ff-founderFlow__step,
body[data-ff-platform="true"] .ff-operatorPremium__card {
  transition:
    transform 180ms ease,
    border-color 180ms ease,
    box-shadow 180ms ease;
}

body[data-ff-platform="true"] .ff-founderFlow__button,
body[data-ff-platform="true"] .ff-operatorPremium__button {
  min-height: 50px;
  border-radius: 15px;
  font-weight: 900;
  letter-spacing: 0.01em;
  box-shadow:
    0 10px 24px rgba(0,0,0,0.18),
    inset 0 1px 0 rgba(255,255,255,0.06);
}

body[data-ff-platform="true"] .ff-founderFlow__button--primary,
body[data-ff-platform="true"] .ff-operatorPremium__button--primary {
  color: #fff7ef;
  border: 1px solid rgba(255, 151, 82, 0.44);
  background:
    linear-gradient(180deg, rgba(255, 154, 80, 0.98), rgba(238, 103, 27, 0.98));
  box-shadow:
    0 16px 34px rgba(238, 103, 27, 0.22),
    inset 0 1px 0 rgba(255,255,255,0.24);
}

body[data-ff-platform="true"] .ff-founderFlow__button--primary:hover,
body[data-ff-platform="true"] .ff-operatorPremium__button--primary:hover {
  transform: translateY(-1px);
  filter: brightness(1.02);
}

body[data-ff-platform="true"] .ff-founderFlow__button--secondary,
body[data-ff-platform="true"] .ff-operatorPremium__button--secondary {
  color: rgba(241, 247, 255, 0.96);
  border: 1px solid rgba(120, 146, 191, 0.18);
  background:
    linear-gradient(180deg, rgba(18, 27, 44, 0.94), rgba(9, 15, 28, 0.98));
}

body[data-ff-platform="true"] .ff-founderFlow__button--secondary:hover,
body[data-ff-platform="true"] .ff-operatorPremium__button--secondary:hover {
  border-color: rgba(255, 151, 82, 0.22);
}

body[data-ff-platform="true"] .ff-founderFlow__close,
body[data-ff-platform="true"] .ff-operatorPremium__rail {
  padding: 1.1rem;
}

body[data-ff-platform="true"] .ff-founderFlow__step,
body[data-ff-platform="true"] .ff-operatorPremium__card {
  padding: 1.05rem;
}

@media (max-width: 720px) {
  body[data-ff-platform="true"] .ff-founderFlow__inner,
  body[data-ff-platform="true"] .ff-operatorPremium__inner {
    border-radius: 24px;
    padding: 1.15rem;
  }

  body[data-ff-platform="true"] .ff-founderFlow__step,
  body[data-ff-platform="true"] .ff-operatorPremium__card,
  body[data-ff-platform="true"] .ff-founderFlow__close,
  body[data-ff-platform="true"] .ff-operatorPremium__rail {
    border-radius: 18px;
  }

  body[data-ff-platform="true"] .ff-founderFlow__button,
  body[data-ff-platform="true"] .ff-operatorPremium__button {
    min-height: 48px;
  }
}

@media (prefers-color-scheme: light) {
  body[data-ff-platform="true"] .ff-founderFlow__inner,
  body[data-ff-platform="true"] .ff-operatorPremium__inner {
    border-color: rgba(15, 23, 42, 0.08);
    background:
      radial-gradient(1200px 420px at 0% -10%, rgba(43, 122, 255, 0.08), transparent 58%),
      radial-gradient(760px 300px at 100% 0%, rgba(255, 122, 38, 0.06), transparent 52%),
      linear-gradient(180deg, rgba(255,255,255,0.96), rgba(246,249,253,0.98));
    box-shadow:
      0 22px 48px rgba(15,23,42,0.08),
      inset 0 1px 0 rgba(255,255,255,0.72);
  }

  body[data-ff-platform="true"] .ff-founderFlow__title,
  body[data-ff-platform="true"] .ff-operatorPremium__title,
  body[data-ff-platform="true"] .ff-founderFlow__closeTitle,
  body[data-ff-platform="true"] .ff-operatorPremium__railTitle,
  body[data-ff-platform="true"] .ff-founderFlow__step h3,
  body[data-ff-platform="true"] .ff-operatorPremium__card h3 {
    color: #0f172a;
    text-shadow: none;
  }

  body[data-ff-platform="true"] .ff-founderFlow__body,
  body[data-ff-platform="true"] .ff-founderFlow__closeBody,
  body[data-ff-platform="true"] .ff-founderFlow__step p,
  body[data-ff-platform="true"] .ff-operatorPremium__body,
  body[data-ff-platform="true"] .ff-operatorPremium__card p,
  body[data-ff-platform="true"] .ff-operatorPremium__list {
    color: rgba(15, 23, 42, 0.82);
  }

  body[data-ff-platform="true"] .ff-founderFlow__step,
  body[data-ff-platform="true"] .ff-founderFlow__close,
  body[data-ff-platform="true"] .ff-operatorPremium__card,
  body[data-ff-platform="true"] .ff-operatorPremium__rail {
    background:
      linear-gradient(180deg, rgba(255,255,255,0.94), rgba(248,250,252,0.98));
    border-color: rgba(15, 23, 42, 0.08);
    box-shadow:
      0 14px 28px rgba(15,23,42,0.07),
      inset 0 1px 0 rgba(255,255,255,0.68);
  }

  body[data-ff-platform="true"] .ff-founderFlow__button--secondary,
  body[data-ff-platform="true"] .ff-operatorPremium__button--secondary {
    color: #0f172a;
    border-color: rgba(15, 23, 42, 0.10);
    background:
      linear-gradient(180deg, rgba(255,255,255,0.98), rgba(244,247,251,1));
  }
}
'''

def backup(path: Path) -> None:
    if path.exists():
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        shutil.copy2(path, path.with_name(f"{path.name}.{ts}.bak"))

css_text = CSS.read_text(encoding="utf-8") if CSS.exists() else ""

if "FF_PLATFORM_STRIP_VISUAL_CONVERGENCE_V1" in css_text:
    print("skip: convergence block already present")
    raise SystemExit(0)

backup(CSS)

if css_text and not css_text.endswith("\n"):
    css_text += "\n"

css_text += "\n" + BLOCK.strip() + "\n"
CSS.write_text(css_text, encoding="utf-8")
print("changed: platform-pages.css strip visual convergence block appended")
