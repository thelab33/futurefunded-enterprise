# FutureFunded Frontend Ownership

## CSS ownership
- `apps/web/app/static/css/ff.css`
  - shared cross-app foundation
  - campaign core primitives
  - safe shared utilities used by both campaign and platform

- `apps/web/app/static/css/platform-pages.css`
  - platform-only layout and presentation
  - onboarding, dashboard, pricing, demo, and platform home
  - should own platform-specific overrides and layout helpers

- `apps/web/app/static/css/ff-above-main-premium.css`
  - campaign premium bridge / residual campaign-only layer
  - do **not** load by default on platform pages
  - opt in only when a specific platform page explicitly needs it

## Template ownership
- `apps/web/app/templates/campaign/index.html`
  - public campaign surface only

- `apps/web/app/templates/platform/base.html`
  - shared platform shell only
  - shared nav, trust strip, canonical/meta, platform config payload

- `apps/web/app/templates/platform/*.html`
  - page-specific platform content only
  - avoid inline styles
  - avoid redefining global shell behavior here

## Cleanup rule
When changing platform UI:
1. Prefer `platform-pages.css`
2. Use `ff.css` only for shared primitives
3. Avoid touching campaign template/CSS unless the campaign itself changed
