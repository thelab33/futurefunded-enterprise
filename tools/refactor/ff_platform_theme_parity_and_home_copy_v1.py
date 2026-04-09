from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/platform-pages.css"
HOME = ROOT / "apps/web/app/templates/platform/pages/home.html"

MARKER = "FF_PLATFORM_THEME_PARITY_AUTHORITY_V1"

CSS_BLOCK = r'''
/* ==========================================================================
   FF_PLATFORM_THEME_PARITY_AUTHORITY_V1
   Platform theme parity + homepage convergence authority
   - makes platform surfaces consume ff.css theme tokens
   - supports both light and dark via html.ff-root[data-theme]
   - overrides OS-only light drift with token-driven surfaces
   - normalizes legacy/current platform selector ownership
   ========================================================================== */

@layer ff.pages {
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) {
    --ff-platform-shell-max: 1240px;
    --ff-platform-section-space: clamp(1.25rem, 0.92rem + 1.1vw, 2.6rem);
    --ff-platform-card-radius: 28px;
    --ff-platform-card-radius-sm: 20px;
    --ff-platform-border: var(--ff-border);
    --ff-platform-border-strong: var(--ff-border-strong);
    --ff-platform-copy-strong: var(--ff-text);
    --ff-platform-copy: var(--ff-text-soft);
    --ff-platform-copy-muted: var(--ff-text-muted);
    --ff-platform-copy-faint: var(--ff-text-faint);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-container {
    width: min(100% - 2rem, var(--ff-platform-shell-max));
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-main {
    padding-bottom: clamp(3rem, 2rem + 2vw, 5rem);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-section {
    --ff-space-section: var(--ff-platform-section-space);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-shellBg {
    background:
      radial-gradient(circle at 8% 0%, var(--ff-info-soft), transparent 34%),
      radial-gradient(circle at 100% 0%, var(--ff-brand-soft), transparent 28%),
      radial-gradient(circle at 50% 100%, var(--ff-info-soft), transparent 36%),
      linear-gradient(180deg, rgb(255 255 255 / 0.03), rgb(255 255 255 / 0));
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-display,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-h2,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-h3 {
    color: var(--ff-platform-copy-strong);
    text-shadow: none;
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-lead {
    color: var(--ff-platform-copy);
    line-height: 1.64;
    max-width: 52ch;
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-help,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-help.ff-muted,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-muted {
    color: var(--ff-platform-copy-muted);
    line-height: 1.62;
    text-wrap: pretty;
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-kicker,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-label,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformBrand__subline {
    color: var(--ff-platform-copy-faint);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) [data-ff-platform-trust],
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-card.ff-glass,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-proofMini {
    border-color: var(--ff-platform-border-strong);
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.05), rgb(255 255 255 / 0)),
      var(--ff-panel-strong);
    box-shadow: var(--ff-shadow-2);
    backdrop-filter: blur(var(--ff-blur));
    -webkit-backdrop-filter: blur(var(--ff-blur));
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-proofMini,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformInlinePill,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformStatPill,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-navPill,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-nav.ff-nav--pill {
    border-color: var(--ff-platform-border);
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.03), rgb(255 255 255 / 0)),
      var(--ff-panel);
    box-shadow: var(--ff-shadow-1);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformInlinePill,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformStatPill {
    color: var(--ff-platform-copy-strong);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-nav.ff-nav--pill .ff-nav__link {
    color: var(--ff-platform-copy);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-nav.ff-nav--pill .ff-nav__link[aria-current="page"] {
    color: var(--ff-platform-copy-strong);
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.08), rgb(255 255 255 / 0)),
      linear-gradient(180deg, rgb(249 115 22 / 0.16), rgb(14 165 233 / 0.08));
    box-shadow:
      inset 0 0 0 1px rgb(255 255 255 / 0.06),
      var(--ff-shadow-1);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-btn.ff-btn--secondary,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-btn.ff-btn--pill.ff-btn--secondary {
    color: var(--ff-platform-copy-strong);
    border-color: var(--ff-platform-border-strong);
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.05), rgb(255 255 255 / 0)),
      var(--ff-panel);
    box-shadow: var(--ff-shadow-1);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-input,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformFieldGrid .ff-input {
    border-color: var(--ff-platform-border-strong);
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.05), rgb(255 255 255 / 0)),
      var(--ff-panel-solid);
    color: var(--ff-platform-copy-strong);
    box-shadow: inset 0 1px 1px rgb(15 23 42 / 0.03);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"])[data-ff-page="home"] .ff-sectionhead[aria-labelledby="platformHomeHeroTitle"] .ff-display,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"])[data-ff-page="home"] #platformHomeHeroTitle {
    max-width: 11ch;
    text-wrap: balance;
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"])[data-ff-page="home"] .ff-platformGridTop .ff-card.ff-glass:first-child,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"])[data-ff-page="home"] [aria-labelledby="platformWhyItWinsTitle"],
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"])[data-ff-page="home"] [aria-labelledby="platformLaunchCardsTitle"] .ff-grid > *:nth-child(-n+2) {
    border-color: rgb(14 165 233 / 0.16);
    background:
      radial-gradient(circle at top right, rgb(14 165 233 / 0.08), transparent 36%),
      linear-gradient(180deg, rgb(255 255 255 / 0.05), rgb(255 255 255 / 0)),
      var(--ff-panel-strong);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow {
    margin-top: clamp(2.25rem, 4vw, 4rem);
    padding: clamp(1rem, 1.6vw, 1.5rem);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__inner {
    position: relative;
    isolation: isolate;
    overflow: hidden;
    display: grid;
    gap: clamp(1rem, 1.8vw, 1.5rem);
    padding: clamp(1.15rem, 2.5vw, 1.85rem);
    border-radius: 30px;
    border: 1px solid var(--ff-platform-border-strong);
    background:
      radial-gradient(900px 320px at 0% -6%, var(--ff-info-soft), transparent 58%),
      radial-gradient(640px 260px at 100% 0%, var(--ff-brand-soft), transparent 50%),
      linear-gradient(180deg, rgb(255 255 255 / 0.05), rgb(255 255 255 / 0)),
      var(--ff-panel-strong);
    box-shadow: var(--ff-shadow-3);
    backdrop-filter: blur(var(--ff-blur));
    -webkit-backdrop-filter: blur(var(--ff-blur));
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__inner::before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.035), transparent 18%, transparent 82%, rgb(255 255 255 / 0.02));
    opacity: 0.95;
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__intro,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__steps,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__close,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__closeCopy,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__actions {
    position: relative;
    z-index: 1;
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__eyebrow,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__closeEyebrow,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__stepNumber {
    margin: 0;
    color: var(--ff-platform-copy-faint);
    font-size: 0.74rem;
    font-weight: 900;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    opacity: 1;
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__title,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__closeTitle,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__step h3 {
    color: var(--ff-platform-copy-strong);
    text-shadow: none;
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__title {
    margin: 0;
    max-width: 18ch;
    font-size: clamp(1.55rem, 2.5vw, 2.25rem);
    line-height: 1.04;
    font-weight: 950;
    letter-spacing: -0.03em;
    text-wrap: balance;
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__body,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__closeBody,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__step p {
    color: var(--ff-platform-copy);
    opacity: 1;
    text-wrap: pretty;
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__steps {
    display: grid;
    gap: 1rem;
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__step,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__close {
    border-color: var(--ff-platform-border);
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.04), rgb(255 255 255 / 0)),
      var(--ff-panel);
    box-shadow: var(--ff-shadow-1);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__step {
    display: grid;
    align-content: start;
    gap: 0.55rem;
    min-height: 100%;
    padding: 1.05rem;
    border-radius: 22px;
    transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
  }

  @media (hover: hover) and (pointer: fine) {
    :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__step:hover {
      transform: translateY(-2px);
      border-color: rgb(249 115 22 / 0.22);
      box-shadow:
        0 0 0 1px rgb(249 115 22 / 0.06),
        var(--ff-shadow-2);
    }
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__close {
    display: grid;
    gap: 1rem;
    grid-template-columns: minmax(0, 1.18fr) minmax(260px, 0.82fr);
    align-items: center;
    padding: 1.1rem;
    border-radius: 24px;
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__actions {
    display: grid;
    gap: 0.75rem;
    width: min(100%, 22rem);
    justify-self: end;
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 50px;
    width: 100%;
    border-radius: 15px;
    text-decoration: none;
    font-weight: 900;
    letter-spacing: 0.01em;
    white-space: nowrap;
    transition: transform 140ms ease, border-color 140ms ease, box-shadow 140ms ease, filter 140ms ease;
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__button--primary {
    color: var(--ff-inverse);
    border: 1px solid transparent;
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.12), rgb(255 255 255 / 0)),
      linear-gradient(180deg, var(--ff-brand), var(--ff-brand-strong));
    box-shadow:
      inset 0 1px 0 rgb(255 255 255 / 0.14),
      0 12px 26px rgb(249 115 22 / 0.24);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__button--secondary {
    color: var(--ff-platform-copy-strong);
    border: 1px solid var(--ff-platform-border-strong);
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.05), rgb(255 255 255 / 0)),
      var(--ff-panel);
    box-shadow: var(--ff-shadow-1);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__button:hover {
    transform: translateY(-1px);
  }

  @media (max-width: 1100px) {
    :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__steps {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__close {
      grid-template-columns: 1fr;
    }

    :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__actions {
      width: 100%;
      justify-self: stretch;
    }
  }

  @media (max-width: 720px) {
    :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__inner {
      border-radius: 24px;
      padding: 1.1rem;
    }

    :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__title {
      max-width: 12ch;
      font-size: clamp(1.4rem, 7vw, 1.9rem);
    }

    :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__steps {
      grid-template-columns: 1fr;
    }

    :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__step,
    :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__close {
      border-radius: 18px;
    }

    :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__button {
      min-height: 48px;
    }

    :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-founderFlow__button--primary {
      order: -1;
    }
  }
}
'''.strip()

