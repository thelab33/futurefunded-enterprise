from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/ff.css"

START = "/* FF_FINAL_PRESTIGE_PASS_V1_START */"
END = "/* FF_FINAL_PRESTIGE_PASS_V1_END */"

BLOCK = r"""
/* FF_FINAL_PRESTIGE_PASS_V1_START */
/* Final launch polish for desktop + mobile, light + dark. */

body[data-ff-page="fundraiser"] .ff-hero__capsule,
body[data-ff-page="fundraiser"] .ff-heroPanel .ff-card,
body[data-ff-page="fundraiser"] .ff-impactCard,
body[data-ff-page="fundraiser"] .ff-storyCard,
body[data-ff-page="fundraiser"] .ff-teamsShell,
body[data-ff-page="fundraiser"] .ff-sponsorsBoard,
body[data-ff-page="fundraiser"] .ff-faqEndcap,
body[data-ff-page="fundraiser"] .ff-footerShell {
  box-shadow:
    0 14px 36px rgb(15 23 42 / 0.05),
    0 2px 8px rgb(15 23 42 / 0.03);
}

body[data-ff-page="fundraiser"] .ff-topbar__capsule--flagship {
  box-shadow:
    0 16px 40px rgb(15 23 42 / 0.07),
    inset 0 1px 0 rgb(255 255 255 / 0.74);
}

body[data-ff-page="fundraiser"] .ff-hero__capsule,
body[data-ff-page="fundraiser"] .ff-heroPanel .ff-card {
  border-color: rgb(148 163 184 / 0.15);
}

body[data-ff-page="fundraiser"] .ff-teamCard,
body[data-ff-page="fundraiser"] .ff-sponsorCell,
body[data-ff-page="fundraiser"] .ff-impactTier,
body[data-ff-page="fundraiser"] .ff-checkoutCard,
body[data-ff-page="fundraiser"] .ff-disclosure {
  box-shadow:
    0 10px 24px rgb(15 23 42 / 0.045),
    0 1px 2px rgb(15 23 42 / 0.03);
}

body[data-ff-page="fundraiser"] .ff-sectionhead {
  margin-bottom: 0.72rem;
}

body[data-ff-page="fundraiser"] .ff-proofMini,
body[data-ff-page="fundraiser"] .ff-progressMini,
body[data-ff-page="fundraiser"] .ff-callout {
  border-color: rgb(148 163 184 / 0.14);
}

body[data-ff-page="fundraiser"] .ff-sponsorEmptyState,
body[data-ff-page="fundraiser"] .ff-empty,
body[data-ff-page="fundraiser"] .ff-teamsEmpty {
  box-shadow: inset 0 1px 0 rgb(255 255 255 / 0.28);
}

body[data-ff-page="fundraiser"] .ff-donate-btn,
body[data-ff-page="fundraiser"] .ff-btn--primary,
body[data-ff-page="fundraiser"] .ff-tab--cta {
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.16),
    0 10px 24px rgb(249 115 22 / 0.24);
}

body[data-ff-page="fundraiser"] .ff-donate-btn:hover,
body[data-ff-page="fundraiser"] .ff-btn--primary:hover,
body[data-ff-page="fundraiser"] .ff-tab--cta:hover {
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.18),
    0 14px 30px rgb(249 115 22 / 0.28);
}

html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-hero__capsule,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-heroPanel .ff-card,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-impactCard,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-storyCard,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-teamsShell,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-sponsorsBoard,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-faqEndcap,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-footerShell {
  border-color: rgb(148 163 184 / 0.14);
  background:
    linear-gradient(180deg, rgb(255 255 255 / 0.03), rgb(255 255 255 / 0)),
    linear-gradient(180deg, rgb(10 18 34 / 0.94), rgb(6 14 28 / 0.98));
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.04),
    0 20px 44px rgb(0 0 0 / 0.34);
}

html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-teamCard,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-sponsorCell,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-impactTier,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-checkoutCard,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-disclosure,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-proofMini,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-progressMini,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-callout {
  border-color: rgb(148 163 184 / 0.14);
  background:
    linear-gradient(180deg, rgb(255 255 255 / 0.025), rgb(255 255 255 / 0)),
    linear-gradient(180deg, rgb(9 17 31 / 0.92), rgb(7 14 28 / 0.98));
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.035),
    0 14px 28px rgb(0 0 0 / 0.28);
}

html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-topbar__capsule--flagship {
  border-color: rgb(148 163 184 / 0.16);
  background:
    linear-gradient(180deg, rgb(255 255 255 / 0.04), rgb(255 255 255 / 0)),
    linear-gradient(180deg, rgb(10 18 34 / 0.94), rgb(7 14 28 / 0.98));
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.05),
    0 18px 42px rgb(0 0 0 / 0.34);
}

html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-topbarGoal {
  border-color: rgb(148 163 184 / 0.16);
  background:
    linear-gradient(180deg, rgb(255 255 255 / 0.04), rgb(255 255 255 / 0)),
    linear-gradient(180deg, rgb(12 21 38 / 0.96), rgb(8 16 31 / 0.98));
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.05),
    0 16px 36px rgb(0 0 0 / 0.28);
}

html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-sponsorEmptyState,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-empty,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-teamsEmpty {
  border-color: rgb(148 163 184 / 0.18);
  background:
    linear-gradient(180deg, rgb(255 255 255 / 0.025), rgb(255 255 255 / 0)),
    linear-gradient(180deg, rgb(10 18 34 / 0.84), rgb(8 15 28 / 0.94));
}

html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-teamCard__media,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-storyPoster,
html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-videoFrame {
  border-color: rgb(148 163 184 / 0.14);
  box-shadow: inset 0 1px 0 rgb(255 255 255 / 0.045);
}

html[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-tabs {
  border-top: 1px solid rgb(148 163 184 / 0.12);
}

@media (max-width: 47.99rem) {
  body[data-ff-page="fundraiser"] {
    --ff-space-section: clamp(1.18rem, 1rem + 0.9vw, 1.85rem);
  }

  body[data-ff-page="fundraiser"] .ff-topbar__capsule,
  body[data-ff-page="fundraiser"] .ff-topbarGoal,
  body[data-ff-page="fundraiser"] .ff-hero__capsule,
  body[data-ff-page="fundraiser"] .ff-heroPanel .ff-card,
  body[data-ff-page="fundraiser"] .ff-impactTier,
  body[data-ff-page="fundraiser"] .ff-teamCard,
  body[data-ff-page="fundraiser"] .ff-sponsorCell,
  body[data-ff-page="fundraiser"] .ff-checkoutCard,
  body[data-ff-page="fundraiser"] .ff-footerShell,
  body[data-ff-page="fundraiser"] .ff-faqEndcap {
    border-radius: 1rem;
  }

  body[data-ff-page="fundraiser"] .ff-sectionhead {
    margin-bottom: 0.62rem;
  }

  body[data-ff-page="fundraiser"] .ff-teamCard,
  body[data-ff-page="fundraiser"] .ff-sponsorCell,
  body[data-ff-page="fundraiser"] .ff-impactTier {
    padding: 0.88rem;
  }

  body[data-ff-page="fundraiser"] .ff-teamCard__stats {
    padding: 0.54rem;
  }

  body[data-ff-page="fundraiser"] .ff-teamCard__foot {
    gap: 0.55rem;
  }

  body[data-ff-page="fundraiser"] .ff-donate-btn,
  body[data-ff-page="fundraiser"] .ff-btn--primary,
  body[data-ff-page="fundraiser"] .ff-tab--cta {
    min-height: 2.7rem;
  }
}
/* FF_FINAL_PRESTIGE_PASS_V1_END */
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
        print("== FF CSS FINAL PRESTIGE PASS V1 ==")
        print("✔ no changes needed")
        raise SystemExit(0)

    bak = backup(CSS)
    CSS.write_text(updated, encoding="utf-8")

    print("== FF CSS FINAL PRESTIGE PASS V1 ==")
    print(f"✅ patched css : {CSS}")
    print(f"🛟 backup      : {bak}")
    print("done:")
    print(" - improved dark mode surface separation")
    print(" - tuned hero / donate / sponsor / faq / footer elevation")
    print(" - softened mobile density slightly")
    print(f"marker start   : {START}")
    print(f"marker end     : {END}")

if __name__ == "__main__":
    main()
