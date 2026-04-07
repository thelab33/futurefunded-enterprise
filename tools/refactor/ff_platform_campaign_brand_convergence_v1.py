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

BLOCK_START = "/* FF_PLATFORM_CAMPAIGN_BRAND_CONVERGENCE_V1_START */"
BLOCK_END = "/* FF_PLATFORM_CAMPAIGN_BRAND_CONVERGENCE_V1_END */"

block = r"""
/* FF_PLATFORM_CAMPAIGN_BRAND_CONVERGENCE_V1_START */
@layer ff.pages {
  body[data-ff-template="platform"] {
    --ff-platform-border: rgba(255, 255, 255, 0.1);
    --ff-platform-border-strong: rgba(255, 255, 255, 0.16);

    --ff-platform-bg-top: rgba(14, 28, 58, 0.84);
    --ff-platform-bg-bottom: rgba(6, 14, 31, 0.96);

    --ff-platform-bg-soft-top: rgba(15, 31, 63, 0.68);
    --ff-platform-bg-soft-bottom: rgba(7, 15, 34, 0.9);

    --ff-platform-shadow: 0 20px 52px rgba(2, 6, 23, 0.34);
    --ff-platform-shadow-soft: 0 12px 30px rgba(2, 6, 23, 0.24);
    --ff-platform-blur: 18px;
  }

  body[data-ff-template="platform"] .ff-shellBg {
    background:
      radial-gradient(circle at 8% 0%, rgba(14, 165, 233, 0.17), transparent 34%),
      radial-gradient(circle at 100% 0%, rgba(249, 115, 22, 0.2), transparent 28%),
      radial-gradient(circle at 50% 100%, rgba(14, 165, 233, 0.09), transparent 36%),
      linear-gradient(180deg, rgba(4, 11, 24, 0.34), rgba(4, 10, 22, 0.1));
  }

  body[data-ff-template="platform"] [data-ff-platform-trust],
  body[data-ff-template="platform"] .ff-card.ff-glass,
  body[data-ff-template="platform"] .ff-proofMini {
    border-color: rgba(255, 255, 255, 0.12);
    box-shadow: var(--ff-platform-shadow);
  }

  body[data-ff-template="platform"] [data-ff-platform-trust],
  body[data-ff-template="platform"] .ff-card.ff-glass {
    background:
      linear-gradient(180deg, rgba(18, 34, 70, 0.84), rgba(7, 15, 34, 0.96));
  }

  body[data-ff-template="platform"] .ff-proofMini {
    background:
      linear-gradient(180deg, rgba(20, 36, 74, 0.74), rgba(8, 17, 37, 0.94));
  }

  body[data-ff-template="platform"] .ff-display,
  body[data-ff-template="platform"] .ff-h2,
  body[data-ff-template="platform"] .ff-h3 {
    color: #f7fbff;
    text-shadow: 0 1px 0 rgba(255, 255, 255, 0.03);
  }

  body[data-ff-template="platform"] .ff-lead {
    color: rgba(223, 233, 247, 0.88);
  }

  body[data-ff-template="platform"] .ff-help.ff-muted,
  body[data-ff-template="platform"] .ff-help,
  body[data-ff-template="platform"] .ff-muted {
    color: rgba(203, 215, 232, 0.82);
  }

  body[data-ff-template="platform"] .ff-kicker,
  body[data-ff-template="platform"] .ff-label {
    color: rgba(182, 196, 216, 0.84);
  }

  body[data-ff-template="platform"] .ff-platformInlinePill,
  body[data-ff-template="platform"] .ff-platformStatPill {
    border-color: rgba(14, 165, 233, 0.18);
    background:
      linear-gradient(180deg, rgba(14, 165, 233, 0.12), rgba(249, 115, 22, 0.08));
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.04),
      0 8px 18px rgba(2, 6, 23, 0.16);
    color: rgba(237, 244, 255, 0.96);
  }

  body[data-ff-template="platform"] .ff-navPill,
  body[data-ff-template="platform"] .ff-nav.ff-nav--pill {
    border: 1px solid rgba(255, 255, 255, 0.08);
    background:
      linear-gradient(180deg, rgba(14, 25, 47, 0.72), rgba(10, 18, 36, 0.92));
  }

  body[data-ff-template="platform"] .ff-nav.ff-nav--pill .ff-nav__link {
    color: rgba(223, 233, 247, 0.88);
  }

  body[data-ff-template="platform"] .ff-nav.ff-nav--pill .ff-nav__link[aria-current="page"] {
    color: #fff;
    background:
      linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0)),
      linear-gradient(180deg, rgba(249, 115, 22, 0.22), rgba(14, 165, 233, 0.14));
    box-shadow:
      inset 0 0 0 1px rgba(255, 255, 255, 0.08),
      0 10px 24px rgba(2, 6, 23, 0.22);
  }

  body[data-ff-template="platform"] .ff-btn.ff-btn--pill.ff-btn--primary,
  body[data-ff-template="platform"] .ff-btn.ff-btn--primary {
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.14),
      0 12px 26px rgba(249, 115, 22, 0.24);
  }

  body[data-ff-template="platform"] .ff-platformBrand__disc {
    overflow: hidden;
    border-color: rgba(255, 255, 255, 0.12);
    background:
      radial-gradient(circle at 30% 25%, rgba(255, 255, 255, 0.18), transparent 52%),
      linear-gradient(180deg, rgba(16, 29, 57, 0.9), rgba(7, 15, 34, 0.96));
    box-shadow:
      0 0 0 1px rgba(255, 255, 255, 0.08),
      0 12px 28px rgba(249, 115, 22, 0.18);
  }

  body[data-ff-template="platform"] .ff-platformBrand__logo {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: inherit;
  }
}
/* FF_PLATFORM_CAMPAIGN_BRAND_CONVERGENCE_V1_END */
"""

if BLOCK_START in src and BLOCK_END in src:
    start = src.index(BLOCK_START)
    end = src.index(BLOCK_END) + len(BLOCK_END)
    updated = src[:start] + block + src[end:]
else:
    updated = src.rstrip() + "\n\n" + block + "\n"

CSS.write_text(updated, encoding="utf-8")
print("Patched:", CSS)
