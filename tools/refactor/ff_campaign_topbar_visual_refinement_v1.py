from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re

ROOT = Path.home() / "futurefunded-enterprise"

CSS_CANDIDATES = [
    ROOT / "apps/web/app/static/css/ff-above-main-premium.css",
    ROOT / "apps/web/app/static/css/ff.css",
]

CSS = next((p for p in CSS_CANDIDATES if p.exists()), None)
if CSS is None:
    raise SystemExit("❌ Could not find ff-above-main-premium.css or ff.css")

START = "/* FF_TOPBAR_VISUAL_REFINEMENT_V1_START */"
END = "/* FF_TOPBAR_VISUAL_REFINEMENT_V1_END */"

BLOCK = r"""
/* FF_TOPBAR_VISUAL_REFINEMENT_V1_START */
body[data-ff-page="fundraiser"] .ff-topbar {
  padding-top: 0.5rem;
}

body[data-ff-page="fundraiser"] .ff-topbar__capsule--flagship {
  border-radius: 2rem;
  padding: 0.4rem;
  border: 1px solid rgb(148 163 184 / 0.16);
  background:
    linear-gradient(180deg, rgb(255 255 255 / 0.9), rgb(255 255 255 / 0.82));
  box-shadow:
    0 18px 44px rgb(15 23 42 / 0.08),
    inset 0 1px 0 rgb(255 255 255 / 0.72);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
}

body[data-ff-page="fundraiser"] .ff-topbar__capsuleInner {
  gap: 0.85rem;
}

body[data-ff-page="fundraiser"] .ff-topbar__mainRow {
  gap: 0.85rem;
  align-items: center;
}

body[data-ff-page="fundraiser"] .ff-topbar__brandCluster,
body[data-ff-page="fundraiser"] .ff-topbar__rightCluster,
body[data-ff-page="fundraiser"] .ff-topbar__desktopActions {
  gap: 0.7rem;
}

body[data-ff-page="fundraiser"] .ff-topbarBrand--flagship {
  min-height: 3.25rem;
  padding: 0.38rem 0.5rem;
  border-radius: 1rem;
}

body[data-ff-page="fundraiser"] .ff-topbarBrand__logo {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 999px;
  box-shadow: 0 6px 14px rgb(15 23 42 / 0.08);
}

body[data-ff-page="fundraiser"] .ff-topbarBrand__text {
  font-weight: 800;
  letter-spacing: -0.015em;
}

body[data-ff-page="fundraiser"] .ff-topbarBrand__sub {
  font-size: 0.92rem;
}

body[data-ff-page="fundraiser"] .ff-navPill.ff-nav--pill {
  min-height: 3.25rem;
  padding: 0.28rem;
  border-radius: 999px;
  border: 1px solid rgb(148 163 184 / 0.16);
  background:
    linear-gradient(180deg, rgb(255 255 255 / 0.92), rgb(255 255 255 / 0.78));
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.7),
    0 8px 20px rgb(15 23 42 / 0.06);
}

body[data-ff-page="fundraiser"] .ff-nav__link {
  padding: 0.82rem 1rem;
  border-radius: 999px;
  font-weight: 700;
  letter-spacing: -0.01em;
  transition:
    transform 160ms ease,
    background-color 160ms ease,
    color 160ms ease,
    box-shadow 160ms ease;
}

body[data-ff-page="fundraiser"] .ff-nav__link:hover,
body[data-ff-page="fundraiser"] .ff-nav__link:focus-visible {
  transform: translateY(-1px);
  background: rgb(255 255 255 / 0.82);
  box-shadow: inset 0 0 0 1px rgb(148 163 184 / 0.16);
}

body[data-ff-page="fundraiser"] .ff-themeToggle--desktop {
  min-height: 3.25rem;
  padding-inline: 0.95rem;
  border-radius: 999px;
  font-weight: 700;
  border: 1px solid rgb(148 163 184 / 0.16);
  background:
    linear-gradient(180deg, rgb(255 255 255 / 0.94), rgb(255 255 255 / 0.82));
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.72),
    0 8px 18px rgb(15 23 42 / 0.05);
}

body[data-ff-page="fundraiser"] .ff-themeToggle__glyph {
  display: inline-grid;
  place-items: center;
  width: 1.1rem;
  margin-right: 0.1rem;
}

body[data-ff-page="fundraiser"] .ff-topbar__desktopActions > .ff-donate-btn,
body[data-ff-page="fundraiser"] .ff-topbar__mobile-only .ff-donate-btn {
  min-height: 3.25rem;
  padding-inline: 1.22rem;
  border-radius: 999px;
  font-weight: 800;
  letter-spacing: -0.01em;
  box-shadow:
    0 14px 26px rgb(249 115 22 / 0.24),
    inset 0 1px 0 rgb(255 255 255 / 0.18);
}

body[data-ff-page="fundraiser"] .ff-topbarGoal {
  border-radius: 1.7rem;
  padding: 1rem 1.05rem 0.95rem;
  border: 1px solid rgb(148 163 184 / 0.14);
  background:
    linear-gradient(180deg, rgb(255 255 255 / 0.86), rgb(248 250 252 / 0.92));
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.65),
    0 10px 26px rgb(15 23 42 / 0.04);
}

body[data-ff-page="fundraiser"] .ff-topbarGoal__summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  align-items: end;
  margin-bottom: 0.4rem;
}

body[data-ff-page="fundraiser"] .ff-topbarGoal__metric {
  min-width: 0;
}

body[data-ff-page="fundraiser"] .ff-topbarGoal__label {
  display: block;
  margin-bottom: 0.18rem;
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: rgb(100 116 139 / 0.92);
}

body[data-ff-page="fundraiser"] .ff-topbarGoal__raised,
body[data-ff-page="fundraiser"] .ff-topbarGoal__goal,
body[data-ff-page="fundraiser"] .ff-topbarGoal__percent {
  display: block;
  font-size: clamp(1.35rem, 1vw + 1rem, 1.85rem);
  line-height: 1;
  font-weight: 850;
  letter-spacing: -0.025em;
  color: rgb(15 23 42 / 0.98);
}

body[data-ff-page="fundraiser"] .ff-topbarGoal__percent {
  color: rgb(249 115 22 / 0.98);
}

body[data-ff-page="fundraiser"] .ff-topbarGoal__metaRow {
  margin-bottom: 0.45rem;
}

body[data-ff-page="fundraiser"] .ff-topbarGoal__progressLabel {
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: rgb(100 116 139 / 0.92);
}

body[data-ff-page="fundraiser"] .ff-topbarGoal__progressWrap .ff-help {
  font-size: 0.95rem;
}

body[data-ff-page="fundraiser"] .ff-meter {
  border-radius: 999px;
  padding: 0.15rem;
  background: rgb(148 163 184 / 0.14);
  box-shadow: inset 0 1px 1px rgb(15 23 42 / 0.04);
}

body[data-ff-page="fundraiser"] .ff-meter__progress {
  block-size: 0.72rem;
  border-radius: 999px;
}

body[data-ff-page="fundraiser"] .ff-topbar__mobile-only .ff-iconbtn {
  min-width: 3rem;
  min-height: 3rem;
  border-radius: 999px;
  border: 1px solid rgb(148 163 184 / 0.16);
  background:
    linear-gradient(180deg, rgb(255 255 255 / 0.94), rgb(255 255 255 / 0.82));
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.72),
    0 8px 18px rgb(15 23 42 / 0.05);
}

@media (max-width: 960px) {
  body[data-ff-page="fundraiser"] .ff-topbar__capsule--flagship {
    border-radius: 1.5rem;
    padding: 0.35rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbar__capsuleInner {
    gap: 0.75rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbarBrand--flagship {
    min-height: 3rem;
    padding: 0.28rem 0.34rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbarBrand__text {
    font-size: 1.02rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbarBrand__sub {
    font-size: 0.84rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbarGoal {
    border-radius: 1.3rem;
    padding: 0.85rem 0.85rem 0.82rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbarGoal__summary {
    gap: 0.7rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbarGoal__raised,
  body[data-ff-page="fundraiser"] .ff-topbarGoal__goal,
  body[data-ff-page="fundraiser"] .ff-topbarGoal__percent {
    font-size: 1.2rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbarGoal__progressWrap .ff-help {
    font-size: 0.86rem;
  }
}

html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-topbar__capsule--flagship,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-navPill.ff-nav--pill,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-themeToggle--desktop,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-topbarGoal,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-topbar__mobile-only .ff-iconbtn {
  border-color: rgb(148 163 184 / 0.16);
  background:
    linear-gradient(180deg, rgb(15 23 42 / 0.88), rgb(15 23 42 / 0.74));
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.04),
    0 18px 44px rgb(2 6 23 / 0.34);
}

html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-nav__link:hover,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-nav__link:focus-visible {
  background: rgb(255 255 255 / 0.05);
  box-shadow: inset 0 0 0 1px rgb(148 163 184 / 0.16);
}

html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-topbarGoal__label,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-topbarGoal__progressLabel {
  color: rgb(148 163 184 / 0.9);
}

html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-topbarGoal__raised,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-topbarGoal__goal {
  color: rgb(248 250 252 / 0.98);
}

html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-topbarGoal__progressWrap .ff-help,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-topbarBrand__sub {
  color: rgb(203 213 225 / 0.88);
}
/* FF_TOPBAR_VISUAL_REFINEMENT_V1_END */
""".strip() + "\n"

def backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = path.with_suffix(path.suffix + f".bak.{stamp}")
    bak.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return bak

orig = CSS.read_text(encoding="utf-8")

if START in orig and END in orig:
    updated = re.sub(
        re.escape(START) + r".*?" + re.escape(END),
        BLOCK.strip(),
        orig,
        flags=re.S,
    )
else:
    updated = orig.rstrip() + "\n\n" + BLOCK

if updated == orig:
    print(f"✔ no CSS changes needed: {CSS}")
    raise SystemExit(0)

bak = backup(CSS)
CSS.write_text(updated, encoding="utf-8")

print("== TOPBAR VISUAL REFINEMENT ==")
print(f"✅ patched css: {CSS}")
print(f"🛟 backup: {bak}")
print("   • premium top capsule")
print("   • stronger nav / theme / donate hierarchy")
print("   • cleaner goal rail typography")
print("   • visible desktop/mobile chrome polish")
