from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/ff.css"

START = "/* FF_HEADER_ROW_COLLISION_FIX_V1_START */"
END = "/* FF_HEADER_ROW_COLLISION_FIX_V1_END */"

BLOCK = r"""
/* FF_HEADER_ROW_COLLISION_FIX_V1_START */
/* Fix topbar/nav/theme/donate crowding in awkward desktop-mid widths. */

body[data-ff-page="fundraiser"] .ff-topbar__mainRow {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  flex-wrap: wrap;
}

body[data-ff-page="fundraiser"] .ff-topbarBrand {
  flex: 0 1 auto;
  min-width: 0;
}

body[data-ff-page="fundraiser"] .ff-topbar__desktop-only {
  min-width: 0;
}

body[data-ff-page="fundraiser"] .ff-navPill,
body[data-ff-page="fundraiser"] .ff-nav--pill {
  flex: 1 1 auto;
  min-width: 0;
  max-width: 100%;
}

body[data-ff-page="fundraiser"] .ff-nav--pill {
  display: flex;
  align-items: center;
  flex-wrap: nowrap;
  overflow-x: auto;
  scrollbar-width: none;
}

body[data-ff-page="fundraiser"] .ff-nav--pill::-webkit-scrollbar {
  display: none;
}

body[data-ff-page="fundraiser"] .ff-nav__link {
  flex: 0 0 auto;
  white-space: nowrap;
}

body[data-ff-page="fundraiser"] .ff-themeToggle {
  flex: 0 0 auto;
  min-inline-size: 2.45rem;
  inline-size: auto;
  padding-inline: 0.72rem;
  white-space: nowrap;
}

body[data-ff-page="fundraiser"] .ff-themeToggle__label {
  display: inline;
  white-space: nowrap;
}

body[data-ff-page="fundraiser"] .ff-donate-btn,
body[data-ff-page="fundraiser"] .ff-btn--primary,
body[data-ff-page="fundraiser"] .ff-tab--cta {
  flex: 0 0 auto;
  white-space: nowrap;
}

body[data-ff-page="fundraiser"] .ff-topbarGoal {
  width: 100%;
}

@media (max-width: 78rem) and (min-width: 64rem) {
  body[data-ff-page="fundraiser"] .ff-topbar__mainRow {
    gap: 0.62rem;
  }

  body[data-ff-page="fundraiser"] .ff-navPill,
  body[data-ff-page="fundraiser"] .ff-nav--pill {
    flex: 1 1 100%;
    order: 3;
  }

  body[data-ff-page="fundraiser"] .ff-topbarBrand {
    order: 1;
  }

  body[data-ff-page="fundraiser"] .ff-themeToggle {
    order: 2;
    min-inline-size: 2.35rem;
    padding-inline: 0.66rem;
  }

  body[data-ff-page="fundraiser"] .ff-themeToggle__label {
    display: none;
  }

  body[data-ff-page="fundraiser"] .ff-donate-btn,
  body[data-ff-page="fundraiser"] .ff-btn--primary {
    order: 2;
  }

  body[data-ff-page="fundraiser"] .ff-nav__link {
    font-size: 0.9rem;
    padding-inline: 0.66rem;
  }
}

@media (min-width: 64rem) {
  body[data-ff-page="fundraiser"] .ff-topbar__mobile-only {
    display: none !important;
  }

  body[data-ff-page="fundraiser"] .ff-topbar__desktop-only {
    display: block !important;
  }
}

@media (max-width: 63.99rem) {
  body[data-ff-page="fundraiser"] .ff-topbar__desktop-only {
    display: none !important;
  }

  body[data-ff-page="fundraiser"] .ff-topbar__mobile-only {
    display: flex !important;
  }
}
/* FF_HEADER_ROW_COLLISION_FIX_V1_END */
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
print("✅ applied FF_HEADER_ROW_COLLISION_FIX_V1")
