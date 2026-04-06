from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/ff.css"

START = "/* FF_FINAL_PRESTIGE_MICRO_POLISH_V1_START */"
END = "/* FF_FINAL_PRESTIGE_MICRO_POLISH_V1_END */"

BLOCK = r"""
/* FF_FINAL_PRESTIGE_MICRO_POLISH_V1_START */
/* Final founder-level polish:
   - tighter mobile chrome
   - calmer hero density
   - stronger sponsor hierarchy
   - smoother FAQ/footer finish
   - cleanup for duplicated donationForm selector
*/

body[data-ff-page="fundraiser"] .ff-topbar {
  padding-top: 0.38rem;
}

body[data-ff-page="fundraiser"] .ff-topbar__capsule {
  padding: 0.74rem;
  border-radius: 1.2rem;
}

body[data-ff-page="fundraiser"] .ff-topbar__capsuleInner {
  gap: 0.68rem;
}

body[data-ff-page="fundraiser"] .ff-topbarGoal {
  padding: 0.72rem 0.84rem;
  border-radius: 1rem;
}

body[data-ff-page="fundraiser"] .ff-topbarGoal__summary {
  gap: 0.5rem;
}

body[data-ff-page="fundraiser"] .ff-topbarGoal__raised,
body[data-ff-page="fundraiser"] .ff-topbarGoal__goal,
body[data-ff-page="fundraiser"] .ff-topbarGoal__percent {
  font-size: 0.94rem;
}

body[data-ff-page="fundraiser"] .ff-topbarGoal__progressWrap {
  gap: 0.3rem;
}

body[data-ff-page="fundraiser"] .ff-hero__capsule {
  padding: clamp(0.96rem, 0.9rem + 0.34vw, 1.2rem);
}

body[data-ff-page="fundraiser"] .ff-heroHeader {
  gap: 0.82rem;
}

body[data-ff-page="fundraiser"] .ff-heroFooter {
  gap: 0.45rem;
}

body[data-ff-page="fundraiser"] .ff-heroSnapshotGrid {
  gap: 0.68rem;
}

body[data-ff-page="fundraiser"] .ff-proofMini--hero,
body[data-ff-page="fundraiser"] .ff-proofMini--teams,
body[data-ff-page="fundraiser"] .ff-proofMini--tile {
  padding: 0.82rem 0.88rem;
}

body[data-ff-page="fundraiser"] .ff-proofMini--hero .ff-h3,
body[data-ff-page="fundraiser"] .ff-proofMini--teams .ff-h3,
body[data-ff-page="fundraiser"] .ff-proofMini--tile .ff-h3 {
  line-height: 1.08;
}

body[data-ff-page="fundraiser"] .ff-section {
  padding-block: clamp(1.45rem, 1.18rem + 1.4vw, 2.7rem);
}

body[data-ff-page="fundraiser"] .ff-sectionhead {
  gap: 0.58rem;
  margin-bottom: 0.72rem;
}

body[data-ff-page="fundraiser"] .ff-impactTier,
body[data-ff-page="fundraiser"] .ff-sponsorTierCard,
body[data-ff-page="fundraiser"] .ff-teamCard,
body[data-ff-page="fundraiser"] .ff-checkoutCard,
body[data-ff-page="fundraiser"] .ff-sponsorCell {
  transition:
    transform var(--ff-ease),
    border-color var(--ff-ease),
    box-shadow var(--ff-ease),
    background-color var(--ff-ease);
}

body[data-ff-page="fundraiser"] .ff-impactTier--recommended,
body[data-ff-page="fundraiser"] .ff-card--premium,
body[data-ff-page="fundraiser"] .ff-impactTier--premium,
body[data-ff-page="fundraiser"] .ff-sponsorTierCard:has(.ff-pill--accent) {
  border-color: rgb(249 115 22 / 0.26);
  box-shadow:
    0 0 0 1px rgb(249 115 22 / 0.08),
    0 18px 36px rgb(249 115 22 / 0.12),
    0 8px 20px rgb(15 23 42 / 0.05);
}

body[data-ff-page="fundraiser"] .ff-impactTier--recommended .ff-btn,
body[data-ff-page="fundraiser"] .ff-sponsorTierCard:has(.ff-pill--accent) .ff-btn {
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 0.14),
    0 10px 22px rgb(249 115 22 / 0.18);
}

body[data-ff-page="fundraiser"] .ff-teamCard__foot {
  gap: 0.62rem;
}

body[data-ff-page="fundraiser"] .ff-teamCard__stats {
  gap: 0.52rem;
}

body[data-ff-page="fundraiser"] .ff-teamStat {
  padding: 0.46rem 0.52rem;
}

body[data-ff-page="fundraiser"] .ff-faqEndcap {
  border-color: rgb(148 163 184 / 0.16);
  box-shadow:
    0 14px 32px rgb(15 23 42 / 0.07),
    0 4px 12px rgb(15 23 42 / 0.03);
}

body[data-ff-page="fundraiser"] .ff-faqEndcap__header {
  gap: 0.62rem;
}

body[data-ff-page="fundraiser"] .ff-faqList {
  gap: 0.62rem;
}

body[data-ff-page="fundraiser"] .ff-disclosure__sum {
  padding: 0.88rem 0.95rem;
}

body[data-ff-page="fundraiser"] .ff-disclosure__panel {
  padding: 0 0.95rem 0.95rem;
}

body[data-ff-page="fundraiser"] .ff-footerShell {
  padding: clamp(0.96rem, 0.92rem + 0.24vw, 1.15rem);
}

body[data-ff-page="fundraiser"] .ff-footerGrid {
  gap: 0.9rem;
}

body[data-ff-page="fundraiser"] .ff-footerBrand__copy {
  max-width: 58ch;
}

body[data-ff-page="fundraiser"] .ff-footerMeta {
  padding-top: 0.78rem;
  gap: 0.35rem;
}

body[data-ff-page="fundraiser"] .ff-backtotop {
  min-height: 2.4rem;
  padding: 0.56rem 0.78rem;
}

html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-impactTier--recommended,
html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-card--premium,
html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-impactTier--premium,
html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-sponsorTierCard:has(.ff-pill--accent) {
  border-color: rgb(249 115 22 / 0.22);
  box-shadow:
    0 0 0 1px rgb(249 115 22 / 0.06),
    0 18px 44px rgb(0 0 0 / 0.32),
    inset 0 1px 0 rgb(255 255 255 / 0.04);
}

html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-faqEndcap {
  border-color: rgb(226 232 240 / 0.08);
  box-shadow:
    0 16px 36px rgb(0 0 0 / 0.26),
    inset 0 1px 0 rgb(255 255 255 / 0.03);
}

@media (max-width: 47.99rem) {
  body[data-ff-page="fundraiser"] .ff-topbar__capsule {
    padding: 0.66rem;
    border-radius: 1.05rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbarGoal {
    padding: 0.64rem 0.76rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbarGoal__summary {
    gap: 0.44rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbarGoal__raised,
  body[data-ff-page="fundraiser"] .ff-topbarGoal__goal,
  body[data-ff-page="fundraiser"] .ff-topbarGoal__percent {
    font-size: 0.9rem;
  }

  body[data-ff-page="fundraiser"] .ff-hero__capsule {
    padding: 0.92rem;
  }

  body[data-ff-page="fundraiser"] .ff-heroHeader {
    gap: 0.72rem;
  }

  body[data-ff-page="fundraiser"] .ff-heroSnapshotGrid {
    gap: 0.56rem;
  }

  body[data-ff-page="fundraiser"] .ff-proofMini--hero {
    padding: 0.76rem 0.8rem;
  }

  body[data-ff-page="fundraiser"] .ff-section {
    padding-block: 1.25rem;
  }

  body[data-ff-page="fundraiser"] .ff-teamCard,
  body[data-ff-page="fundraiser"] .ff-impactTier,
  body[data-ff-page="fundraiser"] .ff-sponsorCell,
  body[data-ff-page="fundraiser"] .ff-checkoutCard {
    padding: 0.88rem;
  }

  body[data-ff-page="fundraiser"] .ff-teamCard__foot > .ff-btn,
  body[data-ff-page="fundraiser"] .ff-teamCard__foot > .ff-footer__link--button,
  body[data-ff-page="fundraiser"] .ff-teamCard__foot > .ff-link {
    flex: 1 1 auto;
  }

  body[data-ff-page="fundraiser"] .ff-footerShell {
    padding: 0.92rem;
  }

  body[data-ff-page="fundraiser"] .ff-footerMeta {
    padding-top: 0.7rem;
  }

  body[data-ff-page="fundraiser"] .ff-backtotop {
    right: 0.72rem;
    bottom: calc(var(--ff-tabs-offset) + 0.78rem + var(--ff-safe-bottom));
  }
}

@media (min-width: 64rem) {
  body[data-ff-page="fundraiser"] .ff-topbar__capsule {
    padding: 0.78rem;
  }

  body[data-ff-page="fundraiser"] .ff-hero__grid {
    gap: 0.92rem;
  }

  body[data-ff-page="fundraiser"] .ff-impactLayout,
  body[data-ff-page="fundraiser"] .ff-storyGrid,
  body[data-ff-page="fundraiser"] .ff-checkoutLayout--form {
    gap: 0.92rem;
  }

  body[data-ff-page="fundraiser"] .ff-footerGrid {
    gap: 1rem;
  }
}
/* FF_FINAL_PRESTIGE_MICRO_POLISH_V1_END */
""".strip() + "\n"

text = CSS.read_text(encoding="utf-8")

# clean one messy duplicated selector fragment
text = text.replace(
    "  #donationForm,\n  \n  #donationForm,\n  #sponsorForm {",
    "  #donationForm,\n  #sponsorForm {"
)

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
print("✅ applied FF_FINAL_PRESTIGE_MICRO_POLISH_V1")
