from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"

FILES = [
    ROOT / "apps/web/app/templates/campaign/index.html",
    ROOT / "apps/web/app/templates/platform/pages/home.html",
    ROOT / "apps/web/app/templates/platform/pages/pricing.html",
    ROOT / "apps/web/app/templates/platform/pages/demo.html",
    ROOT / "apps/web/app/templates/shared/partials/_platform_topbar.html",
]

for path in FILES:
    if path.exists():
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        shutil.copy2(path, path.with_name(f"{path.name}.{ts}.bak"))

def patch_file(path: Path, replacements: list[tuple[str, str, str]]) -> None:
    if not path.exists():
        print(f"SKIP: missing file {path}")
        return

    text = path.read_text(encoding="utf-8")
    changed_any = False

    for old, new, label in replacements:
        if old in text:
            text = text.replace(old, new, 1)
            changed_any = True
            print(f"changed: {label}")
        else:
            print(f"MISS: {label}")

    if changed_any:
        path.write_text(text, encoding="utf-8")

# -------------------------------------------------------------------
# campaign credibility
# -------------------------------------------------------------------
patch_file(
    ROOT / "apps/web/app/templates/campaign/index.html",
    [
        (
            "Support the program while getting real local visibility. Sponsorships may be tax-deductible, custom packages are available, and invoices can be arranged for larger supporters.",
            "Support the program while getting real local visibility. Sponsorships may be tax-deductible, custom packages are available, invoices can be arranged for larger supporters, and featured visibility is currently open for founding partners.",
            "campaign sponsor pitch credibility boost",
        ),
        (
            "Support the teams you know while every gift still helps the full program.",
            "Support the teams you know while every gift still helps the full program. Team cards show who the program serves, while support still feeds the shared program fund unless a restricted campaign is clearly marked.",
            "campaign shared-fund clarification",
        ),
        (
            "Every gift supports the full program and helps cover tournament fees, gym time, and team development.",
            "Every gift supports the shared program fund and helps cover tournament fees, gym time, and team development.",
            "campaign team card shared-fund note 1",
        ),
        (
            "Every gift supports the full program and helps cover weekend travel, entry fees, and more reps for the team.",
            "Every gift supports the shared program fund and helps cover weekend travel, entry fees, and more reps for the team.",
            "campaign team card shared-fund note 2",
        ),
        (
            "Every gift supports the full program and helps cover uniforms, team meals, and game-day essentials.",
            "Every gift supports the shared program fund and helps cover uniforms, team meals, and game-day essentials.",
            "campaign team card shared-fund note 3",
        ),
        (
            "Every gift supports the full program and helps cover gym rentals, training sessions, and weekly development.",
            "Every gift supports the shared program fund and helps cover gym rentals, training sessions, and weekly development.",
            "campaign team card shared-fund note 4",
        ),
    ],
)

# -------------------------------------------------------------------
# platform home credibility / CTA consistency
# -------------------------------------------------------------------
patch_file(
    ROOT / "apps/web/app/templates/platform/pages/home.html",
    [
        (
            "Launch Connect ATX Elite",
            "Start guided launch",
            "home hero primary cta",
        ),
        (
            "Open dashboard",
            "Open operator dashboard",
            "home hero secondary cta",
        ),
        (
            "Create organization",
            "Start founder setup",
            "home close primary cta",
        ),
        (
            "Manage platform",
            "Open operator dashboard",
            "home close secondary cta",
        ),
    ],
)

# -------------------------------------------------------------------
# pricing credibility / CTA consistency
# -------------------------------------------------------------------
patch_file(
    ROOT / "apps/web/app/templates/platform/pages/pricing.html",
    [
        (
            "Claim founder setup",
            "Start founder setup",
            "pricing founder cta label",
        ),
        (
            "View live demo",
            "Open guided demo",
            "pricing founder secondary cta",
        ),
        (
            "Request white-label path",
            "Talk to founder",
            "pricing white-label cta label",
        ),
    ],
)

# -------------------------------------------------------------------
# demo credibility / CTA consistency
# -------------------------------------------------------------------
patch_file(
    ROOT / "apps/web/app/templates/platform/pages/demo.html",
    [
        (
            "Launch your program",
            "Start guided launch",
            "demo close primary cta",
        ),
        (
            "View live example",
            "Open live fundraiser",
            "demo close secondary cta",
        ),
    ],
)

# -------------------------------------------------------------------
# global platform topbar consistency
# -------------------------------------------------------------------
patch_file(
    ROOT / "apps/web/app/templates/shared/partials/_platform_topbar.html",
    [
        (
            "Live example",
            "Open live fundraiser",
            "topbar secondary cta",
        ),
        (
            "Start launch",
            "Start guided launch",
            "topbar primary cta",
        ),
    ],
)

print("done.")
