from __future__ import annotations

from pathlib import Path

ROOT = Path.home() / "futurefunded-enterprise"
TPL = ROOT / "apps/web/app/templates"
MARKETING = TPL / "platform/shells/marketing_base.html"
OPERATOR = TPL / "platform/shells/operator_base.html"
LEGACY = TPL / "platform/shells/platform_base_legacy.html"
TOPBAR = TPL / "shared/partials/_platform_topbar.html"
STATUS = TPL / "shared/partials/_platform_status_bar.html"

HEADER_START = '    <header class="ff-chrome" aria-label="Platform chrome" data-ff-chrome="">'
TOPBAR_START = '        <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">'
STATUS_START = '        <section\n          class="ff-glass ff-surface ff-pad ff-mt-3"'
HEADER_CLOSE = '    </header>'

REPLACEMENT = """    <header class="ff-chrome" aria-label="Platform chrome" data-ff-chrome="">
      <div class="ff-container ff-platformChrome__inner">
        {% include "shared/partials/_platform_topbar.html" %}
        {% include "shared/partials/_platform_status_bar.html" %}
      </div>
    </header>"""

def extract_from_shell(shell_path: Path) -> tuple[str, str]:
    text = shell_path.read_text(encoding="utf-8")

    header_idx = text.find(HEADER_START)
    if header_idx == -1:
        raise SystemExit(f"Could not find header block in {shell_path}")

    topbar_idx = text.find(TOPBAR_START, header_idx)
    if topbar_idx == -1:
        raise SystemExit(f"Could not find topbar block in {shell_path}")

    status_idx = text.find(STATUS_START, topbar_idx)
    if status_idx == -1:
        raise SystemExit(f"Could not find status strip block in {shell_path}")

    header_close_idx = text.find(HEADER_CLOSE, status_idx)
    if header_close_idx == -1:
        raise SystemExit(f"Could not find header close in {shell_path}")

    topbar_markup = text[topbar_idx:status_idx].rstrip() + "\n"
    status_markup = text[status_idx:header_close_idx].rstrip() + "\n"

    return topbar_markup, status_markup


def replace_header(shell_path: Path) -> None:
    text = shell_path.read_text(encoding="utf-8")

    header_idx = text.find(HEADER_START)
    if header_idx == -1:
        raise SystemExit(f"Could not find header start in {shell_path}")

    header_close_idx = text.find(HEADER_CLOSE, header_idx)
    if header_close_idx == -1:
        raise SystemExit(f"Could not find header close in {shell_path}")

    old_block = text[header_idx:header_close_idx + len(HEADER_CLOSE)]
    if '{% include "shared/partials/_platform_topbar.html" %}' in old_block:
        return

    text = text.replace(old_block, REPLACEMENT, 1)
    shell_path.write_text(text, encoding="utf-8")


def main() -> None:
    for p in [MARKETING, OPERATOR, LEGACY]:
        if not p.exists():
            raise SystemExit(f"Missing shell: {p}")

    topbar_markup, status_markup = extract_from_shell(MARKETING)

    TOPBAR.parent.mkdir(parents=True, exist_ok=True)
    STATUS.parent.mkdir(parents=True, exist_ok=True)

    TOPBAR.write_text(topbar_markup, encoding="utf-8")
    STATUS.write_text(status_markup, encoding="utf-8")

    replace_header(MARKETING)
    replace_header(OPERATOR)
    replace_header(LEGACY)

    print("✅ platform chrome extracted")
    print(f"topbar partial : {TOPBAR}")
    print(f"status partial : {STATUS}")
    print(f"updated shells :")
    print(f" - {MARKETING}")
    print(f" - {OPERATOR}")
    print(f" - {LEGACY}")


if __name__ == "__main__":
    main()
