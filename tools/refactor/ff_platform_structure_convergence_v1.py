from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
STAMP = datetime.now().strftime("%Y%m%d-%H%M%S")
ARCHIVE_ROOT = ROOT / "archive" / "platform-structure-convergence" / STAMP
LOG_PATH = ARCHIVE_ROOT / "convergence_log.txt"

ARCH_DOC = ROOT / "apps" / "web" / "app" / "templates" / "ARCHITECTURE.md"
PLATFORM_BASE = ROOT / "apps" / "web" / "app" / "templates" / "platform" / "base.html"
PLATFORM_BASE_LEGACY = ROOT / "apps" / "web" / "app" / "templates" / "platform" / "shells" / "platform_base_legacy.html"
INTEGRATION_SHARED = ROOT / "apps" / "web" / "app" / "templates" / "shared" / "partials" / "integration_health_panel.html"
INTEGRATION_FLAT = ROOT / "apps" / "web" / "app" / "templates" / "partials" / "integration_health_panel.html"
SCAFFOLD = ROOT / "tools" / "refactor" / "ff_platform_architecture_scaffold.py"

ARCHITECTURE_CONTENT = r'''# FutureFunded Platform Architecture

_Last updated: 2026-04-08_

This document is the canonical filesystem and ownership spec for the FutureFunded platform.

It exists to keep the product launch-safe, reduce template drift, and make sure new work lands in the right layer every time.

---

## 1) Architecture goal

FutureFunded is organized around a clean, production-grade authority chain:

**platform routes → platform pages → platform shells → platform partials → shared primitives → runtime assets**

That chain is the source of truth for platform work.

The public fundraiser remains its own authority lane and should not be mixed into the platform page layer unless the product intentionally merges those surfaces.

---

## 2) Canonical ownership map

### Route authority

These files own live request entrypoints for the product surface:

- `apps/web/app/routes/platform.py`
- `apps/web/app/routes/campaign.py`
- `apps/web/app/routes/payments.py`

#### Route responsibilities

- `platform.py` owns the platform marketing/operator pages.
- `campaign.py` owns the public fundraiser page.
- `payments.py` owns payment and API behavior, not template composition.

---

## 3) Canonical platform page layer

These are the official entry templates for platform UI work:

- `apps/web/app/templates/platform/pages/home.html`
- `apps/web/app/templates/platform/pages/onboarding.html`
- `apps/web/app/templates/platform/pages/dashboard.html`
- `apps/web/app/templates/platform/pages/pricing.html`
- `apps/web/app/templates/platform/pages/demo.html`

### Rule

New platform experience work should start in one of these files, not in legacy wrappers or free-floating partial folders.

---

## 4) Canonical platform shell layer

These shells define the page chrome, high-level layout, and shared page frame for the platform:

- `apps/web/app/templates/platform/shells/marketing_base.html`
- `apps/web/app/templates/platform/shells/operator_base.html`

### Shell intent

- `marketing_base.html` is the shell for public-facing product marketing pages.
- `operator_base.html` is the shell for operator and workspace-style pages.

### Rule

Any new platform page should extend one of these two shells unless there is a deliberate architecture decision to add a third current shell.

---

## 5) Canonical platform partial layer

These are the active platform-specific composition pieces:

- `apps/web/app/templates/platform/partials/_founder_demo_flow_strip.html`
- `apps/web/app/templates/platform/partials/_sponsor_packages_merchandising.html`
- `apps/web/app/templates/platform/partials/_dashboard_operator_premium_strip.html`

### Rule

Platform-only layout fragments and merchandising sections belong here.

If a fragment is reused across platform pages and is not fundraiser-specific, prefer this layer over ad hoc local duplication.

---

## 6) Canonical shared primitives

These files are shared building blocks for the platform layer.

### Shared macros

- `apps/web/app/templates/shared/macros/ui.html`
- `apps/web/app/templates/shared/macros/cards.html`
- `apps/web/app/templates/shared/macros/pills.html`

### Shared partials

- `apps/web/app/templates/shared/partials/_platform_topbar.html`
- `apps/web/app/templates/shared/partials/_platform_status_bar.html`
- `apps/web/app/templates/shared/partials/_cta_band.html`

### Rule

Reusable UI primitives, top-level shared chrome, and shared presentation helpers belong under `shared/`, not in flat `templates/partials/` paths.

---

## 7) Canonical runtime assets

These files are the current platform/campaign runtime authority assets:

### CSS

- `apps/web/app/static/css/ff.css`
- `apps/web/app/static/css/ff-above-main-premium.css`
- `apps/web/app/static/css/platform-pages.css`

### JavaScript

- `apps/web/app/static/js/ff-app.js`
- `apps/web/app/static/js/ff-sponsor-leads-v1.js`

### Rule

Do not create parallel authority CSS/JS files for the same surface unless a lane has been explicitly split.

---

## 8) Compatibility and legacy status

### Compatibility bridge: keep, but do not build new work against it

- `apps/web/app/templates/platform/base.html`

This file exists as a compatibility bridge for older inheritance patterns during transition. It is not the preferred base for new work.

### Legacy-review: keep for now, but treat as non-authority

- `apps/web/app/templates/platform/shells/platform_base_legacy.html`

This file is retained for safety and historical migration context. It should not be the target shell for new implementation.

### Rule

- Do not extend `platform/base.html` for new work.
- Do not extend `platform/shells/platform_base_legacy.html` for new work.
- Prefer `marketing_base.html` or `operator_base.html`.

---

## 9) Integration health panel ownership

Canonical location:

- `apps/web/app/templates/shared/partials/integration_health_panel.html`

Legacy/review location:

- `apps/web/app/templates/partials/integration_health_panel.html`

### Rule

The shared partial path is canonical.

The flat `templates/partials/` copy is transitional drift and should be archived once no live reference depends on it.

Do not create new references to the flat path.

---

## 10) Directory policy

### Where new work goes

#### New platform pages
- `apps/web/app/templates/platform/pages/`

#### New platform-only sections
- `apps/web/app/templates/platform/partials/`

#### New shared UI macros
- `apps/web/app/templates/shared/macros/`

#### New shared page fragments / bars / notices
- `apps/web/app/templates/shared/partials/`

#### New platform shell behavior
- `apps/web/app/templates/platform/shells/`

#### New platform styling
- `apps/web/app/static/css/platform-pages.css`

#### Cross-surface shared styling
- `apps/web/app/static/css/ff.css`

---

## 11) Anti-drift rules

Do **not** introduce new work into these patterns without an explicit architecture decision:

- `apps/web/app/templates/partials/`
- duplicate shell families for the same surface
- second authority CSS files for the same page lane
- route-to-template indirection that cannot be traced from config or helper contracts
- copy-paste shared partials across folders when a canonical shared location already exists

---

## 12) Platform route contract

`apps/web/app/routes/platform.py` is the route contract for platform pages.

It should preserve a clear mapping between page keys and template names. The helper-driven config structure is acceptable and preferred when it remains explicit and traceable.

### Contract requirements

- each page key must map to a single canonical template
- the template name must remain explicit in config or helper logic
- helper-based rendering must stay audit-friendly
- route ownership must remain easy to prove by grep or audit scripts

---

## 13) Review lane

These files are not deleted automatically, but they are not part of the current preferred authority chain:

- `apps/web/app/templates/platform/base.html`
- `apps/web/app/templates/platform/shells/platform_base_legacy.html`
- `apps/web/app/templates/partials/integration_health_panel.html`

### Review intent

- preserve compatibility
- reduce accidental breakage
- prevent new work from drifting into old lanes

---

## 14) Launch-safe workflow

When touching the platform architecture:

1. update the page, shell, partial, or shared primitive in its canonical folder
2. avoid introducing alternate copies in old locations
3. rerun architecture and repo audits
4. verify route ownership and template composition
5. keep the authority chain intact

---

## 15) Summary

FutureFunded’s flagship structure is:

- **Routes:** platform / campaign / payments
- **Platform pages:** `platform/pages/*`
- **Current shells:** `platform/shells/marketing_base.html`, `platform/shells/operator_base.html`
- **Platform partials:** `platform/partials/*`
- **Shared primitives:** `shared/macros/*`, `shared/partials/*`
- **Compatibility bridge:** `platform/base.html`
- **Legacy-review:** `platform_base_legacy.html`
- **Canonical integration panel:** `shared/partials/integration_health_panel.html`

Any future restructure should strengthen this chain, not weaken it.
'''

