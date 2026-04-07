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

BLOCK_START = "/* FF_PLATFORM_FLAGSHIP_FINISH_V1_START */"
BLOCK_END = "/* FF_PLATFORM_FLAGSHIP_FINISH_V1_END */"

block = r"""
/* FF_PLATFORM_FLAGSHIP_FINISH_V1_START */
@layer ff.pages {
  /* -----------------------------------------------------------------------
     Hero headline finish
     ----------------------------------------------------------------------- */
  body[data-ff-page="home"] #platformHomeHeroTitle {
    max-width: 10.1ch;
  }

  body[data-ff-page="pricing"] #platformPricingHeroTitle {
    max-width: 9.8ch;
  }

  body[data-ff-page="demo"] #platformDemoTitle {
    max-width: 8.9ch;
  }

  /* -----------------------------------------------------------------------
     Trust strip / top system bar
     ----------------------------------------------------------------------- */
  body[data-ff-template="platform"] [data-ff-platform-trust] {
    padding: clamp(1rem, 0.96rem + 0.35vw, 1.2rem);
    border-color: rgb(255 255 255 / 0.12);
    background:
      radial-gradient(circle at top right, rgb(14 165 233 / 0.08), transparent 28%),
      linear-gradient(180deg, rgb(255 255 255 / 0.04), rgb(255 255 255 / 0)),
      var(--ff-panel-strong);
    box-shadow:
      0 0 0 1px rgb(255 255 255 / 0.03),
      var(--ff-shadow-2);
  }

  body[data-ff-template="platform"] [data-ff-platform-trust] .ff-pill {
    min-height: 1.7rem;
    padding: 0.22rem 0.62rem;
    font-size: 0.68rem;
    letter-spacing: 0.05em;
  }

  /* -----------------------------------------------------------------------
     Close-band finish
     ----------------------------------------------------------------------- */
  body[data-ff-page="pricing"] [aria-labelledby="platformPricingCloseTitle"],
  body[data-ff-page="demo"] [aria-labelledby="demoCloseTitle"],
  body[data-ff-page="demo"] [aria-labelledby="platformDemoFounderCloseTitle"] {
    border-color: rgb(255 255 255 / 0.11);
    background:
      radial-gradient(circle at 85% 18%, rgb(249 115 22 / 0.09), transparent 28%),
      linear-gradient(180deg, rgb(255 255 255 / 0.04), rgb(255 255 255 / 0)),
      var(--ff-panel-strong);
    box-shadow:
      0 0 0 1px rgb(255 255 255 / 0.03),
      var(--ff-shadow-2);
  }

  body[data-ff-page="pricing"] [aria-labelledby="platformPricingCloseTitle"] .ff-row.ff-row--between,
  body[data-ff-page="demo"] [aria-labelledby="demoCloseTitle"] .ff-row.ff-row--between,
  body[data-ff-page="demo"] [aria-labelledby="platformDemoFounderCloseTitle"] .ff-row.ff-row--between {
    align-items: center;
    gap: 1rem;
  }

  body[data-ff-page="pricing"] [aria-labelledby="platformPricingCloseTitle"] .ff-btn--primary,
  body[data-ff-page="demo"] [aria-labelledby="demoCloseTitle"] .ff-btn--primary,
  body[data-ff-page="demo"] [aria-labelledby="platformDemoFounderCloseTitle"] .ff-btn--primary {
    min-width: 12.5rem;
  }

  /* -----------------------------------------------------------------------
     Subtle support-card quieting
     ----------------------------------------------------------------------- */
  body[data-ff-page="home"] [aria-label="Why FutureFunded works"] > *,
  body[data-ff-page="pricing"] #platformIncludedTitle,
  body[data-ff-page="demo"] [aria-labelledby="platformDemoFounderCloseTitle"] .ff-btn--secondary {
    filter: saturate(0.98);
  }

  /* -----------------------------------------------------------------------
     Mobile finish
     ----------------------------------------------------------------------- */
  @media (max-width: 640px) {
    body[data-ff-page="home"] #platformHomeHeroTitle,
    body[data-ff-page="pricing"] #platformPricingHeroTitle,
    body[data-ff-page="demo"] #platformDemoTitle {
      max-width: 10.6ch;
    }

    body[data-ff-page="pricing"] [aria-labelledby="platformPricingCloseTitle"] .ff-btn--primary,
    body[data-ff-page="demo"] [aria-labelledby="demoCloseTitle"] .ff-btn--primary,
    body[data-ff-page="demo"] [aria-labelledby="platformDemoFounderCloseTitle"] .ff-btn--primary {
      min-width: 0;
    }
  }
}
/* FF_PLATFORM_FLAGSHIP_FINISH_V1_END */
"""

if BLOCK_START in src and BLOCK_END in src:
    start = src.index(BLOCK_START)
    end = src.index(BLOCK_END) + len(BLOCK_END)
    updated = src[:start] + block + src[end:]
else:
    updated = src.rstrip() + "\n\n" + block + "\n"

CSS.write_text(updated, encoding="utf-8")
print("patched", CSS)
