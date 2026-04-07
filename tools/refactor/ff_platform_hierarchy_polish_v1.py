from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/platform-pages.css"

if not CSS.exists():
    raise SystemExit(f"Missing CSS file: {CSS}")

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
shutil.copy2(CSS, CSS.with_name(f"{CSS.name}.{timestamp}.bak"))

src = CSS.read_text(encoding="utf-8")

BLOCK_START = "/* FF_PLATFORM_HIERARCHY_POLISH_V1_START */"
BLOCK_END = "/* FF_PLATFORM_HIERARCHY_POLISH_V1_END */"

block = r"""
/* FF_PLATFORM_HIERARCHY_POLISH_V1_START */
@layer ff.pages {
  body[data-ff-template="platform"] {
    --ff-platform-feature-border: rgb(249 115 22 / 0.16);
    --ff-platform-feature-glow: rgb(249 115 22 / 0.14);
    --ff-platform-info-glow: rgb(14 165 233 / 0.12);
    --ff-platform-quiet-border: rgb(226 232 240 / 0.08);
    --ff-platform-quiet-bg:
      linear-gradient(180deg, rgb(255 255 255 / 0.02), rgb(255 255 255 / 0)),
      rgb(8 17 34 / 0.72);
  }

  /* -----------------------------------------------------------------------
     Featured tier
     ----------------------------------------------------------------------- */
  body[data-ff-template="platform"] .ff-platformCard--feature,
  body[data-ff-page="home"] .ff-platformGridTop > .ff-grid.ff-grid--1 > :first-child,
  body[data-ff-page="pricing"] .ff-platformGridTop > aside.ff-card.ff-glass,
  body[data-ff-page="pricing"] [aria-labelledby="platformPlansTitle"] .ff-grid.ff-grid--3 > :nth-child(2),
  body[data-ff-page="demo"] .ff-platformGridTop > aside.ff-card.ff-glass,
  body[data-ff-page="demo"] [aria-labelledby="platformDemoStepsTitle"] .ff-grid.ff-grid--2 > :nth-child(1),
  body[data-ff-page="demo"] [aria-labelledby="platformDemoStepsTitle"] .ff-grid.ff-grid--2 > :nth-child(4) {
    border-color: var(--ff-platform-feature-border);
    background:
      radial-gradient(circle at top right, var(--ff-platform-feature-glow), transparent 34%),
      radial-gradient(circle at top left, var(--ff-platform-info-glow), transparent 38%),
      linear-gradient(180deg, rgb(255 255 255 / 0.05), rgb(255 255 255 / 0)),
      var(--ff-panel-strong);
    box-shadow:
      0 0 0 1px rgb(249 115 22 / 0.05),
      var(--ff-shadow-2);
  }

  /* -----------------------------------------------------------------------
     Quiet tier
     ----------------------------------------------------------------------- */
  body[data-ff-template="platform"] .ff-platformCard--quiet,
  body[data-ff-page="home"] .ff-platformGridTop > .ff-grid.ff-grid--1 > :last-child,
  body[data-ff-page="pricing"] .ff-platformGridTop > aside.ff-card.ff-glass > .ff-card.ff-glass,
  body[data-ff-page="pricing"] [aria-labelledby="platformPlansTitle"] .ff-grid.ff-grid--3 > :nth-child(1),
  body[data-ff-page="pricing"] [aria-labelledby="platformPlansTitle"] .ff-grid.ff-grid--3 > :nth-child(3),
  body[data-ff-page="demo"] .ff-platformGridTop > header .ff-card.ff-glass,
  body[data-ff-page="demo"] .ff-platformGridTop > aside.ff-card.ff-glass > .ff-card.ff-glass {
    border-color: var(--ff-platform-quiet-border);
    background: var(--ff-platform-quiet-bg);
    box-shadow: var(--ff-shadow-1);
  }

  /* -----------------------------------------------------------------------
     Section rhythm
     ----------------------------------------------------------------------- */
  body[data-ff-template="platform"] .ff-sectionhead {
    gap: 0.78rem;
  }

  body[data-ff-template="platform"] .ff-sectionhead__text > .ff-lead,
  body[data-ff-template="platform"] .ff-card.ff-glass > .ff-help,
  body[data-ff-template="platform"] .ff-card.ff-glass p.ff-help,
  body[data-ff-template="platform"] .ff-card.ff-glass p.ff-muted {
    max-width: 56ch;
  }

  body[data-ff-template="platform"] .ff-grid.ff-grid--4 > *,
  body[data-ff-template="platform"] .ff-grid.ff-grid--3 > *,
  body[data-ff-template="platform"] .ff-grid.ff-grid--2 > * {
    min-height: 100%;
  }

  /* -----------------------------------------------------------------------
     Home page hierarchy
     ----------------------------------------------------------------------- */
  body[data-ff-page="home"] .ff-sectionhead[aria-labelledby="platformHomeHeroTitle"] .ff-display {
    max-width: 9.2ch;
  }

  body[data-ff-page="home"] [aria-labelledby="platformLaunchCardsTitle"] .ff-grid.ff-grid--4 > *:nth-child(1),
  body[data-ff-page="home"] [aria-labelledby="platformLaunchCardsTitle"] .ff-grid.ff-grid--4 > *:nth-child(2) {
    border-color: rgb(14 165 233 / 0.14);
    background:
      linear-gradient(180deg, rgb(14 165 233 / 0.05), rgb(14 165 233 / 0)),
      var(--ff-panel);
  }

  body[data-ff-page="home"] [aria-labelledby="platformWhyItWinsTitle"] {
    border-color: rgb(14 165 233 / 0.12);
  }

  /* -----------------------------------------------------------------------
     Pricing page hierarchy
     ----------------------------------------------------------------------- */
  body[data-ff-page="pricing"] [aria-labelledby="platformPlansTitle"] .ff-grid.ff-grid--3 > :nth-child(2) .ff-btn--primary {
    box-shadow:
      inset 0 1px 0 rgb(255 255 255 / 0.14),
      0 14px 28px rgb(249 115 22 / 0.26);
  }

  body[data-ff-page="pricing"] [aria-labelledby="platformPricingDemoTitle"] {
    border-color: rgb(14 165 233 / 0.14);
    background:
      radial-gradient(circle at top right, rgb(14 165 233 / 0.1), transparent 34%),
      linear-gradient(180deg, rgb(255 255 255 / 0.04), rgb(255 255 255 / 0)),
      var(--ff-panel-strong);
  }

  /* -----------------------------------------------------------------------
     Demo page hierarchy
     ----------------------------------------------------------------------- */
  body[data-ff-page="demo"] [aria-labelledby="platformDemoTitle"] .ff-display {
    max-width: 8.6ch;
  }

  body[data-ff-page="demo"] [aria-labelledby="platformDemoStepsTitle"] .ff-grid.ff-grid--2 > :nth-child(2),
  body[data-ff-page="demo"] [aria-labelledby="platformDemoStepsTitle"] .ff-grid.ff-grid--2 > :nth-child(3) {
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.03), rgb(255 255 255 / 0)),
      var(--ff-panel);
  }

  body[data-ff-page="demo"] #demoCloseTitle,
  body[data-ff-page="demo"] #platformDemoFounderCloseTitle {
    text-wrap: balance;
  }

  body[data-ff-page="demo"] [aria-labelledby="demoCloseTitle"],
  body[data-ff-page="demo"] [aria-labelledby="platformDemoFounderCloseTitle"] {
    border-color: rgb(249 115 22 / 0.14);
    background:
      radial-gradient(circle at top right, rgb(249 115 22 / 0.1), transparent 30%),
      linear-gradient(180deg, rgb(255 255 255 / 0.04), rgb(255 255 255 / 0)),
      var(--ff-panel-strong);
  }

  /* -----------------------------------------------------------------------
     CTA polish
     ----------------------------------------------------------------------- */
  body[data-ff-template="platform"] .ff-btn.ff-btn--pill.ff-btn--secondary {
    opacity: 0.96;
  }

  body[data-ff-template="platform"] .ff-btn.ff-btn--pill.ff-btn--secondary:hover,
  body[data-ff-template="platform"] .ff-btn.ff-btn--pill.ff-btn--secondary:focus-visible {
    opacity: 1;
  }

  @media (max-width: 900px) {
    body[data-ff-page="home"] .ff-sectionhead[aria-labelledby="platformHomeHeroTitle"] .ff-display,
    body[data-ff-page="demo"] [aria-labelledby="platformDemoTitle"] .ff-display {
      max-width: 10ch;
    }
  }
}
/* FF_PLATFORM_HIERARCHY_POLISH_V1_END */
"""

if BLOCK_START in src and BLOCK_END in src:
    start = src.index(BLOCK_START)
    end = src.index(BLOCK_END) + len(BLOCK_END)
    updated = src[:start] + block + src[end:]
else:
    updated = src.rstrip() + "\n\n" + block + "\n"

CSS.write_text(updated, encoding="utf-8")
print("patched", CSS)
