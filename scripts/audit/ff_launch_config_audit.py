from pathlib import Path
import os
import re

env_candidates = [Path(".env"), Path("apps/web/.env"), Path(".env.local")]
pairs = {}

for p in env_candidates:
    if p.exists():
        for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            s = line.strip()
            if not s or s.startswith("#") or "=" not in s:
                continue
            k, v = s.split("=", 1)
            pairs.setdefault(k.strip(), v.strip())

checks = {
    "FLASK_ENV": ["production"],
    "APP_ENV": ["production"],
    "STRIPE_PUBLISHABLE_KEY": None,
    "FF_STRIPE_PUBLISHABLE_KEY": None,
    "STRIPE_SECRET_KEY": None,
    "PAYPAL_CLIENT_ID": None,
    "PAYPAL_CLIENT_SECRET": None,
    "PUBLIC_BASE_URL": None,
    "CANONICAL_BASE_URL": None,
    "SECRET_KEY": None,
}

print("== CONFIG AUDIT ==")
for key, wanted in checks.items():
    val = os.environ.get(key, pairs.get(key))
    if not val:
        print(f"MISS  {key}")
    elif wanted and val not in wanted:
        print(f"WARN  {key}={val!r} expected one of {wanted}")
    else:
        masked = val if "PUBLIC" in key or "BASE_URL" in key or key.endswith("_ENV") else ("*" * min(8, len(val)))
        print(f"OK    {key}={masked}")

print("\n== URL SANITY ==")
for key in ("PUBLIC_BASE_URL", "CANONICAL_BASE_URL"):
    val = os.environ.get(key, pairs.get(key, ""))
    if val and not re.match(r"^https?://", val):
        print(f"WARN  {key} should start with http:// or https://")
    elif val:
        print(f"OK    {key}")
