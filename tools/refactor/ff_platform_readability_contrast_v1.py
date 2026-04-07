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

BLOCK_START = "/* FF_PLATFORM_READABILITY_CONTRAST_V1_START */"
BLOCK_END = "/* FF_PLATFORM_READABILITY_CONTRAST_V1_END */"

block = r"""
/* FF_PLATFORM_READABILITY_CONTRAST_V1_START */
@layer ff.pages {
  body[data-ff-template="platform"] .ff-display,
  body[data-ff-template="platform"] .ff-h2,
  body[data-ff-template="platform"] .ff-h3 {
    color: #fbfdff;
    text-shadow: 0 1px 0 rgba(255, 255, 255, 0.03);
  }

  body[data-ff-template="platform"] .ff-lead {
    color: rgba(232, 240, 250, 0.94);
    line-height: 1.62;
  }

  body[data-ff-template="platform"] .ff-help,
  body[data-ff-template="platform"] .ff-help.ff-muted,
  body[data-ff-template="platform"] .ff-muted {
    color: rgba(214, 224, 238, 0.88);
    line-height: 1.62;
    text-wrap: pretty;
  }

  body[data-ff-template="platform"] .ff-kicker,
  body[data-ff-template="platform"] .ff-label,
  body[data-ff-template="platform"] .ff-platformBrand__subline {
    color: rgba(192, 206, 224, 0.88);
    letter-spacing: 0.07em;
  }

  body[data-ff-template="platform"] .ff-card.ff-glass,
  body[data-ff-template="platform"] .ff-proofMini,
  body[data-ff-template="platform"] [data-ff-platform-trust] {
    border-color: rgba(255, 255, 255, 0.13);
  }

  body[data-ff-template="platform"] .ff-card.ff-glass {
    background:
      linear-gradient(180deg, rgba(19, 35, 71, 0.9), rgba(7, 15, 34, 0.97));
  }

  body[data-ff-template="platform"] .ff-proofMini {
    background:
      linear-gradient(180deg, rgba(22, 39, 78, 0.86), rgba(8, 18, 39, 0.96));
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.04),
      0 10px 22px rgba(2, 6, 23, 0.18);
  }

  body[data-ff-template="platform"] .ff-card.ff-glass .ff-help,
  body[data-ff-template="platform"] .ff-proofMini .ff-help {
    color: rgba(224, 233, 245, 0.9);
  }

  body[data-ff-template="platform"] .ff-nav.ff-nav--pill .ff-nav__link {
    color: rgba(235, 243, 252, 0.9);
    font-weight: 700;
  }

  body[data-ff-template="platform"] .ff-nav.ff-nav--pill .ff-nav__link[aria-current="page"] {
    color: #fff;
    box-shadow:
      inset 0 0 0 1px rgba(255, 255, 255, 0.08),
      0 10px 24px rgba(2, 6, 23, 0.24);
  }

  body[data-ff-template="platform"] .ff-btn.ff-btn--secondary,
  body[data-ff-template="platform"] .ff-btn.ff-btn--pill.ff-btn--secondary {
    color: #eef5ff;
    border-color: rgba(255, 255, 255, 0.13);
    background:
      linear-gradient(180deg, rgba(255, 255, 255, 0.09), rgba(255, 255, 255, 0)),
      rgba(16, 29, 57, 0.92);
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.04),
      0 8px 20px rgba(2, 6, 23, 0.16);
  }

  body[data-ff-template="platform"] .ff-platformInlinePill,
  body[data-ff-template="platform"] .ff-platformStatPill {
    color: rgba(239, 246, 255, 0.96);
    border-color: rgba(255, 255, 255, 0.12);
  }

  body[data-ff-template="platform"] .ff-card.ff-glass p,
  body[data-ff-template="platform"] .ff-proofMini p {
    max-width: 62ch;
  }

  @media (max-width: 640px) {
    body[data-ff-template="platform"] .ff-help,
    body[data-ff-template="platform"] .ff-help.ff-muted,
    body[data-ff-template="platform"] .ff-muted {
      font-size: 0.98rem;
      line-height: 1.64;
    }

    body[data-ff-template="platform"] .ff-kicker,
    body[data-ff-template="platform"] .ff-label {
      font-size: 0.76rem;
    }
  }
}
/* FF_PLATFORM_READABILITY_CONTRAST_V1_END */
"""

if BLOCK_START in src and BLOCK_END in src:
    start = src.index(BLOCK_START)
    end = src.index(BLOCK_END) + len(BLOCK_END)
    updated = src[:start] + block + src[end:]
else:
    updated = src.rstrip() + "\n\n" + block + "\n"

CSS.write_text(updated, encoding="utf-8")
print("patched", CSS)
