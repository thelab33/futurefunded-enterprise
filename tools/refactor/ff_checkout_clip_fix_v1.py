from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/ff.css"

if not CSS.exists():
    raise SystemExit(f"Missing CSS file: {CSS}")

src = CSS.read_text(encoding="utf-8")
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = CSS.with_name(f"{CSS.name}.{timestamp}.bak")
shutil.copy2(CSS, backup)

MARKER_START = "/* FF_CHECKOUT_CLIP_FIX_V1_START */"
MARKER_END = "/* FF_CHECKOUT_CLIP_FIX_V1_END */"

BLOCK = """
/* FF_CHECKOUT_CLIP_FIX_V1_START */
body[data-ff-page="fundraiser"] .ff-sheet--checkout {
  align-items: flex-start;
  padding:
    clamp(0.75rem, 1.5vw, 1.25rem)
    clamp(0.75rem, 1.5vw, 1.25rem)
    max(0.75rem, env(safe-area-inset-bottom))
    clamp(0.75rem, 1.5vw, 1.25rem);
}

body[data-ff-page="fundraiser"] .ff-sheet--checkout [data-ff-checkout-viewport],
body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-sheet__viewport {
  width: min(100%, 1520px);
  max-height: calc(100dvh - 1.5rem);
  min-height: 0;
  overflow: hidden;
}

body[data-ff-page="fundraiser"] .ff-sheet--checkout [data-ff-checkout-shell],
body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-sheet__panel,
body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-checkoutShell {
  display: flex;
  flex-direction: column;
  min-height: 0;
  max-height: calc(100dvh - 1.5rem);
  overflow: hidden;
}

body[data-ff-page="fundraiser"] .ff-sheet--checkout [data-ff-checkout-content],
body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-sheet__content,
body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-checkoutMain,
body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-checkoutGrid {
  min-height: 0;
}

body[data-ff-page="fundraiser"] .ff-sheet--checkout [data-ff-checkout-scroll],
body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-sheet__scroll,
body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-checkoutScroll {
  flex: 1 1 auto;
  min-height: 0;
  overflow: auto;
  overscroll-behavior: contain;
  -webkit-overflow-scrolling: touch;
  scrollbar-gutter: stable both-edges;
  padding-right: clamp(0.125rem, 0.35vw, 0.5rem);
}

body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-sheet__head,
body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-modal__head {
  position: sticky;
  top: 0;
  z-index: 5;
  background: inherit;
}

body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-sheet__foot--sticky,
body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-modal__foot--sticky {
  position: sticky;
  bottom: 0;
  z-index: 5;
  background: inherit;
}

body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-checkoutMain,
body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-checkoutFormRail,
body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-checkoutAside {
  min-height: 0;
}

@media (max-width: 1023.98px) {
  body[data-ff-page="fundraiser"] .ff-sheet--checkout {
    padding:
      max(0.25rem, env(safe-area-inset-top))
      0
      max(0.25rem, env(safe-area-inset-bottom))
      0;
  }

  body[data-ff-page="fundraiser"] .ff-sheet--checkout [data-ff-checkout-viewport],
  body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-sheet__viewport,
  body[data-ff-page="fundraiser"] .ff-sheet--checkout [data-ff-checkout-shell],
  body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-sheet__panel,
  body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-checkoutShell {
    width: 100%;
    max-height: 100dvh;
    border-radius: 0;
  }

  body[data-ff-page="fundraiser"] .ff-sheet--checkout [data-ff-checkout-scroll],
  body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-sheet__scroll,
  body[data-ff-page="fundraiser"] .ff-sheet--checkout .ff-checkoutScroll {
    padding-right: 0;
  }
}
/* FF_CHECKOUT_CLIP_FIX_V1_END */
""".strip()

if MARKER_START in src and MARKER_END in src:
    start = src.index(MARKER_START)
    end = src.index(MARKER_END) + len(MARKER_END)
    updated = src[:start] + BLOCK + src[end:]
else:
    updated = src.rstrip() + "\n\n" + BLOCK + "\n"

CSS.write_text(updated, encoding="utf-8")

print("== FF CHECKOUT CLIP FIX V1 ==")
print(f"backup: {backup}")
print("done.")
