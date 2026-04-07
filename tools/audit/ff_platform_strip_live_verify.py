from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROUTES = [
    "/platform/",
    "/platform/pricing",
    "/platform/demo",
    "/platform/onboarding",
    "/platform/dashboard",
]

CHECKS = {
    "/platform/": {
        "founder_title": 1,
        "operator_title": 0,
    },
    "/platform/pricing": {
        "founder_title": 1,
        "operator_title": 0,
    },
    "/platform/demo": {
        "founder_title": 1,
        "operator_title": 0,
    },
    "/platform/onboarding": {
        "founder_title": 1,
        "operator_title": 0,
    },
    "/platform/dashboard": {
        "founder_title": 0,
        "operator_title": 1,
    },
}

FOUNDER_TEXT = "Walk founders from interest to launch in one clean sequence"
OPERATOR_TEXT = "Run fundraising, sponsors, and launch operations from one cleaner command surface"

print("== FF PLATFORM STRIP LIVE VERIFY ==")
print()

failed = False

for route in ROUTES:
    url = f"http://127.0.0.1:5000{route}"
    try:
        html = subprocess.check_output(["curl", "-s", url], text=True)
    except Exception as exc:
        print(f"{route}: ERROR fetching route: {exc}")
        failed = True
        continue

    founder_count = html.count(FOUNDER_TEXT)
    operator_count = html.count(OPERATOR_TEXT)

    exp_founder = CHECKS[route]["founder_title"]
    exp_operator = CHECKS[route]["operator_title"]

    ok = founder_count == exp_founder and operator_count == exp_operator
    status = "OK" if ok else "MISMATCH"

    print(f"{route}: {status}")
    print(f"  founder_title_count:  {founder_count} (expected {exp_founder})")
    print(f"  operator_title_count: {operator_count} (expected {exp_operator})")

    if not ok:
        failed = True

print()
print("RESULT:", "CLEAN" if not failed else "REVIEW NEEDED")
sys.exit(1 if failed else 0)
