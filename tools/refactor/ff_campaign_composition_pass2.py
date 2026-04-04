from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path(".").resolve()
STAMP = datetime.now().strftime("%Y%m%d-%H%M%S")

CSS_PATH = ROOT / "apps/web/app/static/css/ff.css"

if not CSS_PATH.exists():
    raise SystemExit(f"❌ missing css file: {CSS_PATH}")

def backup(path: Path) -> Path:
    bak = path.with_name(path.name + f".bak-campaign-composition-pass2-{STAMP}")
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

CSS_START = "/* FF_CAMPAIGN_LAYOUT_COMPOSITION_V1_START */"
CSS_END = "/* FF_CAMPAIGN_LAYOUT_COMPOSITION_V1_END */"

CSS_BLOCK = f"""
{CSS_START}
@layer ff.pages {{
  body[data-ff-page="fundraiser"] {{
    --ff-campaign-section-gap: clamp(1rem, 2.2vw, 1.5rem);
    --ff-campaign-card-pad: clamp(1rem, 2vw, 1.4rem);
    --ff-campaign-card-pad-lg: clamp(1.1rem, 2.4vw, 1.7rem);
    --ff-campaign-max-copy: 38ch;
    --ff-campaign-hero-title: clamp(2.8rem, 6vw, 5.2rem);
  }}

  body[data-ff-page="fundraiser"] .ff-section {{
    padding-block: clamp(1.2rem, 3vw, 2.8rem);
  }}

  body[data-ff-page="fundraiser"] .ff-card,
  body[data-ff-page="fundraiser"] .ff-proofMini,
  body[data-ff-page="fundraiser"] .ff-teamCard {{
    padding: var(--ff-campaign-card-pad);
  }}

  body[data-ff-page="fundraiser"] #home .ff-card,
  body[data-ff-page="fundraiser"] .ff-checkoutShell--flagship,
  body[data-ff-page="fundraiser"] .ff-modal__panel--flagship {{
    padding: var(--ff-campaign-card-pad-lg);
  }}

  body[data-ff-page="fundraiser"] #home .ff-grid,
  body[data-ff-page="fundraiser"] #impact .ff-grid,
  body[data-ff-page="fundraiser"] #teams .ff-grid,
  body[data-ff-page="fundraiser"] #sponsors .ff-grid,
  body[data-ff-page="fundraiser"] #story .ff-grid,
  body[data-ff-page="fundraiser"] #trust-faq .ff-grid {{
    gap: var(--ff-campaign-section-gap);
    align-items: start;
  }}

  @media (min-width: 980px) {{
    body[data-ff-page="fundraiser"] #home .ff-grid {{
      grid-template-columns: minmax(0, 1.18fr) minmax(320px, 0.82fr);
      align-items: start;
    }}
  }}

  body[data-ff-page="fundraiser"] #home .ff-display {{
    max-width: 11ch;
    font-size: var(--ff-campaign-hero-title);
  }}

  body[data-ff-page="fundraiser"] #home .ff-lead {{
    max-width: var(--ff-campaign-max-copy);
  }}

  body[data-ff-page="fundraiser"] .ff-kicker + .ff-display,
  body[data-ff-page="fundraiser"] .ff-kicker + .ff-h1,
  body[data-ff-page="fundraiser"] .ff-kicker + h1 {{
    margin-top: 0.42rem;
  }}

  body[data-ff-page="fundraiser"] .ff-display + .ff-lead,
  body[data-ff-page="fundraiser"] .ff-h1 + .ff-lead,
  body[data-ff-page="fundraiser"] h1 + .ff-lead {{
    margin-top: 0.85rem;
  }}

  body[data-ff-page="fundraiser"] .ff-row.ff-wrap.ff-gap-2[role="list"],
  body[data-ff-page="fundraiser"] .ff-row.ff-wrap.ff-gap-2 {{
    row-gap: 0.5rem;
  }}

  body[data-ff-page="fundraiser"] .ff-topbar,
  body[data-ff-page="fundraiser"] .ff-header,
  body[data-ff-page="fundraiser"] .ff-nav {{
    backdrop-filter: saturate(1.06) blur(14px);
  }}

  body[data-ff-page="fundraiser"] .ff-topbar {{
    border-bottom: 1px solid rgb(15 23 42 / 0.06);
    box-shadow:
      0 14px 36px rgb(15 23 42 / 0.05),
      inset 0 -1px 0 rgb(255 255 255 / 0.55);
  }}

  body[data-ff-page="fundraiser"] .ff-themeToggle,
  body[data-ff-page="fundraiser"] .ff-btn--secondary,
  body[data-ff-page="fundraiser"] .ff-btn--ghost {{
    min-height: 2.65rem;
  }}

  body[data-ff-page="fundraiser"] #home .ff-btn--primary,
  body[data-ff-page="fundraiser"] [data-ff-floating-donate] .ff-btn--primary,
  body[data-ff-page="fundraiser"] .ff-checkoutShell .ff-btn--primary {{
    min-width: 10.25rem;
  }}

  body[data-ff-page="fundraiser"] #home .ff-card > .ff-row:last-child,
  body[data-ff-page="fundraiser"] #impact .ff-card > .ff-row:last-child,
  body[data-ff-page="fundraiser"] #story .ff-card > .ff-row:last-child {{
    margin-top: 0.95rem;
  }}

  body[data-ff-page="fundraiser"] #impact .ff-card,
  body[data-ff-page="fundraiser"] #sponsors .ff-card,
  body[data-ff-page="fundraiser"] #story .ff-card,
  body[data-ff-page="fundraiser"] #trust-faq .ff-card {{
    min-height: 0;
  }}

  body[data-ff-page="fundraiser"] #impact .ff-grid > *,
  body[data-ff-page="fundraiser"] #sponsors .ff-grid > *,
  body[data-ff-page="fundraiser"] #story .ff-grid > *,
  body[data-ff-page="fundraiser"] #trust-faq .ff-grid > * {{
    min-width: 0;
  }}

  body[data-ff-page="fundraiser"] #teams .ff-teamCard {{
    display: grid;
    grid-template-rows: auto auto 1fr auto;
    gap: 0.8rem;
    align-content: start;
  }}

  body[data-ff-page="fundraiser"] #teams .ff-teamCard .ff-btn {{
    width: 100%;
    justify-content: center;
  }}

  body[data-ff-page="fundraiser"] #teams .ff-teamCard .ff-help,
  body[data-ff-page="fundraiser"] #teams .ff-teamCard p {{
    max-width: 32ch;
  }}

  body[data-ff-page="fundraiser"] #teams .ff-teamCard .ff-row.ff-wrap.ff-gap-2 {{
    align-items: center;
  }}

  body[data-ff-page="fundraiser"] #teams .ff-teamCard .ff-pill,
  body[data-ff-page="fundraiser"] #sponsors .ff-pill {{
    font-size: 0.72rem;
  }}

  body[data-ff-page="fundraiser"] #story .ff-card,
  body[data-ff-page="fundraiser"] #trust-faq .ff-card {{
    align-self: start;
  }}

  body[data-ff-page="fundraiser"] #story .ff-card h2,
  body[data-ff-page="fundraiser"] #trust-faq .ff-card h2 {{
    max-width: 16ch;
  }}

  body[data-ff-page="fundraiser"] .ff-checkoutHead,
  body[data-ff-page="fundraiser"] .ff-sponsorModal__head,
  body[data-ff-page="fundraiser"] .ff-videoModal__head {{
    padding-bottom: 0.9rem;
    margin-bottom: 0.9rem;
  }}

  body[data-ff-page="fundraiser"] .ff-sheet__viewport,
  body[data-ff-page="fundraiser"] .ff-modal__panel {{
    scrollbar-gutter: stable both-edges;
  }}

  body[data-ff-page="fundraiser"] [data-ff-floating-donate] {{
    border-radius: 999px;
    box-shadow:
      0 16px 36px rgb(15 23 42 / 0.10),
      inset 0 1px 0 rgb(255 255 255 / 0.52);
    backdrop-filter: saturate(1.06) blur(16px);
  }}

  body[data-ff-page="fundraiser"] [data-ff-backtotop] {{
    box-shadow:
      0 16px 32px rgb(15 23 42 / 0.12),
      inset 0 1px 0 rgb(255 255 255 / 0.48);
  }}

  body[data-ff-page="fundraiser"] #sponsors .ff-card,
  body[data-ff-page="fundraiser"] #story .ff-card,
  body[data-ff-page="fundraiser"] #trust-faq .ff-card {{
    background-image:
      linear-gradient(180deg, rgb(255 255 255 / 0.42), rgb(255 255 255 / 0.00));
    background-blend-mode: screen;
  }}

  html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] .ff-topbar,
  body[data-ff-page="fundraiser"][data-ff-theme="dark"] .ff-topbar {{
    border-bottom-color: rgb(148 163 184 / 0.12);
    box-shadow:
      0 18px 42px rgb(2 6 23 / 0.26),
      inset 0 -1px 0 rgb(255 255 255 / 0.04);
  }}

  html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] #sponsors .ff-card,
  html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] #story .ff-card,
  html.ff-root[data-theme="dark"] body[data-ff-page="fundraiser"] #trust-faq .ff-card,
  body[data-ff-page="fundraiser"][data-ff-theme="dark"] #sponsors .ff-card,
  body[data-ff-page="fundraiser"][data-ff-theme="dark"] #story .ff-card,
  body[data-ff-page="fundraiser"][data-ff-theme="dark"] #trust-faq .ff-card {{
    background-image:
      linear-gradient(180deg, rgb(255 255 255 / 0.05), rgb(255 255 255 / 0.00));
  }}

  @media (max-width: 767px) {{
    body[data-ff-page="fundraiser"] {{
      --ff-campaign-section-gap: 0.95rem;
      --ff-campaign-card-pad: 0.92rem;
      --ff-campaign-card-pad-lg: 1rem;
    }}

    body[data-ff-page="fundraiser"] .ff-section {{
      padding-block: 1rem 1.15rem;
    }}

    body[data-ff-page="fundraiser"] #home .ff-display {{
      max-width: 9.5ch;
      font-size: clamp(2.35rem, 10vw, 3.3rem);
    }}

    body[data-ff-page="fundraiser"] #home .ff-lead {{
      max-width: 30ch;
    }}

    body[data-ff-page="fundraiser"] #teams .ff-teamCard,
    body[data-ff-page="fundraiser"] #impact .ff-card,
    body[data-ff-page="fundraiser"] #story .ff-card {{
      min-height: 0;
    }}

    body[data-ff-page="fundraiser"] [data-ff-floating-donate] {{
      left: max(0.75rem, env(safe-area-inset-left));
      right: max(0.75rem, env(safe-area-inset-right));
      bottom: max(0.75rem, env(safe-area-inset-bottom));
    }}
  }}
}}
{CSS_END}
"""

