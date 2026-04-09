from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
HTML = ROOT / "apps/web/app/templates/platform/pages/demo.html"
CSS = ROOT / "apps/web/app/static/css/platform-pages.css"

def backup(path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    dst = path.with_name(f"{path.name}.{ts}.bak")
    shutil.copy2(path, dst)
    return dst

def inject_after_paragraph(text: str, needle: str, injection: str, label: str) -> str:
    pattern = re.compile(
        rf'(<p[^>]*>\s*{re.escape(needle)}\s*</p>)',
        flags=re.S,
    )
    new_text, count = pattern.subn(rf'\1\n{injection}', text, count=1)
    if count != 1:
        raise RuntimeError(f"Could not patch paragraph for: {label}")
    return new_text

html = HTML.read_text(encoding="utf-8")

if "ff-demoHero__platformNote" not in html:
    hero_copy = (
        "Launch a sponsor-ready public fundraiser for youth basketball, "
        "starting with Connect ATX Elite — then expand into sponsor packages, "
        "recurring support, and cleaner operator control."
    )
    hero_injection = """        <p class="ff-demoHero__platformNote">
          Powered by FutureFunded — launch your own branded fundraiser in as little as one day.
        </p>
        <p class="ff-demoHero__ctaHint">
          Sponsor-ready • Mobile-first • Guided setup
        </p>"""
    html = inject_after_paragraph(
        html,
        hero_copy,
        hero_injection,
        "hero platform note",
    )

if "ff-demoNextMove__proof" not in html:
    next_move_copy = (
        "Use onboarding to launch the real Connect ATX Elite organization, "
        "go live fast, then expand into sponsor packages and recurring support "
        "as the program grows."
    )
    next_move_injection = """          <div class="ff-demoNextMove__proof" aria-label="Launch proof points">
            <span class="ff-demoNextMove__proofItem">Live fundraiser</span>
            <span class="ff-demoNextMove__proofItem">Sponsor lanes</span>
            <span class="ff-demoNextMove__proofItem">Recurring support</span>
            <span class="ff-demoNextMove__proofItem">Operator-ready</span>
          </div>
          <p class="ff-demoNextMove__hint">
            This is the handoff moment: show the product, explain the revenue lanes,
            then move buyers straight into launch.
          </p>"""
    html = inject_after_paragraph(
        html,
        next_move_copy,
        next_move_injection,
        "next move proof row",
    )

html_backup = backup(HTML)
HTML.write_text(html, encoding="utf-8")
print(f"changed: {HTML}")
print(f"backup:  {html_backup}")

CSS_BLOCK = r"""
/* ==========================================================================
   FF_PLATFORM_DEMO_FINAL_POLISH_V1
   Demo page final founder polish:
   - platform attribution note under hero
   - CTA reassurance line
   - next-move proof chips + handoff hint
   ========================================================================== */

body[data-ff-platform="true"] .ff-demoHero__platformNote {
  margin: 0.8rem 0 0;
  max-width: 60ch;
  color: color-mix(in srgb, var(--ff-text, #e5eefc) 78%, transparent);
  font-size: 0.96rem;
  line-height: 1.55;
}

body[data-ff-platform="true"] .ff-demoHero__ctaHint {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem 0.7rem;
  align-items: center;
  margin: 0.85rem 0 0;
  color: color-mix(in srgb, var(--ff-text, #e5eefc) 72%, transparent);
  font-size: 0.86rem;
  line-height: 1.35;
  letter-spacing: 0.01em;
}

body[data-ff-platform="true"] .ff-demoNextMove__proof {
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem;
  margin-top: 1rem;
}

body[data-ff-platform="true"] .ff-demoNextMove__proofItem {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2rem;
  padding: 0.48rem 0.72rem;
  border-radius: 999px;
  border: 1px solid color-mix(in srgb, var(--ff-line, rgba(255,255,255,0.14)) 100%, transparent);
  background:
    linear-gradient(
      180deg,
      color-mix(in srgb, var(--ff-surface-2, rgba(255,255,255,0.08)) 92%, transparent),
      color-mix(in srgb, var(--ff-surface-3, rgba(255,255,255,0.04)) 96%, transparent)
    );
  color: color-mix(in srgb, var(--ff-text, #e5eefc) 88%, transparent);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.06);
}

body[data-ff-platform="true"] .ff-demoNextMove__hint {
  margin: 0.9rem 0 0;
  max-width: 64ch;
  color: color-mix(in srgb, var(--ff-text, #e5eefc) 75%, transparent);
  font-size: 0.95rem;
  line-height: 1.58;
}

@media (max-width: 768px) {
  body[data-ff-platform="true"] .ff-demoHero__platformNote {
    font-size: 0.93rem;
  }

  body[data-ff-platform="true"] .ff-demoHero__ctaHint {
    font-size: 0.82rem;
  }

  body[data-ff-platform="true"] .ff-demoNextMove__proof {
    gap: 0.45rem;
  }

  body[data-ff-platform="true"] .ff-demoNextMove__proofItem {
    font-size: 0.74rem;
    padding: 0.44rem 0.64rem;
  }

  body[data-ff-platform="true"] .ff-demoNextMove__hint {
    font-size: 0.9rem;
  }
}
""".strip()

css = CSS.read_text(encoding="utf-8")
if "FF_PLATFORM_DEMO_FINAL_POLISH_V1" not in css:
    css_backup = backup(CSS)
    if css and not css.endswith("\n"):
        css += "\n"
    css += "\n\n" + CSS_BLOCK + "\n"
    CSS.write_text(css, encoding="utf-8")
    print(f"changed: {CSS}")
    print(f"backup:  {css_backup}")
else:
    print("skip: CSS block already present")
