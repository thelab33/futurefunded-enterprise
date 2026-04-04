#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://127.0.0.1:5000/c/spring-fundraiser}"
TMP_HTML="$(mktemp)"
trap 'rm -f "$TMP_HTML"' EXIT

curl -fsSL "$URL" -o "$TMP_HTML"

if [[ "${FF_FORCE_PRODISH:-0}" == "1" ]]; then
  PRODISH=1
elif [[ "$URL" =~ 127\.0\.0\.1|localhost|\[::1\] ]]; then
  PRODISH=0
else
  PRODISH=1
fi

FAIL=0

say_no() {
  local pattern="$1"
  local label="$2"
  if rg -n "$pattern" "$TMP_HTML" >/dev/null; then
    echo "❌ $label"
    rg -n "$pattern" "$TMP_HTML" | sed -n '1,20p'
    FAIL=1
  else
    echo "✅ $label"
  fi
}

say_yes() {
  local pattern="$1"
  local label="$2"
  if rg -n "$pattern" "$TMP_HTML" >/dev/null; then
    echo "✅ $label"
    rg -n "$pattern" "$TMP_HTML" | sed -n '1,10p'
  else
    echo "❌ $label"
    FAIL=1
  fi
}

echo "== FF CAMPAIGN TRUTH AUDIT =="
echo "URL: $URL"
echo "prodish: $PRODISH"
echo "force_prodish: ${FF_FORCE_PRODISH:-0}"

echo
echo "== BODY CONFIG SNAPSHOT =="
rg -n 'data-ff-data-mode|data-ff-totals-verified|data-ff-canonical|data-ff-share-url|data-ff-return-url' "$TMP_HTML" \
  | sed -n '1,40p' || true

echo
echo "== REQUIRED ASSETS =="
say_yes 'css/ff\.css' 'campaign should load ff.css'
say_yes 'js/ff-app\.js' 'campaign should load ff-app.js'

echo
echo "== FORBIDDEN PLATFORM ASSETS =="
say_no 'platform-pages\.css' 'campaign should not load platform-pages.css'
say_no 'platform-app\.js' 'campaign should not load platform-app.js'

if [[ "$PRODISH" -eq 1 ]]; then
  echo
  echo "== PROD TRUTH CHECKS =="
  say_no 'data-ff-data-mode="demo"' 'prod fundraiser should not render demo mode'
  say_no 'data-ff-share-url="https?://(127\.0\.0\.1|localhost|\[::1\])' 'prod share URL should not point to localhost'
  say_no 'data-ff-return-url="https?://(127\.0\.0\.1|localhost|\[::1\])' 'prod return URL should not point to localhost'
  say_no 'data-ff-canonical="http://' 'prod canonical should not be http://'
  say_yes 'data-ff-data-mode="live"|data-ff-data-mode="preview"' 'prod fundraiser should render a non-demo mode'
fi

echo
if [[ "$FAIL" -eq 0 ]]; then
  echo "✅ PASS — campaign page cleared truth audit"
else
  echo "❌ FAIL — campaign page still has launch truth issues"
  exit 1
fi
