from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATE = ROOT / "apps/web/app/templates/campaign/index.html"

TRUST_CUE = (
    '<p class="ff-help ff-mutedStrong ff-mt-3 ff-mb-0 ff-faqTrustCue">'
    'Secure checkout • Email receipt • Sponsor follow-up by email.'
    '</p>'
)

pattern = re.compile(
    r'(<div class="ff-row ff-wrap ff-gap-2(?: [^"]*)? ff-faqEndcap__actions"[^>]*>)',
    re.S,
)

def backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = path.with_suffix(path.suffix + f".bak.{stamp}")
    bak.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return bak

text = TEMPLATE.read_text(encoding="utf-8")

if "ff-faqTrustCue" in text:
    print(f"✔ already present: {TEMPLATE}")
    raise SystemExit(0)

updated, count = pattern.subn(TRUST_CUE + r'\1', text, count=1)
if count == 0:
    raise SystemExit("❌ Could not find ff-faqEndcap__actions block for trust-cue injection")

bak = backup(TEMPLATE)
TEMPLATE.write_text(updated, encoding="utf-8")

print("== FAQ TRUST CUE FIX ==")
print(f"✅ patched template: {TEMPLATE}")
print(f"🛟 backup: {bak}")
print("   • injected ff-faqTrustCue above ff-faqEndcap__actions")
