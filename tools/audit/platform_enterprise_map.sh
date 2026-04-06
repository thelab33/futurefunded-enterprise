#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/futurefunded-enterprise}"
cd "$ROOT"

OUT="reports/platform-map"
mkdir -p "$OUT"

# 00) Platform file tree
find apps/web/app/templates/platform -maxdepth 2 -type f | sort > "$OUT/00_platform_tree.txt"

# 01) Routes / path references
rg -n "route\(|Blueprint|@.*route|/platform|/c/" apps/web/app \
  -g '!**/__pycache__/**' \
  > "$OUT/01_routes_and_paths.txt" || true

# 02) Platform template map
rg -n '{% extends "platform/base.html" %}|platform_page|page_title|page_description|{% include "platform/' \
  apps/web/app/templates/platform \
  > "$OUT/02_platform_template_map.txt" || true

# 03) Base nav / chrome map
rg -n 'ff-nav__link|href="/platform/|href="/platform/onboarding|href="/platform/dashboard|href="/platform/pricing|href="/platform/demo|href="/c/' \
  apps/web/app/templates/platform/base.html \
  > "$OUT/03_base_nav_map.txt" || true

# 04) Home data dependencies
rg -n 'data\.[A-Za-z0-9_\.]+' \
  apps/web/app/templates/platform/home.html \
  > "$OUT/04_home_data_dependencies.txt" || true

# 05) Dashboard structure map
rg -n '_intro_split|_promo_bar|ff-platformPanel|ff-platformMiniList|ff-platformInlinePill|Open live campaign|Open campaign page' \
  apps/web/app/templates/platform/dashboard.html \
  > "$OUT/05_dashboard_structure.txt" || true

# 06) Onboarding structure map
rg -n '_intro_split|ff-platformFormGrid|ff-platformFormCard|ff-platformFieldGrid|ff-platformCtaBar|/c/<campaign-slug>|Create org \+ launch page' \
  apps/web/app/templates/platform/onboarding.html \
  > "$OUT/06_onboarding_structure.txt" || true

# 07) Platform CSS hook map
rg -n 'ff-platform|ff-nav__link|ff-platformInlinePill|ff-platformForm|ff-platformPanel|ff-platformCtaBar|ff-platformBrand|ff-chrome|ff-main' \
  apps/web/app/static/css/*.css \
  > "$OUT/07_platform_css_hooks.txt" || true

# 08) Pricing / demo presence
{
  test -f apps/web/app/templates/platform/pricing.html && echo "pricing template: present" || echo "pricing template: missing"
  test -f apps/web/app/templates/platform/demo.html && echo "demo template: present" || echo "demo template: missing"
} > "$OUT/08_pricing_demo_presence.txt"

# 09) Partial presence
find apps/web/app/templates/platform/_partials -maxdepth 2 -type f | sort \
  > "$OUT/09_platform_partials.txt" 2>/dev/null || true

# 10) Enterprise target note
cat > "$OUT/10_enterprise_target.txt" <<'EOF'
Enterprise target map
- base.html = shared shell / chrome authority
- home.html = public platform sales surface
- onboarding.html = guided launch flow
- dashboard.html = operator command center
- pricing.html = commercial offer page
- demo.html = guided live proof page
- campaign page = secondary CTA / live example, not primary platform nav
EOF

echo "Wrote reports to $OUT"
ls -1 "$OUT"