COMPAT_COMMENT = """{#\n  FUTUREFUNDED_ARCHITECTURE_STATUS\n  compatibility-only bridge\n  - retained for older inheritance transition safety\n  - do not target for new platform work\n  - prefer platform/shells/marketing_base.html or operator_base.html\n#}\n\n"""

LEGACY_COMMENT = """{#\n  FUTUREFUNDED_ARCHITECTURE_STATUS\n  legacy-review shell\n  - retained for migration safety and repo history\n  - do not target for new platform work\n  - current authority shells are marketing_base.html and operator_base.html\n#}\n\n"""


def backup(path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = path.with_name(f"{path.name}.{ts}.bak")
    shutil.copy2(path, dest)
    return dest


def prepend_once(path: Path, block: str, marker: str, log: list[str]) -> None:
    if not path.exists():
        log.append(f"SKIP missing: {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    if marker in text:
        log.append(f"UNCHANGED marker already present: {path.relative_to(ROOT)}")
        return
    b = backup(path)
    path.write_text(block + text, encoding="utf-8")
    log.append(f"PATCHED banner: {path.relative_to(ROOT)}")
    log.append(f"BACKUP: {b.relative_to(ROOT)}")


def replace_in_file(path: Path, old: str, new: str, log: list[str]) -> None:
    if not path.exists():
        log.append(f"SKIP missing: {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    if old not in text:
        log.append(f"UNCHANGED no match in: {path.relative_to(ROOT)}")
        return
    if old == new:
        log.append(f"UNCHANGED identical replace request: {path.relative_to(ROOT)}")
        return
    b = backup(path)
    path.write_text(text.replace(old, new), encoding="utf-8")
    log.append(f"PATCHED text replace: {path.relative_to(ROOT)}")
    log.append(f"BACKUP: {b.relative_to(ROOT)}")


def write_architecture(log: list[str]) -> None:
    ARCH_DOC.parent.mkdir(parents=True, exist_ok=True)
    if ARCH_DOC.exists():
        b = backup(ARCH_DOC)
        log.append(f"BACKUP: {b.relative_to(ROOT)}")
    ARCH_DOC.write_text(ARCHITECTURE_CONTENT.strip() + "\n", encoding="utf-8")
    log.append(f"WROTE architecture doc: {ARCH_DOC.relative_to(ROOT)}")


def converge_integration_panel(log: list[str]) -> None:
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
    if INTEGRATION_SHARED.exists() and INTEGRATION_FLAT.exists():
        archive_dest = ARCHIVE_ROOT / "integration_health_panel.legacy.flat.html"
        archive_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(INTEGRATION_FLAT), str(archive_dest))
        log.append(
            f"ARCHIVED legacy flat integration panel: {archive_dest.relative_to(ROOT)}"
        )
    elif not INTEGRATION_SHARED.exists() and INTEGRATION_FLAT.exists():
        INTEGRATION_SHARED.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(INTEGRATION_FLAT), str(INTEGRATION_SHARED))
        log.append(
            f"MOVED flat integration panel to canonical shared path: {INTEGRATION_SHARED.relative_to(ROOT)}"
        )
    elif INTEGRATION_SHARED.exists():
        log.append(
            f"UNCHANGED canonical integration panel already present: {INTEGRATION_SHARED.relative_to(ROOT)}"
        )
    else:
        log.append("SKIP no integration panel file found in either location")

    replace_in_file(
        SCAFFOLD,
        'TEMPLATES / "partials/integration_health_panel.html"',
        'TEMPLATES / "shared/partials/integration_health_panel.html"',
        log,
    )
    replace_in_file(
        SCAFFOLD,
        'copy_if_exists(shared_integration, TEMPLATES / "platform/partials/integration_health_panel.html")\n',
        '',
        log,
    )


def main() -> None:
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
    log: list[str] = []
    log.append(f"repo: {ROOT}")
    log.append(f"archive_root: {ARCHIVE_ROOT.relative_to(ROOT)}")
    log.append("")

    log.append("== WRITE ARCHITECTURE DOC ==")
    write_architecture(log)
    log.append("")

    log.append("== LABEL COMPAT / LEGACY FILES ==")
    prepend_once(PLATFORM_BASE, COMPAT_COMMENT, "FUTUREFUNDED_ARCHITECTURE_STATUS", log)
    prepend_once(PLATFORM_BASE_LEGACY, LEGACY_COMMENT, "FUTUREFUNDED_ARCHITECTURE_STATUS", log)
    log.append("")

    log.append("== CONVERGE INTEGRATION PANEL ==")
    converge_integration_panel(log)
    log.append("")

    LOG_PATH.write_text("\n".join(log) + "\n", encoding="utf-8")
    print(f"wrote: {LOG_PATH}")


if __name__ == "__main__":
    main()

