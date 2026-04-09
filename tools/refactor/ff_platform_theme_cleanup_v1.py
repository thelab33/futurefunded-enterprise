from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/platform-pages.css"
HOME = ROOT / "apps/web/app/templates/platform/pages/home.html"


def backup(path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = path.with_name(f"{path.name}.{ts}.bak")
    shutil.copy2(path, dest)
    return dest


def normalize_spacing(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.rstrip() + "\n"


def remove_block_by_markers(text: str, start_marker: str, next_marker: str) -> tuple[str, bool]:
    marker_idx = text.find(start_marker)
    if marker_idx == -1:
        return text, False

    block_start = text.rfind("/*", 0, marker_idx)
    if block_start == -1:
        block_start = marker_idx

    next_idx = text.find(next_marker, marker_idx + len(start_marker))
    if next_idx == -1:
        block_end = len(text)
    else:
        next_comment_start = text.rfind("/*", 0, next_idx)
        block_end = next_comment_start if next_comment_start != -1 else next_idx

    new_text = text[:block_start].rstrip() + "\n\n" + text[block_end:].lstrip()
    return new_text, True


def patch_css() -> tuple[int, Path | None]:
    text = CSS.read_text(encoding="utf-8")
    original = text
    removed = 0

    text, changed = remove_block_by_markers(
        text,
        "FF_PLATFORM_FOUNDER_DEMO_FLOW_V1",
        "FF_PLATFORM_DASHBOARD_OPERATOR_PREMIUM_V1",
    )
    removed += int(changed)

    text, changed = remove_block_by_markers(
        text,
        "FF_PLATFORM_FOUNDER_FLOW_PREMIUM_V2",
        "FF_PLATFORM_THEME_PARITY_AUTHORITY_V1",
    )
    removed += int(changed)

    text = normalize_spacing(text)

    if text == original:
        return 0, None

    bak = backup(CSS)
    CSS.write_text(text, encoding="utf-8")
    return removed, bak


def patch_home() -> tuple[int, Path | None]:
    if not HOME.exists():
        return 0, None

    text = HOME.read_text(encoding="utf-8")
    original = text

    text, n = re.subn(
        r'\{%\s*set\s+status_pills\s*=\s*data\.get\("status_pills"\)\s*or\s*\["FutureFunded",\s*"Connect ATX Elite",\s*"Launchable now"\]\s*%\}',
        '{% set status_pills = data.get("status_pills") or ["FutureFunded", "Sponsor-ready", "Launch-ready"] %}',
        text,
        count=1,
    )

    if text == original:
        return 0, None

    bak = backup(HOME)
    HOME.write_text(text, encoding="utf-8")
    return n, bak


if __name__ == "__main__":
    if not CSS.exists():
        raise SystemExit(f"missing: {CSS}")

    css_removed, css_bak = patch_css()
    home_changed, home_bak = patch_home()

    print(f"css_removed_blocks: {css_removed}")
    if css_bak:
        print(f"css_backup:         {css_bak}")
    print(f"home_changed:       {home_changed}")
    if home_bak:
        print(f"home_backup:        {home_bak}")
    print(f"css_path:           {CSS}")
    print(f"home_path:          {HOME}")
