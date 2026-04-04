from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path(".").resolve()
CSS_PATH = ROOT / "apps/web/app/static/css/ff.css"
STAMP = datetime.now().strftime("%Y%m%d-%H%M%S")

if not CSS_PATH.exists():
    raise SystemExit(f"❌ missing css file: {CSS_PATH}")

def backup(path: Path) -> Path:
    bak = path.with_name(path.name + f".bak-campaign-lower-half-polish-{STAMP}")
    shutil.copy2(path, bak)
    return bak

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")

def upsert_marker_block(text: str, start: str, end: str, block: str) -> str:
    pattern = re.escape(start) + r".*?" + re.escape(end)
    wrapped = block.strip() + "\n"
    if start in text and end in text:
        return re.sub(pattern, wrapped, text, flags=re.S)
    return text.rstrip() + "\n\n" + wrapped

START = "/* FF_CAMPAIGN_LOWER_HALF_POLISH_V1_START */"
END = "/* FF_CAMPAIGN_LOWER_HALF_POLISH_V1_END */"

BLOCK = f"""
{START}
@layer ff.pages {{
  body[data-ff-page="fundraiser"] {{
    --ff-campaign-lower-gap: clamp(0.95rem, 1.9vw, 1.3rem);
    --ff-campaign-lower-pad: clamp(0.95rem, 1.8vw, 1.25rem);
    --ff-campaign-lower-pad-lg: clamp(1.05rem, 2vw, 1.45rem);
  }}

  body[data-ff-page="fundraiser"] #sponsors,
  body[data-ff-page="fundraiser"] #story,
  body[data-ff-page="fundraiser"] #trust-faq,
  body[data-ff-page="fundraiser"] footer {{
    position: relative;
  }}

  body[data-ff-page="fundraiser"] #sponsors .ff-grid,
  body[data-ff-page="fundraiser"] #story .ff-grid,
  body[data-ff-page="fundraiser"] #trust-faq .ff-grid,
  body[data-ff-page="fundraiser"] footer .ff-grid {{
    gap: var(--ff-campaign-lower-gap);
    align-items: start;
  }}

  body[data-ff-page="fundraiser"] #sponsors .ff-card,
  body[data-ff-page="fundraiser"] #sponsors .ff-proofMini,
  body[data-ff-page="fundraiser"] #story .ff-card,
  body[data-ff-page="fundraiser"] #story .ff-proofMini,
  body[data-ff-page="fundraiser"] #trust-faq .ff-card,
  body[data-ff-page="fundraiser"] footer .ff-card {{
    padding: var(--ff-campaign-lower-pad);
  }}

  body[data-ff-page="fundraiser"] #sponsors .ff-card h2,
  body[data-ff-page="fundraiser"] #story .ff-card h2,
  body[data-ff-page="fundraiser"] #trust-faq .ff-card h2 {{
    max-width: 15ch;
  }}

  body[data-ff-page="fundraiser"] #sponsors .ff-card,
  body[data-ff-page="fundraiser"] #sponsors .ff-proofMini {{
    display: grid;
    grid-template-rows: auto auto 1fr auto;
    align-content: start;
    gap: 0.72rem;
  }}

  body[data-ff-page="fundraiser"] #sponsors .ff-btn,
  body[data-ff-page="fundraiser"] #story .ff-btn {{
    min-height: 2.55rem;
  }}

  body[data-ff-page="fundraiser"] #sponsors .ff-btn--primary {{
    min-width: 8.75rem;
  }}

  body[data-ff-page="fundraiser"] #sponsors .ff-row.ff-wrap.ff-gap-2,
  body[data-ff-page="fundraiser"] #story .ff-row.ff-wrap.ff-gap-2,
  body[data-ff-page="fundraiser"] #trust-faq .ff-row.ff-wrap.ff-gap-2 {{
    row-gap: 0.45rem;
  }}

  body[data-ff-page="fundraiser"] #story .ff-card,
  body[data-ff-page="fundraiser"] #trust-faq .ff-card {{
    min-height: 0;
  }}

  body[data-ff-page="fundraiser"] #story .ff-card > :last-child,
  body[data-ff-page="fundraiser"] #trust-faq .ff-card > :last-child,
  body[data-ff-page="fundraiser"] footer .ff-card > :last-child {{
    margin-bottom: 0;
  }}

  body[data-ff-page="fundraiser"] #story .ff-card p,
  body[data-ff-page="fundraiser"] #trust-faq .ff-card p,
  body[data-ff-page="fundraiser"] footer .ff-card p {{
    max-width: 54ch;
  }}

  body[data-ff-page="fundraiser"] #trust-faq details,
  body[data-ff-page="fundraiser"] #trust-faq .ff-accordion__item,
  body[data-ff-page="fundraiser"] #trust-faq .ff-card {{
    border-radius: 18px;
  }}

  body[data-ff-page="fundraiser"] #trust-faq details,
  body[data-ff-page="fundraiser"] #trust-faq .ff-accordion__item {{
    border: 1px solid rgb(15 23 42 / 0.08);
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.92), rgb(247 249 253 / 0.88));
    box-shadow:
      0 14px 30px rgb(15 23 42 / 0.05),
      inset 0 1px 0 rgb(255 255 255 / 0.55);
  }}

  body[data-ff-page="fundraiser"] #trust-faq summary,
  body[data-ff-page="fundraiser"] #trust-faq [data-ff-question],
  body[data-ff-page="fundraiser"] #trust-faq .ff-row[aria-expanded] {{
    padding: 0.95rem 1rem;
    cursor: pointer;
  }}

  body[data-ff-page="fundraiser"] #trust-faq details > *:not(summary) {{
    padding-inline: 1rem;
    padding-bottom: 0.95rem;
  }}

  body[data-ff-page="fundraiser"] footer {{
    padding-top: clamp(0.5rem, 1.4vw, 1rem);
  }}

  body[data-ff-page="fundraiser"] footer .ff-card,
  body[data-ff-page="fundraiser"] .ff-footer,
  body[data-ff-page="fundraiser"] .ff-footerShell {{
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.94), rgb(245 247 251 / 0.92));
    border: 1px solid rgb(15 23 42 / 0.08);
    box-shadow:
      0 16px 34px rgb(15 23 42 / 0.05),
      inset 0 1px 0 rgb(255 255 255 / 0.56);
    border-radius: clamp(18px, 2vw, 24px);
  }}

  body[data-ff-page="fundraiser"] footer .ff-btn--primary {{
    min-width: 9rem;
  }}

  body[data-ff-page="fundraiser"] footer .ff-btn--secondary,
  body[data-ff-page="fundraiser"] footer .ff-btn--ghost {{
    min-width: 7.5rem;
  }}

  body[data-ff-page="fundraiser"] footer .ff-row.ff-row--between,
  body[data-ff-page="fundraiser"] .ff-footer .ff-row.ff-row--between {{
    align-items: center;
    gap: 0.85rem;
  }}

  body[data-ff-page="fundraiser"] footer .ff-kicker,
  body[data-ff-page="fundraiser"] #story .ff-kicker,
  body[data-ff-page="fundraiser"] #trust-faq .ff-kicker {{
    opacity: 0.9;
  }}

  body[data-ff-page="fundraiser"] #sponsors .ff-card::after,
  body[data-ff-page="fundraiser"] #story .ff-card::after,
  body[data-ff-page="fundraiser"] #trust-faq .ff-card::after,
  body[data-ff-page="fundraiser"] footer .ff-card::after {{
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    border-radius: inherit;
    box-shadow: inset 0 1px 0 rgb(255 255 255 / 0.38);
  }}

  body[data-ff-page="fundraiser"] #sponsors .ff-card,
  body[data-ff-page="fundraiser"] #story .ff-card,
  body[data-ff-page="fundraiser"] #trust-faq .ff-card,
  body[data-ff-page="fundraiser"] footer .ff-card {{
    position: relative;
    overflow: clip;
  }}

  body[data-ff-page="fundraiser"] #sponsors .ff-card:hover,
  body[data-ff-page="fundraiser"] #story .ff-card:hover,
  body[data-ff-page="fundraiser"] #trust-faq .ff-card:hover {{
    transform: translateY(-1px);
    transition: transform 160ms ease, box-shadow 160ms ease;
  }}

  html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] #trust-faq details,
  html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] #trust-faq .ff-accordion__item,
  body[data-ff-page="fundraiser"][data-ff-theme="dark"] #trust-faq details,
  body[data-ff-page="fundraiser"][data-ff-theme="dark"] #trust-faq .ff-accordion__item {{
    border-color: rgb(148 163 184 / 0.14);
    background:
      linear-gradient(180deg, rgb(8 15 30 / 0.88), rgb(7 18 42 / 0.84));
    box-shadow:
      0 18px 36px rgb(2 6 23 / 0.22),
      inset 0 1px 0 rgb(255 255 255 / 0.04);
  }}

  html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] footer .ff-card,
  html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-footer,
  html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-footerShell,
  body[data-ff-page="fundraiser"][data-ff-theme="dark"] footer .ff-card,
  body[data-ff-page="fundraiser"][data-ff-theme="dark"] .ff-footer,
  body[data-ff-page="fundraiser"][data-ff-theme="dark"] .ff-footerShell {{
    background:
      linear-gradient(180deg, rgb(7 17 36 / 0.90), rgb(5 14 30 / 0.88));
    border-color: rgb(148 163 184 / 0.14);
    box-shadow:
      0 20px 40px rgb(2 6 23 / 0.24),
      inset 0 1px 0 rgb(255 255 255 / 0.04);
  }}

  @media (max-width: 767px) {{
    body[data-ff-page="fundraiser"] {{
      --ff-campaign-lower-gap: 0.9rem;
      --ff-campaign-lower-pad: 0.88rem;
      --ff-campaign-lower-pad-lg: 0.96rem;
    }}

    body[data-ff-page="fundraiser"] #sponsors .ff-card,
    body[data-ff-page="fundraiser"] #story .ff-card,
    body[data-ff-page="fundraiser"] #trust-faq .ff-card,
    body[data-ff-page="fundraiser"] footer .ff-card {{
      border-radius: 18px;
    }}

    body[data-ff-page="fundraiser"] #trust-faq summary,
    body[data-ff-page="fundraiser"] #trust-faq [data-ff-question] {{
      padding: 0.88rem 0.9rem;
    }}

    body[data-ff-page="fundraiser"] #trust-faq details > *:not(summary) {{
      padding-inline: 0.9rem;
      padding-bottom: 0.88rem;
    }}

    body[data-ff-page="fundraiser"] footer .ff-row.ff-row--between,
    body[data-ff-page="fundraiser"] .ff-footer .ff-row.ff-row--between {{
      align-items: stretch;
    }}

    body[data-ff-page="fundraiser"] footer .ff-btn,
    body[data-ff-page="fundraiser"] .ff-footer .ff-btn {{
      width: 100%;
      justify-content: center;
    }}
  }}
}}
{END}
"""

def main():
    bak = backup(CSS_PATH)
    css = read(CSS_PATH)
    css = upsert_marker_block(css, START, END, BLOCK)
    write(CSS_PATH, css)

    print("✅ ff_campaign_lower_half_polish_v1 applied")
    print(f"🛟 backup[css]: {bak}")

    text = read(CSS_PATH)
    print("\\n== MARKER PROOF ==")
    print("lower-half marker:", START in text and END in text)

if __name__ == "__main__":
    main()
