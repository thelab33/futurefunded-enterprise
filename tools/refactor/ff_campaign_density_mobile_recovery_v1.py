from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/ff.css"

BLOCK = r'''
/* ==========================================================================
   FF_CAMPAIGN_DENSITY_MOBILE_RECOVERY_V1
   - compress teams dead-air shell
   - improve sponsor empty-state / visibility rail
   - restore branded mobile CTA styling
   - tighten below-the-fold campaign density
   ========================================================================== */

body[data-ff-page="fundraiser"] #teams,
body[data-ff-page="fundraiser"] #sponsors {
  scroll-margin-top: 5.5rem;
}

body[data-ff-page="fundraiser"] .ff-teamsShell {
  gap: clamp(0.9rem, 1.6vw, 1.25rem);
}

body[data-ff-page="fundraiser"] .ff-teamsEmpty {
  position: relative;
  min-height: clamp(11rem, 22vw, 16rem);
  border-radius: 1.35rem;
  border: 1px solid rgba(90, 118, 165, 0.16);
  background:
    radial-gradient(1200px 280px at 0% 0%, rgba(43,122,255,0.10), transparent 58%),
    linear-gradient(180deg, rgba(8,16,30,0.92), rgba(5,10,22,0.98));
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.04),
    0 18px 36px rgba(0,0,0,0.16);
  overflow: hidden;
}

body[data-ff-page="fundraiser"] .ff-teamsEmpty::before {
  content: "Program spotlight area";
  position: absolute;
  top: 1rem;
  left: 1rem;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: rgba(191, 216, 255, 0.78);
}

body[data-ff-page="fundraiser"] .ff-teamsEmpty::after {
  content: "";
  position: absolute;
  inset: auto 1rem 1rem 1rem;
  height: 56%;
  border-radius: 1rem;
  border: 1px dashed rgba(120, 146, 191, 0.16);
  background:
    linear-gradient(180deg, rgba(255,255,255,0.018), rgba(255,255,255,0.01)),
    repeating-linear-gradient(
      90deg,
      rgba(255,255,255,0.018) 0 1px,
      transparent 1px 72px
    );
  opacity: 0.9;
}

body[data-ff-page="fundraiser"] .ff-teamGrid {
  align-items: start;
}

body[data-ff-page="fundraiser"] .ff-teamCard {
  min-height: 100%;
}

body[data-ff-page="fundraiser"] .ff-teamCard__media {
  background:
    linear-gradient(180deg, rgba(255,255,255,0.015), rgba(255,255,255,0.005)),
    rgba(5, 10, 20, 0.42);
}

body[data-ff-page="fundraiser"] .ff-teamCard__foot {
  margin-top: auto;
}

body[data-ff-page="fundraiser"] .ff-sponsorsBoard,
body[data-ff-page="fundraiser"] .ff-sponsorWallBlock {
  gap: clamp(0.85rem, 1.5vw, 1.15rem);
}

body[data-ff-page="fundraiser"] .ff-sponsorWallRail {
  gap: 0.75rem;
  align-items: stretch;
}

body[data-ff-page="fundraiser"] .ff-sponsorGhost,
body[data-ff-page="fundraiser"] .ff-sponsorEmptyState,
body[data-ff-page="fundraiser"] [data-ff-sponsor-wall-empty] {
  min-height: 4.5rem;
  border-radius: 1rem;
  border: 1px solid rgba(90, 118, 165, 0.14);
  background:
    linear-gradient(180deg, rgba(10,18,32,0.88), rgba(6,12,24,0.94));
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.03);
}

body[data-ff-page="fundraiser"] .ff-sponsorEmptyState,
body[data-ff-page="fundraiser"] [data-ff-sponsor-wall-empty] {
  display: grid;
  align-content: center;
  gap: 0.5rem;
  padding: 0.9rem 1rem;
  color: rgba(218, 228, 242, 0.84);
}

body[data-ff-page="fundraiser"] .ff-sponsorGhost {
  position: relative;
  overflow: hidden;
}

body[data-ff-page="fundraiser"] .ff-sponsorGhost::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, transparent, rgba(255,255,255,0.045), transparent);
  transform: translateX(-100%);
  animation: ffSponsorGhostSweep 2.8s linear infinite;
  opacity: 0.8;
}

@keyframes ffSponsorGhostSweep {
  to {
    transform: translateX(100%);
  }
}

body[data-ff-page="fundraiser"] .ff-sponsorTierGrid {
  align-items: stretch;
}

body[data-ff-page="fundraiser"] .ff-sponsorCell {
  min-height: 100%;
}

body[data-ff-page="fundraiser"] .ff-sponsorCell > *:last-child,
body[data-ff-page="fundraiser"] .ff-sponsorTierCard__foot {
  margin-top: auto;
}

body[data-ff-page="fundraiser"] .ff-sponsorSpotlight,
body[data-ff-page="fundraiser"] .ff-sponsorPitch {
  margin-bottom: 0.35rem;
}

body[data-ff-page="fundraiser"] .ff-proofMini--teams {
  margin-top: 0.2rem;
}

body[data-ff-page="fundraiser"] .ff-footerGrid {
  gap: clamp(0.9rem, 1.8vw, 1.25rem);
}

@media (max-width: 768px) {
  body[data-ff-page="fundraiser"] .ff-teamsEmpty {
    min-height: 8.5rem;
    border-radius: 1.1rem;
  }

  body[data-ff-page="fundraiser"] .ff-teamsEmpty::before {
    top: 0.85rem;
    left: 0.85rem;
    font-size: 0.66rem;
  }

  body[data-ff-page="fundraiser"] .ff-teamsEmpty::after {
    inset: auto 0.85rem 0.85rem 0.85rem;
    height: 48%;
    border-radius: 0.9rem;
  }

  body[data-ff-page="fundraiser"] .ff-sponsorGhost,
  body[data-ff-page="fundraiser"] .ff-sponsorEmptyState,
  body[data-ff-page="fundraiser"] [data-ff-sponsor-wall-empty] {
    min-height: 3.75rem;
    border-radius: 0.9rem;
  }

  body[data-ff-page="fundraiser"] .ff-teamCard,
  body[data-ff-page="fundraiser"] .ff-sponsorCell,
  body[data-ff-page="fundraiser"] .ff-sponsorTierCard {
    border-radius: 1.1rem;
  }

  body[data-ff-page="fundraiser"] .ff-donate-btn,
  body[data-ff-page="fundraiser"] .ff-tab--cta,
  body[data-ff-page="fundraiser"] .ff-mobileCtaBar__btn,
  body[data-ff-page="fundraiser"] .ff-mobileActionRail__button--primary,
  body[data-ff-page="fundraiser"] .ff-teamCard__foot .ff-btn,
  body[data-ff-page="fundraiser"] .ff-sponsorTierCard .ff-btn,
  body[data-ff-page="fundraiser"] [data-ff-donate] {
    color: #fff7ef !important;
    border: 1px solid rgba(255, 151, 82, 0.46) !important;
    background:
      linear-gradient(180deg, rgba(255, 154, 80, 0.99), rgba(238, 103, 27, 0.99)) !important;
    box-shadow:
      0 14px 30px rgba(238, 103, 27, 0.20),
      inset 0 1px 0 rgba(255,255,255,0.22) !important;
  }

  body[data-ff-page="fundraiser"] .ff-mobileActionRail__button--secondary,
  body[data-ff-page="fundraiser"] .ff-footer__link--button,
  body[data-ff-page="fundraiser"] .ff-teamCard__foot .ff-link,
  body[data-ff-page="fundraiser"] [data-ff-open-sponsor] {
    color: rgba(241, 247, 255, 0.96) !important;
    border: 1px solid rgba(120, 146, 191, 0.18) !important;
    background:
      linear-gradient(180deg, rgba(18, 27, 44, 0.94), rgba(9, 15, 28, 0.98)) !important;
    box-shadow:
      0 10px 22px rgba(0,0,0,0.16),
      inset 0 1px 0 rgba(255,255,255,0.05) !important;
  }

  body[data-ff-page="fundraiser"] .ff-donate-btn,
  body[data-ff-page="fundraiser"] .ff-tab--cta,
  body[data-ff-page="fundraiser"] .ff-mobileCtaBar__btn,
  body[data-ff-page="fundraiser"] .ff-mobileActionRail__button--primary,
  body[data-ff-page="fundraiser"] .ff-mobileActionRail__button--secondary,
  body[data-ff-page="fundraiser"] .ff-teamCard__foot .ff-btn,
  body[data-ff-page="fundraiser"] .ff-sponsorTierCard .ff-btn,
  body[data-ff-page="fundraiser"] .ff-footer__link--button,
  body[data-ff-page="fundraiser"] [data-ff-donate],
  body[data-ff-page="fundraiser"] [data-ff-open-sponsor] {
    min-height: 44px !important;
    border-radius: 0.9rem !important;
    font-weight: 800 !important;
    text-decoration: none !important;
  }
}

html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-teamsEmpty {
  border-color: rgba(120, 146, 191, 0.16);
}

html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-sponsorGhost,
html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-sponsorEmptyState,
html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] [data-ff-sponsor-wall-empty] {
  border-color: rgba(120, 146, 191, 0.14);
}
'''

def backup(path: Path) -> None:
    if path.exists():
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        shutil.copy2(path, path.with_name(f"{path.name}.{ts}.bak"))

css_text = CSS.read_text(encoding="utf-8") if CSS.exists() else ""

if "FF_CAMPAIGN_DENSITY_MOBILE_RECOVERY_V1" in css_text:
    print("skip: density/mobile recovery block already present")
    raise SystemExit(0)

backup(CSS)

if css_text and not css_text.endswith("\n"):
    css_text += "\n"

css_text += "\n" + BLOCK.strip() + "\n"
CSS.write_text(css_text, encoding="utf-8")
print("changed: ff.css campaign density/mobile recovery block appended")
