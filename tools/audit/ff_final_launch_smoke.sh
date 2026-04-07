#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/futurefunded-enterprise}"
cd "$ROOT"

OUT="reports/final-smoke"
mkdir -p "$OUT"

TEMPLATE="apps/web/app/templates/campaign/index.html"
JS="apps/web/app/static/js/ff-app.js"

printf '== 00) STATIC FILE CHECKS ==\n' | tee "$OUT/00_static_checks.txt"
ls -l "$TEMPLATE" "$JS" | tee -a "$OUT/00_static_checks.txt"

printf '\n== 01) NO ONBOARDING DRIFT ==\n' | tee "$OUT/01_no_onboarding_drift.txt"
rg -n \
  'openOnboard|closeOnboard|onboardModal|onboardForm|onboardNext|onboardPrev|onboardFinish|onboardCopy|onboardEmail|onboardSummary|onboardStatus|onboardResult|stepPill|stepPanel|ff-onboarding|data-ff-open-onboard|data-ff-close-onboard' \
  "$TEMPLATE" "$JS" | tee -a "$OUT/01_no_onboarding_drift.txt" || true

printf '\n== 02) JS SYNTAX ==\n' | tee "$OUT/02_js_syntax.txt"
node --check "$JS" | tee -a "$OUT/02_js_syntax.txt"

printf '\n== 03) TEMPLATE CONTRACT COUNTS ==\n' | tee "$OUT/03_template_contract_counts.txt"
python3 - <<'PY' | tee -a "$OUT/03_template_contract_counts.txt"
from pathlib import Path
p = Path("apps/web/app/templates/campaign/index.html")
text = p.read_text(encoding="utf-8")

checks = {
    "ffConfig_count": text.count('id="ffConfig"'),
    "ffSelectors_count": text.count('id="ffSelectors"'),
    "checkout_section_count": text.count('id="checkout"'),
    "sponsor_form_count": text.count('id="sponsorForm"'),
    "hero_title_count": text.count('id="heroTitle"'),
    "topbar_count": text.count('id="ffTopbar"'),
    "footer_count": text.count('id="footer"'),
}
for k, v in checks.items():
    print(f"{k}: {v}")
PY

printf '\n== 04) CORE HOOK PRESENCE ==\n' | tee "$OUT/04_core_hook_presence.txt"
rg -n \
  'openCheckout|closeCheckout|openSponsor|closeSponsor|openVideo|closeVideo|themeToggle|openDrawer|closeDrawer|floatingDonate|backToTop|renderPayPalButtons|mountStripeForCurrentAmount|submitSponsorForm|handleCheckoutSubmit' \
  "$JS" | tee -a "$OUT/04_core_hook_presence.txt" || true

printf '\n== 05) CORE TEMPLATE MARKERS ==\n' | tee "$OUT/05_template_markers.txt"
rg -n \
  'id="ffTopbar"|id="heroTitle"|id="checkout"|id="sponsorsTitle"|id="storyTitle"|id="trustFaqTitle"|id="footer"|id="donationForm"|id="sponsorForm"' \
  "$TEMPLATE" | tee -a "$OUT/05_template_markers.txt" || true

printf '\n== 06) LOCAL ROUTE SMOKE (if server is running on :5000) ==\n' | tee "$OUT/06_route_smoke.txt"
python3 - <<'PY' | tee -a "$OUT/06_route_smoke.txt"
import urllib.request
import urllib.error

base = "http://127.0.0.1:5000"
routes = [
    "/platform/",
    "/platform/onboarding",
    "/platform/dashboard",
    "/platform/pricing",
    "/platform/demo",
    "/c/spring-fundraiser",
]

for route in routes:
    url = base + route
    try:
        with urllib.request.urlopen(url, timeout=4) as resp:
            html = resp.read(3000).decode("utf-8", "ignore")
            print(f"{route} -> {resp.status}")
            markers = []
            for token in ["ffTopbar", "heroTitle", "checkoutTitle", "platform", "onboarding", "dashboard"]:
                if token in html:
                    markers.append(token)
            print("  markers:", ", ".join(markers) if markers else "(none in preview)")
    except Exception as e:
        print(f"{route} -> SKIP ({e.__class__.__name__})")
PY

printf '\n== 07) DONE ==\n'
printf 'Open these reports:\n'
printf '  %s\n' \
  "$OUT/01_no_onboarding_drift.txt" \
  "$OUT/02_js_syntax.txt" \
  "$OUT/03_template_contract_counts.txt" \
  "$OUT/06_route_smoke.txt"
