from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/ff.css"

START = "/* FF_MEDIA_RECOVERY_V1_START */"
END = "/* FF_MEDIA_RECOVERY_V1_END */"

BLOCK = r"""
/* FF_MEDIA_RECOVERY_V1_START */
/* Restore visible campaign media while preserving prestige surfaces. */

body[data-ff-page="fundraiser"] .ff-teamCard__media,
body[data-ff-page="fundraiser"] .ff-storyPoster,
body[data-ff-page="fundraiser"] .ff-videoFrame {
  position: relative;
  overflow: hidden;
  isolation: isolate;
}

body[data-ff-page="fundraiser"] .ff-teamCard__img,
body[data-ff-page="fundraiser"] .ff-storyPoster__img,
body[data-ff-page="fundraiser"] .ff-storyPoster__picture img,
body[data-ff-page="fundraiser"] .ff-videoMount iframe,
body[data-ff-page="fundraiser"] .ff-videoMount video {
  display: block;
  width: 100%;
  height: 100%;
  opacity: 1 !important;
  visibility: visible !important;
}

body[data-ff-page="fundraiser"] .ff-teamCard__img,
body[data-ff-page="fundraiser"] .ff-storyPoster__img,
body[data-ff-page="fundraiser"] .ff-storyPoster__picture img {
  object-fit: cover;
  position: relative;
  z-index: 1;
}

body[data-ff-page="fundraiser"] .ff-videoMount iframe,
body[data-ff-page="fundraiser"] .ff-videoMount video {
  border: 0;
  position: relative;
  z-index: 1;
}

body[data-ff-page="fundraiser"] .ff-teamCard__media::before,
body[data-ff-page="fundraiser"] .ff-storyPoster::before,
body[data-ff-page="fundraiser"] .ff-videoFrame::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  background:
    radial-gradient(circle at top right, rgb(14 165 233 / 0.06), transparent 38%),
    linear-gradient(180deg, rgb(255 255 255 / 0.04), rgb(255 255 255 / 0));
}

body[data-ff-page="fundraiser"] .ff-storyPoster__overlay {
  z-index: 2;
}

html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-teamCard__media,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-storyPoster,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-videoFrame {
  background:
    linear-gradient(180deg, rgb(255 255 255 / 0.02), rgb(255 255 255 / 0)),
    rgb(8 15 28 / 0.92) !important;
}

html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-teamCard__media::before,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-storyPoster::before,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-videoFrame::before {
  background:
    radial-gradient(circle at top right, rgb(14 165 233 / 0.08), transparent 38%),
    linear-gradient(180deg, rgb(255 255 255 / 0.025), rgb(255 255 255 / 0));
}

html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-teamCard__img,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-storyPoster__img,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-storyPoster__picture img,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-videoMount iframe,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-videoMount video {
  filter: none !important;
  mix-blend-mode: normal !important;
}

@media (max-width: 47.99rem) {
  body[data-ff-page="fundraiser"] .ff-teamCard__media,
  body[data-ff-page="fundraiser"] .ff-storyPoster,
  body[data-ff-page="fundraiser"] .ff-videoFrame {
    min-height: 11.5rem;
  }
}
/* FF_MEDIA_RECOVERY_V1_END */
""".strip() + "\n"

def backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = path.with_name(path.name + f".bak.{stamp}")
    shutil.copy2(path, bak)
    return bak

def main() -> None:
    if not CSS.exists():
        raise SystemExit(f"❌ missing css file: {CSS}")

    orig = CSS.read_text(encoding="utf-8")

    if START in orig and END in orig:
        updated = re.sub(
            re.escape(START) + r".*?" + re.escape(END),
            BLOCK.strip(),
            orig,
            flags=re.S,
        )
    else:
        marker = "/* ==========================================================================\n   UTILITIES + RESPONSIVE\n   ========================================================================== */"
        idx = orig.find(marker)
        if idx == -1:
            updated = orig.rstrip() + "\n\n" + BLOCK
        else:
            updated = orig[:idx].rstrip() + "\n\n" + BLOCK + "\n\n" + orig[idx:]

    if updated == orig:
        print("== FF CSS MEDIA RECOVERY V1 ==")
        print("✔ no changes needed")
        raise SystemExit(0)

    bak = backup(CSS)
    CSS.write_text(updated, encoding="utf-8")

    print("== FF CSS MEDIA RECOVERY V1 ==")
    print(f"✅ patched css : {CSS}")
    print(f"🛟 backup      : {bak}")
    print("done:")
    print(" - restored team/story/video media visibility")
    print(" - preserved dark-mode prestige surfaces")
    print(" - added safe mobile media minimum height")
    print(f"marker start   : {START}")
    print(f"marker end     : {END}")

if __name__ == "__main__":
    main()
