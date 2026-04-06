from __future__ import annotations

from pathlib import Path
from datetime import datetime

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/ff.css"

text = CSS.read_text(encoding="utf-8")
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = ROOT / "backups" / f"ff.css.contract_gap_patch_v1.{stamp}.bak"
backup.write_text(text, encoding="utf-8")

start = "/* FF_CONTRACT_GAP_PATCH_V1_START */"
end = "/* FF_CONTRACT_GAP_PATCH_V1_END */"

patch = r"""
/* FF_CONTRACT_GAP_PATCH_V1_START */
@layer ff.utilities {
  .ff-checkoutContent,
  .ff-checkoutScroll,
  .ff-checkoutStage,
  .ff-modal--video,
  .ff-onboardModal__footer,
  .ff-sectionhead__text,
  .ff-sponsorModal__footer,
  .ff-teamsEmpty,
  .ff-themeToggle--desktop,
  .ff-topbarBrand--flagship,
  .ff-topbarGoal__metaRow,
  .ff-topbar__brandCluster,
  .ff-topbar__desktopActions,
  .ff-topbar__rightCluster {
    min-width: 0;
  }

  .ff-topbarBrand--flagship {
    display: inline-flex;
    align-items: center;
    gap: 0.72rem;
    min-width: 0;
  }

  .ff-topbar__brandCluster,
  .ff-topbar__rightCluster {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.72rem;
    min-width: 0;
  }

  .ff-topbar__brandCluster {
    flex: 1 1 auto;
  }

  .ff-topbar__rightCluster {
    justify-content: flex-start;
  }

  .ff-topbar__desktopActions {
    display: none;
    align-items: center;
    justify-content: flex-end;
    gap: 0.6rem;
  }

  .ff-topbarGoal__metaRow {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
  }

  .ff-themeToggle--desktop {
    display: none;
    flex: 0 0 auto;
  }

  .ff-sectionhead__text {
    display: grid;
    gap: 0.32rem;
    min-width: 0;
  }

  .ff-teamsEmpty {
    display: grid;
    gap: 0.72rem;
    padding: 1rem 1.05rem;
    border: 1px dashed var(--ff-border-strong);
    border-radius: var(--ff-radius-3);
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.06), rgb(255 255 255 / 0)),
      var(--ff-panel);
    text-wrap: pretty;
    box-shadow: var(--ff-shadow-1);
  }

  .ff-checkoutContent,
  .ff-checkoutStage {
    display: grid;
    gap: 1rem;
    align-content: start;
  }

  .ff-checkoutScroll {
    display: grid;
    gap: 1rem;
    max-height: inherit;
    overflow: auto;
    -webkit-overflow-scrolling: touch;
    overscroll-behavior: contain;
    scrollbar-gutter: stable;
  }

  .ff-modal--video {
    isolation: isolate;
  }

  .ff-modal--video .ff-modal__panel {
    width: min(100%, 62rem);
  }

  .ff-modal--video .ff-modal__body {
    display: grid;
    gap: 0.9rem;
  }

  .ff-sponsorModal__footer,
  .ff-onboardModal__footer {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    padding-top: 0.8rem;
    border-top: 1px solid var(--ff-line);
  }

  .ff-sponsorModal__footer > *,
  .ff-onboardModal__footer > * {
    min-width: 0;
  }

  html.ff-root[data-theme="dark"] .ff-teamsEmpty {
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.035), rgb(255 255 255 / 0)),
      var(--ff-panel-strong);
  }

  html.ff-root[data-theme="dark"] .ff-sponsorModal__footer,
  html.ff-root[data-theme="dark"] .ff-onboardModal__footer {
    border-top-color: rgb(226 232 240 / 0.1);
  }

  @media (min-width: 64rem) {
    .ff-topbar__desktopActions,
    .ff-themeToggle--desktop {
      display: inline-flex;
    }

    .ff-topbar__rightCluster {
      justify-content: flex-end;
      margin-left: auto;
    }
  }

  @media (max-width: 63.99rem) {
    .ff-topbar__rightCluster {
      width: 100%;
      justify-content: space-between;
    }

    .ff-sponsorModal__footer,
    .ff-onboardModal__footer {
      align-items: stretch;
    }

    .ff-sponsorModal__footer > *,
    .ff-onboardModal__footer > * {
      flex: 1 1 calc(50% - 0.375rem);
    }
  }
}
/* FF_CONTRACT_GAP_PATCH_V1_END */
""".strip() + "\n"

if start in text and end in text:
    before = text.split(start, 1)[0]
    after = text.split(end, 1)[1]
    text = before + patch + after
    mode = "updated existing patch block"
else:
    text = text.rstrip() + "\n\n" + patch
    mode = "appended new patch block"

CSS.write_text(text, encoding="utf-8")

print("== FF CSS CONTRACT GAP PATCH V1 ==")
print(f"backup : {backup}")
print(f"target : {CSS}")
print(f"result : {mode}")
