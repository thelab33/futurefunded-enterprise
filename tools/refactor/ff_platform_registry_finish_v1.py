from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import re

ROOT = Path.home() / "futurefunded-enterprise"
ROUTES = ROOT / "apps/web/app/routes/platform.py"


def backup(path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    bak = path.with_name(f"{path.name}.bak.{ts}")
    shutil.copy2(path, bak)
    return bak


def write_text(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def replace_once(text: str, old: str, new: str, *, label: str) -> tuple[str, bool]:
    if old in text:
        return text.replace(old, new, 1), True
    if new in text:
        return text, False
    raise RuntimeError(f"could not find expected block for: {label}")


def replace_route_block(text: str, *, route: str, func_name: str, page_key: str) -> tuple[str, bool]:
    replacement = f'''@bp.get("{route}")
def {func_name}():
    return _render_platform_page(page_key="{page_key}")
'''

    if replacement in text:
        return text, False

    pattern = re.compile(
        rf'''@bp\.get\("{re.escape(route)}"\)\s*
def\s+{func_name}\(\):\s*
    return\s+_render_platform_page\(
        .*?
    \)\s*''',
        re.S | re.M,
    )

    new_text, count = pattern.subn(replacement + "\n", text, count=1)
    if count == 0:
        raise RuntimeError(f"could not simplify route block: {func_name} ({route})")
    return new_text, True


def main() -> int:
    print("== FF PLATFORM REGISTRY FINISH V1 ==")

    if not ROUTES.exists():
        raise FileNotFoundError(ROUTES)

    bak = backup(ROUTES)
    text = ROUTES.read_text(encoding="utf-8")
    original = text
    notes: list[str] = []

    api_replacements = [
        ('"api_path": "/platform/home"', '"api_path": "/api/v1/platform/home"', "registry home api_path"),
        ('"api_path": "/platform/pricing"', '"api_path": "/api/v1/platform/pricing"', "registry pricing api_path"),
        ('"api_path": "/platform/demo"', '"api_path": "/api/v1/platform/demo"', "registry demo api_path"),
        ('"api_path": "/platform/onboarding"', '"api_path": "/api/v1/platform/onboarding"', "registry onboarding api_path"),
        ('"api_path": "/platform/dashboard"', '"api_path": "/api/v1/platform/dashboard"', "registry dashboard api_path"),
    ]

    for old, new, label in api_replacements:
        text, changed = replace_once(text, old, new, label=label)
        if changed:
            notes.append(f"updated {label}")

    routes = [
        ("/", "home", "home"),
        ("/onboarding", "onboarding", "onboarding"),
        ("/dashboard", "dashboard", "dashboard"),
        ("/pricing", "pricing", "pricing"),
        ("/demo", "demo", "demo"),
    ]

    for route, func_name, page_key in routes:
        text, changed = replace_route_block(
            text,
            route=route,
            func_name=func_name,
            page_key=page_key,
        )
        if changed:
            notes.append(f"simplified route {func_name} -> page_key={page_key}")

    if text != original:
        write_text(ROUTES, text)

    print(f"patched: {ROUTES}")
    print(f"backup:  {bak}")
    for note in notes:
        print(f"  - {note}")
    print("result:  changed" if text != original else "result:  no-op (already aligned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