HOME_REPLACEMENTS: list[tuple[str, str]] = [
    (
        r'FutureFunded\s+launch-ready\s+platform',
        'Launch-ready fundraising platform',
    ),
    (
        r'Give\s+Connect\s+ATX\s+Elite\s+a\s+premium\s+fundraising\s+home\s+with\s+FutureFunded\.',
        'Launch premium fundraising pages, sponsor lanes, and recurring support from one platform.',
    ),
    (
        r'FutureFunded\s+turns\s+a\s+youth\s+program\s+into\s+a\s+sponsor-ready,\s*donor-ready\s+fundraising\s+presence\s+with\s+stronger\s+branding,\s*clearer\s+readability,\s*and\s+operator\s+control\s+that\s+feels\s+built\s+—\s*not\s+pieced\s+together\.',
        'FutureFunded gives programs a branded fundraising system with clear donor paths, structured sponsor support, recurring giving, and cleaner operator control.',
    ),
    (
        r'A\s+premium\s+FutureFunded\s+launch,\s*not\s+a\s+generic\s+fundraiser\s+page\.',
        'A platform launch, not a one-page fundraiser.',
    ),
    (
        r'What\s+programs\s+get\s+on\s+day\s+one\.',
        'What launches on day one.',
    ),
    (
        r'FutureFunded\s+starts\s+with\s+a\s+premium\s+core\s+offer\s+that\s+is\s+easy\s+to\s+explain,\s*easy\s+to\s+trust,\s*and\s+strong\s+enough\s+to\s+grow\s+into\s+a\s+larger\s+platform\s+sale\s+later\.',
        'FutureFunded starts with a clear launch offer that is easy to explain, easy to trust, and strong enough to expand into sponsor packages and recurring support later.',
    ),
    (
        r'Use\s+the\s+live\s+Connect\s+ATX\s+Elite\s+fundraiser\s+to\s+show\s+what\s+FutureFunded\s+looks\s+like\s+in\s+production:\s*premium\s+branding,\s*clearer\s+trust,\s*sponsor\s+readiness,\s*and\s+a\s+stronger\s+operator\s+story\.',
        'Use the live platform view to show how FutureFunded presents public fundraising, sponsor visibility, and operator readiness in one cleaner system.',
    ),
    (
        r'Start\s+with\s+Connect\s+ATX\s+Elite\.\s*Expand\s+with\s+confidence\.',
        'Start with one launch. Expand without rework.',
    ),
    (
        r'Built\s+to\s+feel\s+like\s+a\s+premium\s+platform,\s*not\s+a\s+fundraiser\s+template\.',
        'Built to feel like a real platform, not a fundraiser template.',
    ),
    (
        r'Launch\s+the\s+real\s+program\s+with\s+FutureFunded\.',
        'Launch with a cleaner fundraising system.',
    ),
    (
        r'Use\s+onboarding\s+to\s+brand\s+Connect\s+ATX\s+Elite\s+inside\s+FutureFunded,\s*go\s+live\s+with\s+a\s+premium\s+public\s+fundraiser,\s*then\s+expand\s+into\s+sponsor\s+packages\s+and\s+recurring\s+support\s+without\s+rebuilding\s+the\s+experience\.',
        'Use onboarding to configure branding, launch a premium public fundraiser, and expand into sponsor packages and recurring support without rebuilding the experience.',
    ),
]


