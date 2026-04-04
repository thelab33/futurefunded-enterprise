#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://127.0.0.1:5000/c/spring-fundraiser}"
TMP_HTML="$(mktemp)"
trap 'rm -f "$TMP_HTML"' EXIT

curl -fsSL "$URL" -o "$TMP_HTML"

if [[ "$URL" =~ 127\.0\.0\.1|localhost|\[::1\] ]]; then
  PRODISH=0
else
  PRODISH=1
fi

FAIL=0

check_no() {
  local pattern="$1"
  local label="$2"
  if rg -n "$pattern" "$TMP_HTML" >/dev/null; then
    echo "❌ $label"
    rg -n "$pattern" "$TMP_HTML" | sed -n '1,40p'
    FAIL=1
  else
    echo "✅ $label"
  fi
}

echo "== FF LAUNCH TRUTH GATE =="
echo "URL: $URL"
echo "prodish: $PRODISH"

echo
echo "== ASSET OWNERSHIP =="
check_no 'platform-pages\.css' 'campaign page should not load platform-pages.css'
check_no 'platform-app\.js' 'campaign page should not load platform-app.js'

if [[ "$PRODISH" -eq 1 ]]; then
  echo
  echo "== PROD TRUTH =="
  check_no 'data-ff-data-mode="demo"' 'prod fundraiser should not render demo mode'
  check_no 'data-ff-share-url="https?://(127\.0\.0\.1|localhost|\[::1\])' 'prod fundraiser share URL should not point to localhost'
  check_no 'data-ff-return-url="https?://(127\.0\.0\.1|localhost|\[::1\])' 'prod fundraiser return URL should not point to localhost'
  check_no 'data-ff-canonical="http://' 'prod fundraiser canonical should not be http://'
fi

echo
if [[ "$FAIL" -eq 0 ]]; then
  echo "✅ PASS — fundraiser page cleared launch truth gate"
else
  echo "❌ FAIL — fundraiser page still has truth/ownership leaks"
  exit 1
fi
