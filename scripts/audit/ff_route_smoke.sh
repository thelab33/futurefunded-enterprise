#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${FF_BASE_URL:-http://127.0.0.1:5000}"
CAMPAIGN_PATH="${FF_CAMPAIGN_PATH:-/c/spring-fundraiser}"

mkdir -p /tmp/ff-smoke

declare -a URLS=(
  "/"
  "/platform/onboarding"
  "/platform/dashboard"
  "$CAMPAIGN_PATH"
)

for path in "${URLS[@]}"; do
  slug="$(echo "$path" | sed 's#[^a-zA-Z0-9]#_#g')"
  out="/tmp/ff-smoke/${slug}.html"
  echo
  echo "== FETCH $path =="
  curl -fsS "${BASE_URL}${path}" > "$out"
  wc -c "$out"
  rg -n "FutureFunded|Donate|Sponsor|Dashboard|Onboarding|Create org|campaign|membership|goal|raised" "$out" | sed -n '1,20p' || true
done

echo
echo "✅ route smoke complete"
