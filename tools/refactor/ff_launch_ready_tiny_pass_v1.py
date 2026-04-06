from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/ff.css"

START = "/* FF_LAUNCH_READY_TINY_PASS_V1_START */"
END = "/* FF_LAUNCH_READY_TINY_PASS_V1_END */"

BLOCK = r"""
/* FF_LAUNCH_READY_TINY_PASS_V1_START */
/* Final tiny launch pass:
   - mobile chrome compression
   - hero card calmness
   - sponsor consistency
   - faq/footer quiet luxury
*/

body[data-ff-page="fundraiser"] .ff-pill {
  min-height: 1.68rem;
  padding: 0.24rem 0.62rem;
}

body[data-ff-page="fundraiser"] .ff-btn--sm {
  min-height: 2.22rem;
  padding: 0.5rem 0.8rem;
}

body[data-ff-page="fundraiser"] .ff-topbarBrand__text,
body[data-ff-page="fundraiser"] .ff-brand__title {
  letter-spacing: -0.015em;
}

body[data-ff-page="fundraiser"] .ff-topbarBrand__sub {
  opacity: 0.92;
}

body[data-ff-page="fundraiser"] .ff-proofMini--hero {
  border-color: rgb(148 163 184 / 0.14);
}

body[data-ff-page="fundraiser"] .ff-proofMini--hero .ff-help {
  max-width: 24ch;
}

body[data-ff-page="fundraiser"] .ff-impactTier,
body[data-ff-page="fundraiser"] .ff-sponsorTierCard {
  min-height: 100%;
}

body[data-ff-page="fundraiser"] .ff-impactTier__head,
body[data-ff-page="fundraiser"] .ff-impactTier__body,
body[data-ff-page="fundraiser"] .ff-impactTier__footer,
body[data-ff-page="fundraiser"] .ff-sponsorTierCard__head,
body[data-ff-page="fundraiser"] .ff-sponsorTierCard__body,
body[data-ff-page="fundraiser"] .ff-sponsorTierCard__foot {
  gap: 0.52rem;
}

body[data-ff-page="fundraiser"] .ff-impactTier__footer,
body[data-ff-page="fundraiser"] .ff-sponsorTierCard__foot {
  margin-top: auto;
}

body[data-ff-page="fundraiser"] .ff-faqEndcap {
  border-radius: 1.1rem;
}

body[data-ff-page="fundraiser"] .ff-footerMeta,
body[data-ff-page="fundraiser"] .ff-footerBrand__meta {
  row-gap: 0.22rem;
}

body[data-ff-page="fundraiser"] .ff-footer__link,
body[data-ff-page="fundraiser"] .ff-footer__link--button {
  text-underline-offset: 0.12em;
}

html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-proofMini--hero {
  border-color: rgb(226 232 240 / 0.08);
}

@media (max-width: 47.99rem) {
  body[data-ff-page="fundraiser"] .ff-topbar {
    padding-top: 0.26rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbar__capsule {
    padding: 0.58rem;
    border-radius: 0.96rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbar__capsuleInner,
  body[data-ff-page="fundraiser"] .ff-topbar__mainRow {
    gap: 0.56rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbarBrand {
    gap: 0.52rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbarBrand__logo {
    width: 30px;
    height: 30px;
  }

  body[data-ff-page="fundraiser"] .ff-topbarBrand__text,
  body[data-ff-page="fundraiser"] .ff-brand__title {
    font-size: 0.92rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbarBrand__sub {
    font-size: 0.76rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbarGoal {
    padding: 0.58rem 0.7rem;
    border-radius: 0.92rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbarGoal__summary {
    gap: 0.38rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbarGoal__label,
  body[data-ff-page="fundraiser"] .ff-topbarGoal__progressLabel {
    font-size: 0.66rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbarGoal__raised,
  body[data-ff-page="fundraiser"] .ff-topbarGoal__goal,
  body[data-ff-page="fundraiser"] .ff-topbarGoal__percent {
    font-size: 0.86rem;
  }

  body[data-ff-page="fundraiser"] .ff-heroHeader {
    gap: 0.66rem;
  }

  body[data-ff-page="fundraiser"] .ff-display {
    max-width: 10.5ch;
    line-height: 0.94;
  }

  body[data-ff-page="fundraiser"] .ff-heroSnapshotGrid {
    gap: 0.5rem;
  }

  body[data-ff-page="fundraiser"] .ff-proofMini--hero {
    padding: 0.7rem 0.76rem;
  }

  body[data-ff-page="fundraiser"] .ff-proofMini--hero .ff-h3 {
    font-size: 0.96rem;
  }

  body[data-ff-page="fundraiser"] .ff-sectionhead {
    margin-bottom: 0.62rem;
  }

  body[data-ff-page="fundraiser"] .ff-impactTier,
  body[data-ff-page="fundraiser"] .ff-teamCard,
  body[data-ff-page="fundraiser"] .ff-sponsorCell,
  body[data-ff-page="fundraiser"] .ff-checkoutCard {
    padding: 0.8rem;
    border-radius: 1rem;
  }

  body[data-ff-page="fundraiser"] .ff-teamCard__stats {
    gap: 0.42rem;
    padding: 0.58rem;
  }

  body[data-ff-page="fundraiser"] .ff-teamStat {
    padding: 0.42rem 0.48rem;
    border-radius: 0.78rem;
  }

  body[data-ff-page="fundraiser"] .ff-impactTier__head,
  body[data-ff-page="fundraiser"] .ff-impactTier__body,
  body[data-ff-page="fundraiser"] .ff-impactTier__footer,
  body[data-ff-page="fundraiser"] .ff-sponsorTierCard__head,
  body[data-ff-page="fundraiser"] .ff-sponsorTierCard__body,
  body[data-ff-page="fundraiser"] .ff-sponsorTierCard__foot {
    gap: 0.48rem;
  }

  body[data-ff-page="fundraiser"] .ff-faqEndcap {
    border-radius: 1rem;
  }

  body[data-ff-page="fundraiser"] .ff-disclosure__sum {
    padding: 0.82rem 0.88rem;
  }

  body[data-ff-page="fundraiser"] .ff-disclosure__panel {
    padding: 0 0.88rem 0.88rem;
  }

  body[data-ff-page="fundraiser"] .ff-footerShell {
    border-radius: 1rem;
  }

  body[data-ff-page="fundraiser"] .ff-footerMeta {
    padding-top: 0.64rem;
  }
}

@media (max-width: 26rem) {
  body[data-ff-page="fundraiser"] .ff-topbarBrand__text,
  body[data-ff-page="fundraiser"] .ff-brand__title {
    font-size: 0.88rem;
  }

  body[data-ff-page="fundraiser"] .ff-pill {
    min-height: 1.58rem;
    padding: 0.2rem 0.52rem;
    font-size: 0.64rem;
  }

  body[data-ff-page="fundraiser"] .ff-btn--sm {
    min-height: 2.08rem;
    padding: 0.46rem 0.72rem;
    font-size: 0.86rem;
  }

  body[data-ff-page="fundraiser"] .ff-topbarGoal__raised,
  body[data-ff-page="fundraiser"] .ff-topbarGoal__goal,
  body[data-ff-page="fundraiser"] .ff-topbarGoal__percent {
    font-size: 0.82rem;
  }

  body[data-ff-page="fundraiser"] .ff-proofMini--hero .ff-help {
    max-width: none;
  }
}
/* FF_LAUNCH_READY_TINY_PASS_V1_END */
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
print("✅ applied FF_LAUNCH_READY_TINY_PASS_V1")
