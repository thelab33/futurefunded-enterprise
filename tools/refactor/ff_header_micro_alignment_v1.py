from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/ff.css"

START = "/* FF_HEADER_MICRO_ALIGNMENT_V1_START */"
END = "/* FF_HEADER_MICRO_ALIGNMENT_V1_END */"

BLOCK = r"""
/* FF_HEADER_MICRO_ALIGNMENT_V1_START */
/* Micro-alignment pass:
   - tighten utility/nav rhythm
   - reduce floating-band feeling
   - calm donate shadow at awkward desktop widths
*/

body[data-ff-page="fundraiser"] .ff-topbar__capsule {
  padding-bottom: 0.72rem;
}

body[data-ff-page="fundraiser"] .ff-topbar__capsuleInner {
  gap: 0.62rem;
}

body[data-ff-page="fundraiser"] .ff-topbar__mainRow {
  align-items: start;
  row-gap: 0.48rem;
}

body[data-ff-page="fundraiser"] .ff-navPill,
body[data-ff-page="fundraiser"] .ff-nav--pill {
  margin-top: 0;
}

body[data-ff-page="fundraiser"] .ff-themeToggle,
body[data-ff-page="fundraiser"] .ff-donate-btn,
body[data-ff-page="fundraiser"] .ff-btn--primary {
  align-self: start;
}

body[data-ff-page="fundraiser"] .ff-donate-btn,
body[data-ff-page="fundraiser"] .ff-btn--primary {
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.12),
    0 8px 18px rgb(249 115 22 / 0.16);
}

body[data-ff-page="fundraiser"] .ff-donate-btn:hover,
body[data-ff-page="fundraiser"] .ff-donate-btn:focus-visible,
body[data-ff-page="fundraiser"] .ff-btn--primary:hover,
body[data-ff-page="fundraiser"] .ff-btn--primary:focus-visible {
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.14),
    0 10px 22px rgb(249 115 22 / 0.18);
}

@media (max-width: 78rem) and (min-width: 64rem) {
  body[data-ff-page="fundraiser"] .ff-topbar__capsule {
    padding-bottom: 0.66rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbar__capsuleInner {
    gap: 0.54rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbar__mainRow {
    row-gap: 0.38rem;
  }

  body[data-ff-page="fundraiser"] .ff-navPill,
  body[data-ff-page="fundraiser"] .ff-nav--pill {
    margin-top: -0.04rem;
  }

  body[data-ff-page="fundraiser"] .ff-themeToggle {
    transform: translateY(0.02rem);
  }

  body[data-ff-page="fundraiser"] .ff-donate-btn,
  body[data-ff-page="fundraiser"] .ff-btn--primary {
    transform: translateY(0.02rem);
    box-shadow:
      inset 0 1px 0 rgb(255 255 255 / 0.12),
      0 7px 16px rgb(249 115 22 / 0.14);
  }

  body[data-ff-page="fundraiser"] .ff-nav__link {
    min-height: 2rem;
  }
}

html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-donate-btn,
html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-btn--primary {
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.1),
    0 8px 18px rgb(249 115 22 / 0.13);
}

html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-donate-btn:hover,
html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-donate-btn:focus-visible,
html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-btn--primary:hover,
html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-btn--primary:focus-visible {
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.12),
    0 10px 22px rgb(249 115 22 / 0.16);
}
/* FF_HEADER_MICRO_ALIGNMENT_V1_END */
""".strip() + "\n"

text = CSS.read_text(encoding="utf-8")

if START in text and END in text:
    text = re.sub(
        re.escape(START) + r".*?" + re.escape(END),
        BLOCK.strip(),
        text,
        flags=re.S,
    )
else:
    text = text.rstrip() + "\n\n" + BLOCK

backup = CSS.with_suffix(CSS.suffix + f".bak.{datetime.now().strftime('%Y%m%d-%H%M%S')}")
backup.write_text(CSS.read_text(encoding="utf-8"), encoding="utf-8")
CSS.write_text(text.rstrip() + "\n", encoding="utf-8")

print("✅ patched", CSS)
print("🗂 backup ", backup)
print("✅ applied FF_HEADER_MICRO_ALIGNMENT_V1")
