#!/usr/bin/env bash
set -euo pipefail

FAIL=0

check_no() {
  local pattern="$1"
  local target="$2"
  local label="$3"
  if rg -n "$pattern" "$target" >/dev/null; then
    echo "❌ $label"
    rg -n "$pattern" "$target" | sed -n '1,20p'
    FAIL=1
  else
    echo "✅ $label"
  fi
}

check_yes() {
  local pattern="$1"
  local target="$2"
  local label="$3"
  if rg -n "$pattern" "$target" >/dev/null; then
    echo "✅ $label"
    rg -n "$pattern" "$target" | sed -n '1,20p'
  else
    echo "❌ $label"
    FAIL=1
  fi
}

check_no_backup_files() {
  local label="$1"
  local hits
  hits="$(find apps -type f \( -iname '*.bak' -o -iname '*.bak-*' -o -iname '*.bak.*' -o -iname '*.old' -o -iname '*.backup' \) | sed -n '1,40p')"
  if [[ -n "$hits" ]]; then
    echo "❌ $label"
    printf '%s\n' "$hits"
    FAIL=1
  else
    echo "✅ $label"
  fi
}

echo "== FF REPO OWNER GATE =="

echo
echo "== CAMPAIGN TEMPLATE OWNERSHIP =="
check_yes "css/ff\.css" "apps/web/app/templates/campaign" "campaign templates should own ff.css"
check_yes "js/ff-app\.js" "apps/web/app/templates/campaign" "campaign templates should own ff-app.js"
check_no "platform-pages\.css|platform-app\.js" "apps/web/app/templates/campaign" "campaign templates should not own platform assets"

echo
echo "== PLATFORM TEMPLATE OWNERSHIP =="
check_yes "platform-pages\.css" "apps/web/app/templates/platform" "platform templates should own platform-pages.css"
check_yes "css/ff\.css" "apps/web/app/templates/platform" "platform templates should also own ff.css"

echo
echo "== LIVE APP TREE CLEANLINESS =="
check_no_backup_files "apps tree should be backup-clean"

echo
if [[ "$FAIL" -eq 0 ]]; then
  echo "✅ PASS — repo ownership gate cleared"
else
  echo "❌ FAIL — repo ownership rules were violated"
  exit 1
fi
