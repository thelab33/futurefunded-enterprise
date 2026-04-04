# FutureFunded platform structure snapshot

## apps
├── api/
│   ├── alembic/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── health.py
│   │   │   │   └── platform.py
│   │   │   ├── __init__.py
│   │   │   └── router.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── settings.py
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── alembic.ini
│   └── requirements.txt
└── web/
    ├── app/
    │   ├── data/
    │   │   ├── campaign_store.py
    │   │   └── campaigns.json
    │   ├── routes/
    │   │   ├── __init__.py
    │   │   ├── campaign.py
    │   │   ├── campaign.py.bak-public-base-20260331-232041
    │   │   ├── platform.py
    │   │   ├── platform.py.bak-dashboard-inject-20260401-004500
    │   │   ├── platform.py.bak-dashboard-route-20260401-003851
    │   │   └── platform.py.bak-dashboard-smart-20260401-004904
    │   ├── services/
    │   │   ├── __init__.py
    │   │   └── api_client.py
    │   ├── static/
    │   │   ├── css/
    │   │   │   ├── ff-above-main-premium.css
    │   │   │   ├── ff-above-main-premium.css.bak-campaign-compression-pass2-20260401-011807
    │   │   │   ├── ff-above-main-premium.css.bak-checkout-conversion
    │   │   │   ├── ff-above-main-premium.css.bak-checkout-micropolish
    │   │   │   ├── ff-above-main-premium.css.bak-fundraiser-chrome-canonical-20260401-015927
    │   │   │   ├── ff-above-main-premium.css.bak-fundraiser-chrome-micropolish-20260401-021248
    │   │   │   ├── ff-above-main-premium.css.bak-overrides-only-20260401-025348
    │   │   │   ├── ff-above-main-premium.css.bak-strip-dead-chrome-20260401-020643
    │   │   │   ├── ff-above-main-premium.css.bak.calm-hierarchy
    │   │   │   ├── ff.css
    │   │   │   ├── platform-pages.css
    │   │   │   └── platform-pages.css.bak-pass4-20260331-203953
    │   │   ├── images/
    │   │   │   ├── hero/
    │   │   │   │   ├── hero-1280.avif
    │   │   │   │   ├── hero-1280.webp
    │   │   │   │   ├── hero-1920.avif
    │   │   │   │   ├── hero-1920.webp
    │   │   │   │   ├── hero-960.avif
    │   │   │   │   ├── hero-960.webp
    │   │   │   │   ├── hero-lqip.txt.br
    │   │   │   │   └── hero-lqip.txt.gz
    │   │   │   ├── optimized/
    │   │   │   │   ├── connect-atx-team.avif
    │   │   │   │   ├── connect-atx-team.webp
    │   │   │   │   ├── og_connect_atx_elite.avif
    │   │   │   │   └── og_connect_atx_elite.webp
    │   │   │   ├── teams/
    │   │   │   │   ├── 6th.webp
    │   │   │   │   ├── 7th.webp
    │   │   │   │   └── 8th.webp
    │   │   │   ├── 49b3c83f5b8d5dae45a6b9eb17430e30.jpg
    │   │   │   ├── 7thBlack.png
    │   │   │   ├── 7thGold.jpg
    │   │   │   ├── 7thGold.webp
    │   │   │   ├── 8thGold.jpg
    │   │   │   ├── apple-touch-icon.png
    │   │   │   ├── connect-atx-team - Copy.jpg
    │   │   │   ├── connect-atx-team.jpg
    │   │   │   ├── connect-atx-team_2.jpg
    │   │   │   ├── connect-atx-team_3.jpg
    │   │   │   ├── favicon.ico
    │   │   │   ├── fundchamps-fc.svg
    │   │   │   ├── fundchamps-logo.svg.br
    │   │   │   ├── fundchamps-logo.svg.gz
    │   │   │   ├── futurefunded-mark.svg
    │   │   │   ├── icon-192.png
    │   │   │   ├── icon-32.png
    │   │   │   ├── icon-512.png
    │   │   │   ├── logo.avif
    │   │   │   ├── logo.webp
    │   │   │   ├── news-poster.webp
    │   │   │   ├── og.jpg
    │   │   │   ├── og.webp
    │   │   │   ├── og_connect_atx_elite.jpg
    │   │   │   ├── og_connect_atx_elite.webp
    │   │   │   ├── safari-pinned-tab.svg
    │   │   │   ├── TeamImage1.avif
    │   │   │   └── TeamRings.webp
    │   │   ├── js/
    │   │   │   ├── ff-app.js
    │   │   │   ├── ff-app.js.bak-before-temp-repair
    │   │   │   ├── ff-app.js.bak-checkout-chip-cleanup
    │   │   │   ├── ff-app.js.bak-checkout-chip-sync-v2
    │   │   │   ├── ff-app.js.bak-no-socket-20260401-002651
    │   │   │   ├── ff-app.js.bak-remove-checkout-chip-sync-v2
    │   │   │   ├── ff-app.js.bak-socket-fix-20260401-004428
    │   │   │   ├── ff-app.js.bak-sync-amount-chip-state-premium
    │   │   │   ├── ff-app.js.bak-theme-rescue-v1
    │   │   │   └── ff-sponsor-leads-v1.js
    │   │   └── manifest.webmanifest
    │   ├── templates/
    │   │   ├── campaign/
    │   │   │   ├── index.html
    │   │   │   ├── index.html.bak-campaign-arch-note-20260401-011040
    │   │   │   ├── index.html.bak-campaign-compress-hero-20260401-011007
    │   │   │   ├── index.html.bak-campaign-faq-endcap-20260401-011017
    │   │   │   ├── index.html.bak-checkout-conversion-markup
    │   │   │   ├── index.html.bak-checkout-flagship-upgrade
    │   │   │   ├── index.html.bak-debug-strip-20260331-232035
    │   │   │   ├── index.html.bak-socket-quiet-20260331-232029
    │   │   │   └── index.html.bak.jinja-hotfix
    │   │   ├── partials/
    │   │   │   └── integration_health_panel.html
    │   │   └── platform/
    │   │       ├── base.html
    │   │       ├── base.html.bak-platform-css-20260331-192630
    │   │       ├── dashboard.html
    │   │       ├── dashboard.html.bak-dashboard-cta-20260401-004511
    │   │       ├── dashboard.html.bak-dashboard-latest-card-20260401-005209
    │   │       ├── dashboard.html.bak-dashboard-template-20260401-003901
    │   │       ├── dashboard.html.bak-pass4-20260331-203953
    │   │       ├── home.html
    │   │       ├── onboarding.html
    │   │       └── onboarding.html.bak-pass4-20260331-203953
    │   ├── __init__.py
    │   ├── __init__.py.bak-campaign-20260331-230645
    │   ├── config.py
    │   └── extensions.py
    ├── requirements.txt
    └── wsgi.py

## packages
├── shared/
│   ├── clients/
│   ├── schemas/
│   ├── settings/
│   │   ├── __init__.py
│   │   └── base.py
│   └── __init__.py
└── __init__.py

## infra
├── docker/
├── nginx/
└── systemd/

## scripts
└── audit/
    └── ff_launch_runtime_gate.sh

## docs
└── audits/

## README.md
- README.md

## Makefile
- Makefile