def backup(path: Path) -> Path:
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    dest = path.with_name(f"{path.name}.{ts}.bak")
    shutil.copy2(path, dest)
    return dest


def append_css_authority() -> tuple[bool, Path | None]:
    text = CSS.read_text(encoding='utf-8')
    if MARKER in text:
        return False, None
    new_text = text.rstrip() + '\n\n' + CSS_BLOCK + '\n'
    bak = backup(CSS)
    CSS.write_text(new_text, encoding='utf-8')
    return True, bak


def patch_home_copy() -> tuple[int, Path | None]:
    if not HOME.exists():
        return 0, None

    text = HOME.read_text(encoding='utf-8')
    original = text
    total = 0

    for pattern, replacement in HOME_REPLACEMENTS:
        text, n = re.subn(pattern, replacement, text, flags=re.I | re.S)
        total += n

    if text == original:
        return 0, None

    bak = backup(HOME)
    HOME.write_text(text, encoding='utf-8')
    return total, bak


if __name__ == '__main__':
    if not CSS.exists():
        raise SystemExit(f'missing: {CSS}')

    css_changed, css_bak = append_css_authority()
    home_changes, home_bak = patch_home_copy()

    print(f'css_changed: {css_changed}')
    if css_bak:
        print(f'css_backup:  {css_bak}')
    print(f'home_changes: {home_changes}')
    if home_bak:
        print(f'home_backup: {home_bak}')
    print(f'css_path:     {CSS}')
    print(f'home_path:    {HOME}')