AUDIT_PATH = ROOT / "tools/audit/ff_css_gate_lite.py"
AUDIT_SCRIPT = r'''from __future__ import annotations
from pathlib import Path
import sys

ROOT = Path(".").resolve()
CSS = ROOT / "apps/web/app/static/css/ff.css"

if not CSS.exists():
    print(f"❌ missing css: {CSS}")
    raise SystemExit(1)

text = CSS.read_text(encoding="utf-8")

checks = []

checks.append(("CSS file exists and is non-empty", len(text.strip()) > 0))
checks.append(("No merge conflict markers", all(mark not in text for mark in ("<<<<<<<", "=======", ">>>>>>>"))))
checks.append(("Campaign system polish marker present", "FF_CAMPAIGN_SYSTEM_POLISH_V1_START" in text))
checks.append(("Campaign layout composition marker present", "FF_CAMPAIGN_LAYOUT_COMPOSITION_V1_START" in text))
checks.append(("Brace balance looks sane", text.count("{") == text.count("}")))
checks.append(("No inline style strings accidentally copied into CSS", 'style="' not in text))

failed = [name for name, ok in checks if not ok]

print("== FF CSS GATE LITE ==")
for name, ok in checks:
    print(f"{'✅' if ok else '❌'} {name}")

if failed:
    print("\nFAILED:")
    for name in failed:
        print(f" - {name}")
    raise SystemExit(1)

print("\nPASS")
'''

def main():
    backup_path = backup(CSS_PATH)
    css = read(CSS_PATH)
    css = upsert_marker_block(css, CSS_START, CSS_END, CSS_BLOCK)
    write(CSS_PATH, css)

    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    write(AUDIT_PATH, AUDIT_SCRIPT)

    print("✅ ff_campaign_composition_pass2 applied")
    print(f"🛟 backup[css]: {backup_path}")
    print(f"✅ audit: {AUDIT_PATH}")

    text = read(CSS_PATH)
    print("\n== MARKER PROOF ==")
    print("layout composition marker:", CSS_START in text and CSS_END in text)
    print("campaign polish marker   :", "FF_CAMPAIGN_SYSTEM_POLISH_V1_START" in text)

if __name__ == "__main__":
    main()
