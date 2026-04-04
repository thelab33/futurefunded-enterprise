# FutureFunded Ownership Rules

## CSS
- ff.css = shared/public/campaign design system
- platform-pages.css = platform-only pages
- campaign pages must not load platform-pages.css

## JS
- ff-app.js = campaign runtime
- platform-app.js = platform runtime

## Config
- PUBLIC_BASE_URL / CANONICAL_BASE_URL / STRIPE_RETURN_URL are required for production
- localhost values must never render in production HTML

## Hygiene
- no backup files inside apps/
- generated reports belong in artifacts/
- audits live in scripts/audit/
