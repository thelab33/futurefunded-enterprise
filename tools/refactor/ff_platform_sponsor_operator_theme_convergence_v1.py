from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/platform-pages.css"

MARKER = "FF_PLATFORM_SPONSOR_OPERATOR_THEME_PARITY_V1"

CSS_BLOCK = r'''
/* ==========================================================================
   FF_PLATFORM_SPONSOR_OPERATOR_THEME_PARITY_V1
   Sponsor + operator token-driven theme authority
   - converges sponsor/operator premium surfaces onto ff.css tokens
   - removes dependence on prefers-color-scheme light overrides
   - preserves existing selectors and template contracts
   ========================================================================== */

@layer ff.pages {
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorMerch__inner,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorConvert,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__inner,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorCard--diagnostics {
    border-color: var(--ff-border-strong);
    background:
      radial-gradient(circle at top right, var(--ff-info-soft), transparent 34%),
      radial-gradient(circle at top left, var(--ff-brand-soft), transparent 30%),
      linear-gradient(180deg, rgb(255 255 255 / 0.05), rgb(255 255 255 / 0)),
      var(--ff-panel-strong);
    box-shadow: var(--ff-shadow-2);
    backdrop-filter: blur(var(--ff-blur));
    -webkit-backdrop-filter: blur(var(--ff-blur));
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorMerch__card,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorMerch__meta > div,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorProof,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorProof__card,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorConvert__chip,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__card,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__rail,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorStat {
    border-color: var(--ff-border);
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.04), rgb(255 255 255 / 0)),
      var(--ff-panel);
    box-shadow: var(--ff-shadow-1);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorProof,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorConvert,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__rail {
    border-color: var(--ff-border-strong);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorMerch__chip,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorConvert__chip {
    color: var(--ff-text);
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.03), rgb(255 255 255 / 0)),
      var(--ff-panel);
    border-color: var(--ff-border);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorMerch__button,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorConvert__button,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__button {
    min-height: 50px;
    border-radius: 15px;
    font-weight: 900;
    letter-spacing: 0.01em;
    transition:
      transform 140ms ease,
      border-color 140ms ease,
      box-shadow 140ms ease,
      filter 140ms ease;
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorMerch__button--primary,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorConvert__button--primary,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__button--primary {
    color: var(--ff-inverse);
    border: 1px solid transparent;
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.12), rgb(255 255 255 / 0)),
      linear-gradient(180deg, var(--ff-brand), var(--ff-brand-strong));
    box-shadow:
      inset 0 1px 0 rgb(255 255 255 / 0.14),
      0 12px 26px rgb(249 115 22 / 0.24);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorMerch__button--secondary,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorConvert__button--secondary,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__button--secondary {
    color: var(--ff-text);
    border: 1px solid var(--ff-border-strong);
    background:
      linear-gradient(180deg, rgb(255 255 255 / 0.05), rgb(255 255 255 / 0)),
      var(--ff-panel);
    box-shadow: var(--ff-shadow-1);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorMerch__button:hover,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorConvert__button:hover,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__button:hover {
    transform: translateY(-1px);
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorProof__eyebrow,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorConvert__eyebrow,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__eyebrow,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__railEyebrow,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__kicker,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorMerch__meta dt {
    color: var(--ff-text-faint);
    opacity: 1;
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorProof__title,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorProof__card h4,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorConvert__title,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__title,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__railTitle,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__card h3 {
    color: var(--ff-text);
    text-shadow: none;
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorMerch__meta dd,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorProof__card p,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorConvert__body,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorConvert__footer p,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__body,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__card p,
  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__list {
    color: var(--ff-text-soft);
    opacity: 1;
  }

  :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorConvert__footer {
    border-top-color: var(--ff-line);
  }

  @media (hover: hover) and (pointer: fine) {
    :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorMerch__card.is-featured:hover,
    :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorProof__card:hover,
    :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__card:hover {
      transform: translateY(-2px);
      border-color: rgb(249 115 22 / 0.22);
      box-shadow:
        0 0 0 1px rgb(249 115 22 / 0.06),
        var(--ff-shadow-2);
    }
  }

  @media (max-width: 720px) {
    :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorMerch__button,
    :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-platformSponsorConvert__button,
    :where(body[data-ff-template="platform"], body[data-ff-platform="true"]) .ff-operatorPremium__button {
      min-height: 48px;
    }
  }
}
'''.strip()


def backup(path: Path) -> Path:
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    dest = path.with_name(f"{path.name}.{ts}.bak")
    shutil.copy2(path, dest)
    return dest


def append_authority(text: str) -> tuple[str, bool]:
    if MARKER in text:
        return text, False
    return text.rstrip() + '\n\n' + CSS_BLOCK + '\n', True


def find_matching_brace(text: str, open_brace_idx: int) -> int:
    depth = 0
    for i in range(open_brace_idx, len(text)):
        ch = text[i]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return i
    raise ValueError('matching brace not found')


def remove_light_media_block_by_anchor(text: str, anchor: str) -> tuple[str, bool]:
    anchor_idx = text.find(anchor)
    if anchor_idx == -1:
        return text, False

    start = text.rfind('@media (prefers-color-scheme: light)', 0, anchor_idx)
    if start == -1:
        return text, False

    brace_idx = text.find('{', start)
    if brace_idx == -1:
        return text, False

    end = find_matching_brace(text, brace_idx)
    new_text = text[:start].rstrip() + '\n\n' + text[end + 1:].lstrip()
    return new_text, True


def normalize_spacing(text: str) -> str:
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.rstrip() + '\n'


def main() -> None:
    if not CSS.exists():
        raise SystemExit(f'missing: {CSS}')

    text = CSS.read_text(encoding='utf-8')
    original = text

    text, appended = append_authority(text)

    anchors = [
        'ff-platformSponsorMerch__inner',
        'ff-platformSponsorMerch__meta > div',
        'ff-platformSponsorConvert {',
        'ff-operatorPremium__inner {',
        'ff-founderFlow__inner,\n  body[data-ff-platform="true"] .ff-operatorPremium__inner {',
    ]

    removed = 0
    for anchor in anchors:
        text, changed = remove_light_media_block_by_anchor(text, anchor)
        removed += int(changed)

    text = normalize_spacing(text)

    if text == original:
        print('no-op: no changes applied')
        return

    bak = backup(CSS)
    CSS.write_text(text, encoding='utf-8')

    print(f'authority_appended: {appended}')
    print(f'light_blocks_removed: {removed}')
    print(f'css_backup:          {bak}')
    print(f'css_path:            {CSS}')


if __name__ == '__main__':
    main()
