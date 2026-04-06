from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/ff.css"

START = "/* FF_STORY_POSTER_RENDER_FIX_V1_START */"
END = "/* FF_STORY_POSTER_RENDER_FIX_V1_END */"

BLOCK = r"""
/* FF_STORY_POSTER_RENDER_FIX_V1_START */
/* Force the story poster media path to paint like the healthy team cards. */

body[data-ff-page="fundraiser"] .ff-storyPoster,
body[data-ff-page="fundraiser"] .ff-storyPoster__picture,
body[data-ff-page="fundraiser"] .ff-storyPoster__img {
  display: block;
  visibility: visible !important;
  opacity: 1 !important;
}

body[data-ff-page="fundraiser"] .ff-storyPoster {
  position: relative;
  overflow: hidden;
  isolation: isolate;
  background:
    radial-gradient(circle at top right, rgb(14 165 233 / 0.08), transparent 40%),
    linear-gradient(180deg, rgb(255 255 255 / 0.04), rgb(15 23 42 / 0.05));
}

body[data-ff-page="fundraiser"] .ff-storyPoster__picture {
  position: relative;
  inline-size: 100%;
  block-size: 100%;
  min-inline-size: 100%;
  min-block-size: 100%;
}

body[data-ff-page="fundraiser"] .ff-storyPoster__picture source {
  display: none;
}

body[data-ff-page="fundraiser"] .ff-storyPoster__img {
  position: relative;
  z-index: 1;
  inline-size: 100%;
  block-size: 100%;
  min-inline-size: 100%;
  min-block-size: 100%;
  inline-size: 100%;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center center;
  image-rendering: auto;
  transform: translateZ(0);
  backface-visibility: hidden;
}

body[data-ff-page="fundraiser"] .ff-storyPoster__overlay {
  position: absolute;
  inset: 0;
  z-index: 2;
  pointer-events: none;
}

html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-storyPoster {
  background:
    radial-gradient(circle at top right, rgb(14 165 233 / 0.12), transparent 40%),
    linear-gradient(180deg, rgb(255 255 255 / 0.03), rgb(255 255 255 / 0));
}
/* FF_STORY_POSTER_RENDER_FIX_V1_END */
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
print("✅ applied FF_STORY_POSTER_RENDER_FIX_V1")
