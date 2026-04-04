from __future__ import annotations

from pathlib import Path
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
TPL = ROOT / "apps/web/app/templates/platform"
BASE = TPL / "base.html"

MARKETING_PAGES = ["home.html", "pricing.html", "demo.html"]
OPERATOR_PAGES = ["onboarding.html", "dashboard.html"]


def write_shell(src: Path, dst: Path, label: str) -> None:
    text = src.read_text(encoding="utf-8")
    text = text.replace("FutureFunded • Platform Base", f"FutureFunded • {label} Base")

    if 'data-ff-platform="true"' in text and 'data-ff-platform-surface=' not in text:
        text = text.replace(
            'data-ff-platform="true"',
            f'data-ff-platform="true"\n  data-ff-platform-surface="{label.lower()}"',
            1,
        )

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")


def retarget(page_path: Path, new_base: str) -> bool:
    if not page_path.exists():
        return False

    text = page_path.read_text(encoding="utf-8")
    candidates = [
        '{% extends "platform/base.html" %}',
        "{% extends 'platform/base.html' %}",
        '{% extends "platform/shells/platform_base_legacy.html" %}',
        "{% extends 'platform/shells/platform_base_legacy.html' %}",
        '{% extends "platform/shells/marketing_base.html" %}',
        "{% extends 'platform/shells/marketing_base.html' %}",
        '{% extends "platform/shells/operator_base.html" %}',
        "{% extends 'platform/shells/operator_base.html' %}",
    ]

    replacement = '{% extends "' + new_base + '" %}'
    changed = False

    for candidate in candidates:
        if candidate in text:
            text = text.replace(candidate, replacement, 1)
            changed = True
            break

    if changed:
        page_path.write_text(text, encoding="utf-8")

    return changed


def main() -> None:
    if not BASE.exists():
        raise SystemExit(f"Missing base template: {BASE}")

    marketing = TPL / "shells/marketing_base.html"
    operator = TPL / "shells/operator_base.html"
    legacy = TPL / "shells/platform_base_legacy.html"

    shutil.copy2(BASE, legacy)
    write_shell(BASE, marketing, "Marketing")
    write_shell(BASE, operator, "Operator")

    changed = []

    for name in MARKETING_PAGES:
        p = TPL / "pages" / name
        if retarget(p, "platform/shells/marketing_base.html"):
            changed.append(str(p.relative_to(ROOT)))

    for name in OPERATOR_PAGES:
        p = TPL / "pages" / name
        if retarget(p, "platform/shells/operator_base.html"):
            changed.append(str(p.relative_to(ROOT)))

    print("✅ platform base split scaffold complete")
    print(f"marketing shell: {marketing}")
    print(f"operator shell : {operator}")
    print(f"legacy shell   : {legacy}")
    print("retargeted pages:")
    for item in changed:
        print(f" - {item}")


if __name__ == "__main__":
    main()
