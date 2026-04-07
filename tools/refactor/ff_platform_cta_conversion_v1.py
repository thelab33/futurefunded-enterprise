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

BLOCK_START = "/* FF_PLATFORM_CTA_CONVERSION_V1_START */"
BLOCK_END = "/* FF_PLATFORM_CTA_CONVERSION_V1_END */"

block = r"""
/* FF_PLATFORM_CTA_CONVERSION_V1_START */
@layer ff.pages {
  body[data-ff-template="platform"] {
    --ff-platform-cta-shadow:
      inset 0 1px 0 rgb(255 255 255 / 0.16),
      0 16px 32px rgb(249 115 22 / 0.24);
    --ff-platform-cta-shadow-hover:
      inset 0 1px 0 rgb(255 255 255 / 0.18),
      0 18px 36px rgb(249 115 22 / 0.28);
  }

  body[data-ff-template="platform"] .ff-btn.ff-btn--primary,
  body[data-ff-template="platform"] .ff-btn.ff-btn--pill.ff-btn--primary {
    box-shadow: var(--ff-platform-cta-shadow);
  }

  body[data-ff-template="platform"] .ff-btn.ff-btn--primary:hover,
  body[data-ff-template="platform"] .ff-btn.ff-btn--primary:focus-visible,
  body[data-ff-template="platform"] .ff-btn.ff-btn--pill.ff-btn--primary:hover,
  body[data-ff-template="platform"] .ff-btn.ff-btn--pill.ff-btn--primary:focus-visible {
    box-shadow: var(--ff-platform-cta-shadow-hover);
    transform: translateY(-1px);
  }

  body[data-ff-template="platform"] .ff-btn.ff-btn--secondary,
  body[data-ff-template="platform"] .ff-btn.ff-btn--pill.ff-btn--secondary {
    opacity: 0.92;
  }

  body[data-ff-template="platform"] .ff-btn.ff-btn--secondary:hover,
  body[data-ff-template="platform"] .ff-btn.ff-btn--secondary:focus-visible,
  body[data-ff-template="platform"] .ff-btn.ff-btn--pill.ff-btn--secondary:hover,
  body[data-ff-template="platform"] .ff-btn.ff-btn--pill.ff-btn--secondary:focus-visible {
    opacity: 1;
  }

  /* Hero CTA emphasis */
  body[data-ff-page="home"] .ff-sectionhead[aria-labelledby="platformHomeHeroTitle"] .ff-btn--primary,
  body[data-ff-page="pricing"] .ff-platformGridTop > aside.ff-card.ff-glass .ff-btn--primary,
  body[data-ff-page="demo"] .ff-platformGridTop > aside.ff-card.ff-glass .ff-btn--primary {
    min-height: 3rem;
    padding-inline: 1.1rem;
  }

  /* Pricing featured plan CTA */
  body[data-ff-page="pricing"] [aria-labelledby="platformPlansTitle"] .ff-grid.ff-grid--3 > :nth-child(2) .ff-btn--primary {
    min-height: 3rem;
    width: 100%;
  }

  /* Close-section CTA bars */
  body[data-ff-page="pricing"] [aria-labelledby="platformPricingCloseTitle"] .ff-row.ff-wrap.ff-gap-2,
  body[data-ff-page="demo"] [aria-labelledby="demoCloseTitle"] .ff-row.ff-wrap.ff-gap-2,
  body[data-ff-page="demo"] [aria-labelledby="platformDemoFounderCloseTitle"] .ff-row.ff-wrap.ff-gap-2 {
    align-items: center;
  }

  body[data-ff-page="pricing"] [aria-labelledby="platformPricingCloseTitle"] .ff-btn--primary,
  body[data-ff-page="demo"] [aria-labelledby="demoCloseTitle"] .ff-btn--primary,
  body[data-ff-page="demo"] [aria-labelledby="platformDemoFounderCloseTitle"] .ff-btn--primary {
    min-height: 3rem;
    padding-inline: 1.15rem;
  }

  /* CTA spacing rhythm */
  body[data-ff-template="platform"] .ff-row.ff-wrap.ff-gap-2 .ff-btn + .ff-btn {
    margin-inline-start: 0;
  }

  @media (max-width: 640px) {
    body[data-ff-template="platform"] .ff-row.ff-wrap.ff-gap-2 {
      width: 100%;
    }

    body[data-ff-template="platform"] .ff-row.ff-wrap.ff-gap-2 .ff-btn {
      flex: 1 1 100%;
      width: 100%;
    }

    body[data-ff-template="platform"] .ff-row.ff-wrap.ff-gap-2 .ff-btn--primary {
      order: -1;
    }
  }
}
/* FF_PLATFORM_CTA_CONVERSION_V1_END */
"""

if BLOCK_START in src and BLOCK_END in src:
    start = src.index(BLOCK_START)
    end = src.index(BLOCK_END) + len(BLOCK_END)
    updated = src[:start] + block + src[end:]
else:
    updated = src.rstrip() + "\n\n" + block + "\n"

CSS.write_text(updated, encoding="utf-8")
print("patched", CSS)
