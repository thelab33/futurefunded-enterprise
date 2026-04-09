# FutureFunded Platform Architecture

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

Archived former flat location:

- `archive/platform-structure-convergence/20260408-145121/integration_health_panel.legacy.flat.html`

### Rule

The shared partial path is canonical.

The old flat `templates/partials/` copy has been archived and should not be restored as a live template path.

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
