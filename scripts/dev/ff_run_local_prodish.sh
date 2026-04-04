#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT/apps/web" || exit 1

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

exec ../../.venv/bin/flask --app wsgi:app run --host 127.0.0.1 --port 5000
