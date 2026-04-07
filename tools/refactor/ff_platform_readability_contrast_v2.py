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

BLOCK_START = "/* FF_PLATFORM_READABILITY_CONTRAST_V2_START */"
BLOCK_END = "/* FF_PLATFORM_READABILITY_CONTRAST_V2_END */"

block = r"""
/* FF_PLATFORM_READABILITY_CONTRAST_V2_START */
@layer ff.pages {
  body[data-ff-template="platform"] .ff-help,
  body[data-ff-template="platform"] .ff-help.ff-muted,
  body[data-ff-template="platform"] .ff-muted {
    color: rgba(224, 232, 244, 0.92);
    font-size: 1rem;
    line-height: 1.66;
  }

  body[data-ff-template="platform"] .ff-kicker,
  body[data-ff-template="platform"] .ff-label,
  body[data-ff-template="platform"] .ff-platformBrand__subline {
    color: rgba(202, 214, 231, 0.92);
  }

  body[data-ff-template="platform"] .ff-proofMini,
  body[data-ff-template="platform"] .ff-card.ff-glass .ff-proofMini {
    border-color: rgba(255, 255, 255, 0.14);
    background:
      linear-gradient(180deg, rgba(24, 42, 84, 0.9), rgba(9, 19, 42, 0.97));
  }

  body[data-ff-template="platform"] .ff-card.ff-glass .ff-help,
  body[data-ff-template="platform"] .ff-proofMini .ff-help {
    color: rgba(232, 239, 248, 0.94);
  }

  body[data-ff-template="platform"] .ff-lead {
    color: rgba(239, 245, 252, 0.96);
  }

  body[data-ff-template="platform"] .ff-btn.ff-btn--secondary,
  body[data-ff-template="platform"] .ff-btn.ff-btn--pill.ff-btn--secondary {
    color: #f4f8ff;
    border-color: rgba(255, 255, 255, 0.15);
  }

  body[data-ff-template="platform"] .ff-card.ff-glass p,
  body[data-ff-template="platform"] .ff-proofMini p {
    max-width: 60ch;
  }

  @media (max-width: 640px) {
    body[data-ff-template="platform"] .ff-help,
    body[data-ff-template="platform"] .ff-help.ff-muted,
    body[data-ff-template="platform"] .ff-muted {
      font-size: 0.99rem;
      line-height: 1.68;
    }
  }
}
/* FF_PLATFORM_READABILITY_CONTRAST_V2_END */
"""

if BLOCK_START in src and BLOCK_END in src:
    start = src.index(BLOCK_START)
    end = src.index(BLOCK_END) + len(BLOCK_END)
    updated = src[:start] + block + src[end:]
else:
    updated = src.rstrip() + "\n\n" + block + "\n"

CSS.write_text(updated, encoding="utf-8")
print("patched", CSS)
