#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT/apps/web" || exit 1

# Pull payment-related vars from repo-root .env safely.
eval "$(
python3 - <<'PY'
from pathlib import Path

env_path = Path('../../.env').resolve()
wanted = {
    'STRIPE_MODE',
    'STRIPE_SECRET_KEY',
    'STRIPE_PUBLISHABLE_KEY',
    'PAYPAL_MODE',
    'PAYPAL_CLIENT_ID',
    'FF_ALLOW_TEST_PAYMENTS_DEMO',
}

if env_path.exists():
    for raw in env_path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k in wanted and v:
            safe = v.replace("'", "'\"'\"'")
            print(f"export {k}='{safe}'")

# force local prod-ish demo mode with test keys if not already set
print("export FF_ALLOW_TEST_PAYMENTS_DEMO='1'")
PY
)"

export APP_ENV=production
export FLASK_ENV=production
export PUBLIC_BASE_URL="https://getfuturefunded.com"
export CANONICAL_BASE_URL="https://getfuturefunded.com"
export FF_PUBLIC_BASE_URL="https://getfuturefunded.com"
export PREFERRED_URL_SCHEME="https"
export PYTHONPATH="../..:../../apps/web"

echo "== FF LOCAL PRODISH RUN =="
echo "APP_ENV=$APP_ENV"
echo "FLASK_ENV=$FLASK_ENV"
echo "PUBLIC_BASE_URL=$PUBLIC_BASE_URL"
echo "CANONICAL_BASE_URL=$CANONICAL_BASE_URL"
echo "FF_PUBLIC_BASE_URL=$FF_PUBLIC_BASE_URL"
echo "PYTHONPATH=$PYTHONPATH"

python3 - <<'PY'
import os
for k in [
    "STRIPE_MODE",
    "STRIPE_SECRET_KEY",
    "STRIPE_PUBLISHABLE_KEY",
    "PAYPAL_MODE",
    "PAYPAL_CLIENT_ID",
    "FF_ALLOW_TEST_PAYMENTS_DEMO",
]:
    v = os.getenv(k, "")
    print(f"{k}:", "set" if v else "missing", (v[:12] + "...") if v else "")
PY

exec ../../.venv/bin/flask --app wsgi:app run --host 127.0.0.1 --port 5000
