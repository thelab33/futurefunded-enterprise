#!/usr/bin/env bash
set -euo pipefail

echo "== PLATFORM ASSET OWNERS =="
rg -n "platform-pages\.css|platform-app\.js" apps/web/app/templates | sed -n '1,200p' || true

echo
echo "== SHARED FUNDRAISER ASSET OWNERS =="
rg -n "ff\.css|ff-app\.js" apps/web/app/templates | sed -n '1,260p' || true

echo
echo "== CAMPAIGN TEMPLATE EXTENDS CHAIN =="
rg -n "{% extends " apps/web/app/templates/campaign apps/web/app/templates/_layouts apps/web/app/templates/platform 2>/dev/null | sed -n '1,260p' || true
