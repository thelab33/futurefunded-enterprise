from __future__ import annotations

from pathlib import Path
import os
import sys

ROOT = Path.home() / "futurefunded-enterprise"
WEB_ROOT = ROOT / "apps" / "web"
sys.path.insert(0, str(WEB_ROOT))

issues = []
warnings = []

try:
    from app import create_app
except Exception as exc:
    raise SystemExit(f"could not import app.create_app: {exc}")

app = create_app()

def val(key, default=None):
    return app.config.get(key, default)

env_app = (os.getenv("APP_ENV") or os.getenv("ENV") or os.getenv("FLASK_ENV") or "").strip().lower()
public_base = (os.getenv("FF_PUBLIC_BASE_URL") or os.getenv("PUBLIC_BASE_URL") or "").strip()
canonical_base = (os.getenv("CANONICAL_BASE_URL") or "").strip()

stripe_pk = (os.getenv("STRIPE_PUBLISHABLE_KEY") or os.getenv("STRIPE_PUBLIC_KEY") or "").strip()
stripe_sk = (os.getenv("STRIPE_SECRET_KEY") or "").strip()
paypal_mode = (os.getenv("PAYPAL_MODE") or "").strip().lower()
allow_test_demo = (os.getenv("FF_ALLOW_TEST_PAYMENTS_DEMO") or "0").strip()

if val("DEBUG") is True:
    issues.append("DEBUG must be False in production")
if val("TESTING") is True:
    issues.append("TESTING must be False in production")
if not val("SECRET_KEY"):
    issues.append("SECRET_KEY missing/blank")
if env_app != "production":
    issues.append(f"APP_ENV/ENV/FLASK_ENV should resolve to production, got: {env_app or 'blank'}")
if not public_base.startswith("https://"):
    issues.append(f"FF_PUBLIC_BASE_URL/PUBLIC_BASE_URL must be https, got: {public_base or 'blank'}")
if canonical_base and not canonical_base.startswith("https://"):
    issues.append(f"CANONICAL_BASE_URL must be https when set, got: {canonical_base}")

if val("SESSION_COOKIE_SECURE") is not True:
    issues.append("SESSION_COOKIE_SECURE should be True")
if str(val("SESSION_COOKIE_SAMESITE", "")).lower() not in {"lax", "strict"}:
    issues.append(f"SESSION_COOKIE_SAMESITE should be Lax or Strict, got: {val('SESSION_COOKIE_SAMESITE')}")
if val("SESSION_COOKIE_HTTPONLY") is not True:
    issues.append("SESSION_COOKIE_HTTPONLY should be True")
if val("PREFERRED_URL_SCHEME") != "https":
    issues.append(f"PREFERRED_URL_SCHEME should be https, got: {val('PREFERRED_URL_SCHEME')}")
if val("TEMPLATES_AUTO_RELOAD") is True:
    warnings.append("TEMPLATES_AUTO_RELOAD is True; that should usually be off in production")

if stripe_pk.startswith("pk_test_") or stripe_sk.startswith("sk_test_"):
    if allow_test_demo != "1":
        issues.append("test Stripe keys detected without FF_ALLOW_TEST_PAYMENTS_DEMO=1")
    else:
        warnings.append("test Stripe keys allowed because FF_ALLOW_TEST_PAYMENTS_DEMO=1")
if stripe_pk and stripe_sk:
    if stripe_pk.startswith("pk_live_") != stripe_sk.startswith("sk_live_"):
        issues.append("Stripe publishable/secret keys do not match live/test mode")

if paypal_mode not in {"", "disabled", "live", "sandbox"}:
    warnings.append(f"unexpected PAYPAL_MODE value: {paypal_mode}")

print("== RUNTIME CONFIG AUDIT ==")
print(f"ENV={env_app}")
print(f"DEBUG={val('DEBUG')}")
print(f"TESTING={val('TESTING')}")
print(f"PREFERRED_URL_SCHEME={val('PREFERRED_URL_SCHEME')}")
print(f"SESSION_COOKIE_SECURE={val('SESSION_COOKIE_SECURE')}")
print(f"SESSION_COOKIE_HTTPONLY={val('SESSION_COOKIE_HTTPONLY')}")
print(f"SESSION_COOKIE_SAMESITE={val('SESSION_COOKIE_SAMESITE')}")
print(f"TEMPLATES_AUTO_RELOAD={val('TEMPLATES_AUTO_RELOAD')}")
print(f"FF_PUBLIC_BASE_URL={public_base or 'blank'}")
print(f"CANONICAL_BASE_URL={canonical_base or 'blank'}")
print(f"FF_ALLOW_TEST_PAYMENTS_DEMO={allow_test_demo}")

print("\n== ISSUES ==")
if issues:
    for item in issues:
        print(f"ERROR: {item}")
else:
    print("none")

print("\n== WARNINGS ==")
if warnings:
    for item in warnings:
        print(f"WARN: {item}")
else:
    print("none")

if issues:
    sys.exit(1)
