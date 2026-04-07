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

BLOCK_START = "/* FF_PLATFORM_SURFACE_PARITY_V1_START */"
BLOCK_END = "/* FF_PLATFORM_SURFACE_PARITY_V1_END */"

block = r"""
/* FF_PLATFORM_SURFACE_PARITY_V1_START */
@layer ff.pages {
  body[data-ff-template="platform"] {
    --ff-platform-copy-strong: var(--ff-text);
    --ff-platform-copy: var(--ff-text-soft);
    --ff-platform-copy-muted: var(--ff-text-muted);
    --ff-platform-copy-faint: var(--ff-text-faint);
  }

  body[data-ff-template="platform"] .ff-card.ff-glass,
  body[data-ff-template="platform"] [data-ff-platform-trust] {
    border-color: var(--ff-border-strong);
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.04), rgb(255 255 255 / 0)),
      var(--ff-panel-strong);
    box-shadow: var(--ff-shadow-2);
  }

  body[data-ff-template="platform"] .ff-proofMini,
  body[data-ff-template="platform"] .ff-platformInlinePill,
  body[data-ff-template="platform"] .ff-platformStatPill {
    border-color: var(--ff-border);
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.028), rgb(255 255 255 / 0)),
      var(--ff-panel);
    box-shadow: var(--ff-shadow-1);
  }

  body[data-ff-template="platform"] .ff-card.ff-glass .ff-proofMini {
    box-shadow:
      inset 0 1px 0 rgb(255 255 255 / 0.03),
      0 10px 24px rgb(0 0 0 / 0.22);
  }

  body[data-ff-template="platform"] .ff-display,
  body[data-ff-template="platform"] .ff-h2,
  body[data-ff-template="platform"] .ff-h3 {
    color: var(--ff-platform-copy-strong);
    text-shadow: none;
  }

  body[data-ff-template="platform"] .ff-lead {
    color: var(--ff-platform-copy);
    line-height: 1.64;
    max-width: 52ch;
  }

  body[data-ff-template="platform"] .ff-help,
  body[data-ff-template="platform"] .ff-help.ff-muted,
  body[data-ff-template="platform"] .ff-muted {
    color: var(--ff-platform-copy-muted);
    line-height: 1.62;
    text-wrap: pretty;
  }

  body[data-ff-template="platform"] .ff-card.ff-glass .ff-help,
  body[data-ff-template="platform"] .ff-card.ff-glass .ff-muted,
  body[data-ff-template="platform"] .ff-proofMini .ff-help,
  body[data-ff-template="platform"] .ff-proofMini .ff-muted {
    color: var(--ff-platform-copy);
  }

  body[data-ff-template="platform"] .ff-kicker,
  body[data-ff-template="platform"] .ff-label,
  body[data-ff-template="platform"] .ff-proofMini .ff-kicker,
  body[data-ff-template="platform"] .ff-platformBrand__subline {
    color: var(--ff-platform-copy-faint);
  }

  body[data-ff-template="platform"] .ff-btn.ff-btn--secondary,
  body[data-ff-template="platform"] .ff-btn.ff-btn--pill.ff-btn--secondary {
    color: var(--ff-platform-copy-strong);
    border-color: var(--ff-border-strong);
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.05), rgb(255 255 255 / 0)),
      var(--ff-panel);
    box-shadow: var(--ff-shadow-1);
  }

  body[data-ff-template="platform"] .ff-nav.ff-nav--pill .ff-nav__link {
    color: var(--ff-platform-copy);
  }

  body[data-ff-template="platform"] .ff-nav.ff-nav--pill .ff-nav__link[aria-current="page"] {
    color: var(--ff-platform-copy-strong);
  }

  body[data-ff-template="platform"] .ff-card.ff-glass p,
  body[data-ff-template="platform"] .ff-proofMini p {
    max-width: 58ch;
  }
}
/* FF_PLATFORM_SURFACE_PARITY_V1_END */
"""

if BLOCK_START in src and BLOCK_END in src:
    start = src.index(BLOCK_START)
    end = src.index(BLOCK_END) + len(BLOCK_END)
    updated = src[:start] + block + src[end:]
else:
    updated = src.rstrip() + "\n\n" + block + "\n"

CSS.write_text(updated, encoding="utf-8")
print("patched", CSS)
