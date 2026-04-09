from __future__ import annotations

from pathlib import Path
import shutil
from datetime import datetime

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATES = ROOT / "apps/web/app/templates"
ROUTES = ROOT / "apps/web/app/routes/platform.py"
ARCHIVE = ROOT / "archive/template-backups" / datetime.now().strftime("%Y%m%d-%H%M%S")

DIRS = [
    TEMPLATES / "shared/partials",
    TEMPLATES / "shared/macros",
    TEMPLATES / "platform/shells",
    TEMPLATES / "platform/pages",
    TEMPLATES / "platform/partials",
    TEMPLATES / "campaign/partials",
]

PAGE_FILES = ["home.html", "onboarding.html", "dashboard.html", "pricing.html", "demo.html"]

PLACEHOLDERS = {
    TEMPLATES / "shared/partials/_platform_topbar.html": "{# FutureFunded shared topbar partial #}\n",
    TEMPLATES / "shared/partials/_platform_status_bar.html": "{# FutureFunded shared platform status strip partial #}\n",
    TEMPLATES / "shared/partials/_cta_band.html": "{# FutureFunded shared CTA band partial #}\n",
    TEMPLATES / "shared/partials/_section_header.html": "{# FutureFunded shared section header partial #}\n",
    TEMPLATES / "shared/partials/_footer_minimal.html": "{# FutureFunded shared minimal footer partial #}\n",
    TEMPLATES / "shared/macros/ui.html": "{# FutureFunded shared UI macros #}\n",
    TEMPLATES / "shared/macros/cards.html": "{# FutureFunded shared card macros #}\n",
    TEMPLATES / "shared/macros/pills.html": "{# FutureFunded shared pill / badge macros #}\n",
    TEMPLATES / "campaign/partials/.gitkeep": "",
}

def ensure_dirs() -> None:
    for d in DIRS:
        d.mkdir(parents=True, exist_ok=True)

def copy_if_exists(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

def move_backup_files() -> list[Path]:
    moved = []
    if not TEMPLATES.exists():
      return moved

    for p in TEMPLATES.rglob("*"):
        if not p.is_file():
            continue
        name = p.name
        if ".bak" in name or name.endswith(".launch-freeze"):
            rel = p.relative_to(TEMPLATES)
            target = ARCHIVE / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(p), str(target))
            moved.append(rel)
    return moved

def scaffold_platform_files() -> None:
    for name in PAGE_FILES:
        copy_if_exists(TEMPLATES / "platform" / name, TEMPLATES / "platform/pages" / name)

    base_src = TEMPLATES / "platform/base.html"
    if base_src.exists():
        copy_if_exists(base_src, TEMPLATES / "platform/shells/platform_base_legacy.html")
        copy_if_exists(base_src, TEMPLATES / "platform/shells/marketing_base.html")
        copy_if_exists(base_src, TEMPLATES / "platform/shells/operator_base.html")

    legacy_partials = TEMPLATES / "platform/_partials"
    if legacy_partials.exists():
        for p in legacy_partials.glob("*.html"):
            copy_if_exists(p, TEMPLATES / "platform/partials" / p.name)

    shared_integration = TEMPLATES / "shared/partials/integration_health_panel.html"
    if shared_integration.exists():
                copy_if_exists(shared_integration, TEMPLATES / "shared/partials/integration_health_panel.html")

    for path, content in PLACEHOLDERS.items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

def rewrite_routes() -> None:
    text = ROUTES.read_text(encoding="utf-8")

    replacements = {
        'render_template(\n        "platform/home.html",': 'render_template(\n        "platform/pages/home.html",',
        'render_template(\n        "platform/onboarding.html",': 'render_template(\n        "platform/pages/onboarding.html",',
        'render_template(\n        "platform/dashboard.html",': 'render_template(\n        "platform/pages/dashboard.html",',
        'return render_template(\n        "platform/pricing.html"\n    )': 'return render_template(\n        "platform/pages/pricing.html",\n        page_title="FutureFunded Pricing",\n        platform_page="pricing",\n    )',
        'return render_template(\n        "platform/demo.html"\n    )': 'return render_template(\n        "platform/pages/demo.html",\n        page_title="FutureFunded Demo",\n        platform_page="demo",\n    )',
    }

    original = text
    for old, new in replacements.items():
        if old in text:
            text = text.replace(old, new)

    if text != original:
        bak = ROUTES.with_name(ROUTES.name + ".bak-platform-architecture-scaffold")
        if not bak.exists():
            bak.write_text(original, encoding="utf-8")
        ROUTES.write_text(text, encoding="utf-8")

def write_architecture_note() -> None:
    note = TEMPLATES / "ARCHITECTURE.md"
    note.write_text(
        "\n".join([
            "# FutureFunded template architecture",
            "",
            "## Current target structure",
            "- shared/partials: global chrome / repeated shell pieces",
            "- shared/macros: buttons, pills, cards, reusable UI atoms",
            "- platform/shells: marketing/operator shell variants",
            "- platform/pages: routed platform pages",
            "- platform/partials: platform-specific reusable sections",
            "- campaign/index.html: public fundraising funnel",
            "- campaign/partials: future campaign section extraction",
            "",
            "## Migration strategy",
            "1. Keep current live paths working",
            "2. Move routed pages into platform/pages",
            "3. Preserve platform/base.html during transition",
            "4. Extract repeated sections only after shell split is stable",
            "",
        ]),
        encoding="utf-8",
    )

def main() -> None:
    if not TEMPLATES.exists():
        raise SystemExit(f"Missing templates dir: {TEMPLATES}")
    if not ROUTES.exists():
        raise SystemExit(f"Missing routes file: {ROUTES}")

    ensure_dirs()
    scaffold_platform_files()
    moved = move_backup_files()
    rewrite_routes()
    write_architecture_note()

    print("✅ FutureFunded platform architecture scaffold complete")
    print(f"📁 templates: {TEMPLATES}")
    print(f"🗃 archive : {ARCHIVE}")
    print(f"🧹 backups moved: {len(moved)}")
    for rel in moved[:20]:
        print(f"   - {rel}")
    if len(moved) > 20:
        print(f"   … and {len(moved) - 20} more")

if __name__ == "__main__":
    main()
