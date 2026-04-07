from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATE = ROOT / "apps/web/app/templates/campaign/index.html"
CSS = ROOT / "apps/web/app/static/css/ff.css"
SPEC = ROOT / "tests/e2e/fundraiser-smoke.spec.ts"

for p in (TEMPLATE, CSS, SPEC):
    if not p.exists():
        raise SystemExit(f"Missing file: {p}")

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
for p in (TEMPLATE, CSS, SPEC):
    shutil.copy2(p, p.with_name(f"{p.name}.{timestamp}.bak"))

# ------------------------------------------------------------------
# 1) Restore/add rendered video modal contract to template
# ------------------------------------------------------------------
template_src = TEMPLATE.read_text(encoding="utf-8")

VIDEO_MODAL_BLOCK = """
<section
  id="press-video"
  class="ff-modal ff-modal--compact ff-modal--flagship"
  data-ff-video-modal=""
  data-open="false"
  hidden
  aria-hidden="true"
  role="dialog"
  aria-modal="true"
  aria-labelledby="videoTitle"
  aria-describedby="videoStatus"
>
  <a
    class="ff-modal__backdrop ff-modal__backdrop--flagship ff-sheet__close"
    data-ff-close-video=""
    href="#home"
    tabindex="-1"
    aria-label="Close video"
  ></a>

  <div
    class="ff-modal__panel ff-modal__panel--flagship"
    data-ff-video-panel=""
    role="document"
    tabindex="-1"
  >
    <header class="ff-modal__head ff-modal__head--flagship ff-videoModal__head">
      <div class="ff-minw-0">
        <p class="ff-kicker ff-m-0">Program video</p>
        <h2 class="ff-modal__title ff-mt-1 ff-mb-0" data-ff-video-title="" id="videoTitle">
          {{ _press_video_title|default('Watch the story', true)|e }}
        </h2>
        <p class="ff-help ff-muted ff-mt-1 ff-mb-0" data-ff-video-status="" id="videoStatus">
          Ready when you are.
        </p>
      </div>

      <button
        type="button"
        class="ff-iconbtn ff-sheet__close"
        data-ff-close-video=""
        aria-label="Close video"
      >
        <span aria-hidden="true">✕</span>
        <span class="ff-sr">Close video</span>
      </button>
    </header>

    <div class="ff-modal__body ff-videoModal__body">
      <div
        class="ff-videoModal__mount"
        data-ff-video-mount=""
        aria-live="polite"
      ></div>
    </div>
  </div>
</section>
""".strip()

if 'data-ff-video-modal=""' not in template_src:
    anchor = '<section id="terms"'
    idx = template_src.find(anchor)
    if idx == -1:
        anchor = '<section\n  id="terms"'
        idx = template_src.find(anchor)
    if idx == -1:
        raise SystemExit("Could not find terms modal anchor to insert video modal before it")
    template_src = template_src[:idx] + VIDEO_MODAL_BLOCK + "\n\n" + template_src[idx:]

TEMPLATE.write_text(template_src, encoding="utf-8")

# ------------------------------------------------------------------
# 2) Add sponsor/video modal mobile scroll safety CSS
# ------------------------------------------------------------------
css_src = CSS.read_text(encoding="utf-8")
CSS_START = "/* FF_SPONSOR_VIDEO_MODAL_SCROLL_FIX_V1_START */"
CSS_END = "/* FF_SPONSOR_VIDEO_MODAL_SCROLL_FIX_V1_END */"

CSS_BLOCK = """
/* FF_SPONSOR_VIDEO_MODAL_SCROLL_FIX_V1_START */
body[data-ff-page="fundraiser"] [data-ff-sponsor-modal],
body[data-ff-page="fundraiser"] [data-ff-video-modal] {
  align-items: flex-start;
  padding:
    clamp(0.75rem, 1.5vw, 1.25rem)
    clamp(0.75rem, 1.5vw, 1.25rem)
    max(0.75rem, env(safe-area-inset-bottom))
    clamp(0.75rem, 1.5vw, 1.25rem);
}

body[data-ff-page="fundraiser"] [data-ff-sponsor-modal] .ff-modal__panel,
body[data-ff-page="fundraiser"] [data-ff-video-modal] .ff-modal__panel {
  display: flex;
  flex-direction: column;
  min-height: 0;
  max-height: calc(100dvh - 1.5rem);
  overflow: hidden;
}

body[data-ff-page="fundraiser"] [data-ff-sponsor-modal] .ff-modal__body,
body[data-ff-page="fundraiser"] [data-ff-video-modal] .ff-modal__body {
  flex: 1 1 auto;
  min-height: 0;
  overflow: auto;
  overscroll-behavior: contain;
  -webkit-overflow-scrolling: touch;
  scrollbar-gutter: stable both-edges;
}

body[data-ff-page="fundraiser"] .ff-videoModal__mount {
  min-height: min(56dvh, 560px);
}

@media (max-width: 1023.98px) {
  body[data-ff-page="fundraiser"] [data-ff-sponsor-modal],
  body[data-ff-page="fundraiser"] [data-ff-video-modal] {
    padding:
      max(0.25rem, env(safe-area-inset-top))
      0
      max(0.25rem, env(safe-area-inset-bottom))
      0;
  }

  body[data-ff-page="fundraiser"] [data-ff-sponsor-modal] .ff-modal__panel,
  body[data-ff-page="fundraiser"] [data-ff-video-modal] .ff-modal__panel {
    width: 100%;
    max-height: 100dvh;
    border-radius: 0;
  }
}
/* FF_SPONSOR_VIDEO_MODAL_SCROLL_FIX_V1_END */
""".strip()

if CSS_START in css_src and CSS_END in css_src:
    start = css_src.index(CSS_START)
    end = css_src.index(CSS_END) + len(CSS_END)
    css_src = css_src[:start] + CSS_BLOCK + css_src[end:]
else:
    css_src = css_src.rstrip() + "\n\n" + CSS_BLOCK + "\n"

CSS.write_text(css_src, encoding="utf-8")

# ------------------------------------------------------------------
# 3) Sync Playwright fundraiser smoke spec with new architecture
# ------------------------------------------------------------------
spec_src = SPEC.read_text(encoding="utf-8")

spec_src = spec_src.replace(
    "sponsor, legal, video, and onboarding modals all open and close",
    "sponsor, legal, and video modals all open and close",
)

# Remove stale onboarding expectations from campaign-route smoke
lines = []
for line in spec_src.splitlines():
    if re.search(r'onboard|ff-onboarding|data-ff-open-onboard|data-ff-onboard-modal', line, flags=re.I):
        continue
    lines.append(line)
spec_src = "\n".join(lines)

# Minor phrase cleanup after removing onboarding lines
spec_src = spec_src.replace("video, and", "video and")
spec_src = spec_src.replace("video and legal", "legal and video")

SPEC.write_text(spec_src, encoding="utf-8")

print("== FF VIDEO + SPONSOR MODAL + PLAYWRIGHT SYNC V1 ==")
print("done.")
