from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"

ROUTES = ROOT / "apps/web/app/routes/platform.py"
ONBOARDING = ROOT / "apps/web/app/templates/platform/pages/onboarding.html"
DASHBOARD = ROOT / "apps/web/app/templates/platform/pages/dashboard.html"

FILES = [ROUTES, ONBOARDING, DASHBOARD]


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


def patch_routes(path: Path) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8")
    original = text
    notes: list[str] = []

    old_home_cta_block = """            "primary_cta_label": "Launch Connect ATX Elite",
            "primary_cta_href": "/platform/onboarding",
            "secondary_cta_label": "Open dashboard",
            "secondary_cta_href": "/platform/dashboard","""
    new_home_cta_block = """            "primary_cta_label": "Start guided launch",
            "primary_cta_href": "/platform/onboarding",
            "secondary_cta_label": "View live example",
            "secondary_cta_href": "/c/spring-fundraiser","""

    text, changed = replace_once(
        text,
        old_home_cta_block,
        new_home_cta_block,
        label="home hero CTA block",
    )
    if changed:
        notes.append("aligned home hero CTAs with marketing funnel")

    old_next_move_block = """            "primary_cta_label": "Create organization",
            "primary_cta_href": "/platform/onboarding",
            "secondary_cta_label": "Manage platform",
            "secondary_cta_href": "/platform/dashboard","""
    new_next_move_block = """            "primary_cta_label": "Create organization",
            "primary_cta_href": "/platform/onboarding",
            "secondary_cta_label": "View pricing",
            "secondary_cta_href": "/platform/pricing","""

    text, changed = replace_once(
        text,
        old_next_move_block,
        new_next_move_block,
        label="home next move CTA block",
    )
    if changed:
        notes.append("aligned home next-move CTAs with pricing path")

    old_dashboard_actions = """        "actions": [
            {"label": "Create another org", "href": "/platform/onboarding", "variant": "primary"},
            {"label": "Open live campaign", "href": "/c/spring-fundraiser", "variant": "secondary"},
        ],"""
    new_dashboard_actions = """        "actions": [
            {"label": "Open live campaign", "href": "/c/spring-fundraiser", "variant": "primary"},
            {"label": "Create another org", "href": "/platform/onboarding", "variant": "secondary"},
        ],"""

    text, changed = replace_once(
        text,
        old_dashboard_actions,
        new_dashboard_actions,
        label="dashboard action order",
    )
    if changed:
        notes.append("reordered dashboard actions for operator-first flow")

    changed_any = text != original
    if changed_any:
        write_text(path, text)
    return changed_any, notes


def patch_onboarding(path: Path) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8")
    original = text
    notes: list[str] = []

    old_block = '{{ ff_cta_pair(submit_label, submit_href, "Back to platform home", "/platform/") }}'
    new_block = '{{ ff_cta_pair(submit_label, submit_href, "Preview live page", "/c/spring-fundraiser") }}'

    text, changed = replace_once(
        text,
        old_block,
        new_block,
        label="onboarding launch outcome CTA pair",
    )
    if changed:
        notes.append("changed onboarding secondary CTA to preview live page")

    changed_any = text != original
    if changed_any:
        write_text(path, text)
    return changed_any, notes


def patch_dashboard(path: Path) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8")
    original = text
    notes: list[str] = []

    old_block = """          {{ ff_cta_pair(
            actions[0].get("label", "Start guided launch") if actions|length > 0 else "Start guided launch",
            actions[0].get("href", "/platform/onboarding") if actions|length > 0 else "/platform/onboarding",
            actions[1].get("label", "Open live fundraiser") if actions|length > 1 else "Open live fundraiser",
            actions[1].get("href", "/c/spring-fundraiser") if actions|length > 1 else "/c/spring-fundraiser"
          ) }}"""

    new_block = """          {{ ff_cta_pair(
            actions[0].get("label", "Open live fundraiser") if actions|length > 0 else "Open live fundraiser",
            actions[0].get("href", "/c/spring-fundraiser") if actions|length > 0 else "/c/spring-fundraiser",
            actions[1].get("label", "Create another org") if actions|length > 1 else "Create another org",
            actions[1].get("href", "/platform/onboarding") if actions|length > 1 else "/platform/onboarding"
          ) }}"""

    text, changed = replace_once(
        text,
        old_block,
        new_block,
        label="dashboard hero CTA pair defaults",
    )
    if changed:
        notes.append("aligned dashboard CTA defaults with operator priority")

    changed_any = text != original
    if changed_any:
        write_text(path, text)
    return changed_any, notes


def main() -> int:
    print("== FF PLATFORM OPERATOR + ROUTE PASS V1 ==")

    backups = []
    for path in FILES:
        if not path.exists():
            raise FileNotFoundError(path)
        backups.append((path, backup(path)))

    changed_any = False

    changed, notes = patch_routes(ROUTES)
    changed_any = changed_any or changed
    print(f"patched: {ROUTES}")
    for note in notes:
        print(f"  - {note}")

    changed, notes = patch_onboarding(ONBOARDING)
    changed_any = changed_any or changed
    print(f"patched: {ONBOARDING}")
    for note in notes:
        print(f"  - {note}")

    changed, notes = patch_dashboard(DASHBOARD)
    changed_any = changed_any or changed
    print(f"patched: {DASHBOARD}")
    for note in notes:
        print(f"  - {note}")

    print("\\nbackups:")
    for path, bak in backups:
        print(f"  - {path.name} -> {bak.name}")

    print("\\nresult:")
    print("  - changed" if changed_any else "  - no-op (already aligned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
