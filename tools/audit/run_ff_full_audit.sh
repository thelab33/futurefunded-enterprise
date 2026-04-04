#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://127.0.0.1:5000/c/connect-atx-elite}"

printf '\n== RUN REPO ARCHITECTURE AUDIT ==\n'
python3 tools/audit/ff_repo_architecture_audit.py

printf '\n== RUN CAMPAIGN RUNTIME AUDIT ==\n'
python3 tools/audit/ff_campaign_runtime_audit.py "$URL"

printf '\n== RUN CSS ORIGIN AUDIT ==\n'
python3 tools/audit/ff_css_origin_audit.py \
  ".ff-checkoutShell" \
  ".ff-modal" \
  ".ff-floatingDonate" \
  ".ff-sponsorTierGrid" \
  ".ff-sheet__close" \
  ".ff-themeToggle" \
  ".ff-storyCopy" \
  ".ff-topbar__capsuleInner"

printf '\n== ARTIFACTS ==\n'
ls -lah tools/.artifacts | sed -n '1,120p'
