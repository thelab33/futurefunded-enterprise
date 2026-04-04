from __future__ import annotations
from pathlib import Path
import re

ROOT = Path.home() / "futurefunded-enterprise"
TEMPLATE = ROOT / "apps/web/app/templates/campaign/index.html"

pattern = re.compile(
    r"""\{% set _public_base_raw = \(
\s*ff_public_base_url\|default\('', true\)
\s*or _cfg\.get\('FF_PUBLIC_BASE_URL'\)
\s*or _cfg\.get\('PUBLIC_BASE_URL'\)
\s*or \(request\.url_root if request is defined else ''\)
\)\|string\|trim %\}""",
    re.X,
)

replacement = """{% set _public_base_raw = (
  ff_public_base_url|default('', true)
  or _cfg.get('FF_PUBLIC_BASE_URL')
  or _cfg.get('PUBLIC_BASE_URL')
  or _cfg.get('CANONICAL_BASE_URL')
  or 'https://getfuturefunded.com'
)|string|trim %}"""

def main() -> None:
    if not TEMPLATE.exists():
        raise SystemExit(f"Missing template: {TEMPLATE}")

    text = TEMPLATE.read_text(encoding="utf-8")

    if "or _cfg.get('CANONICAL_BASE_URL')" in text and "or 'https://getfuturefunded.com'" in text:
        print("ℹ️ public-base truth lock already present")
        return

    if not pattern.search(text):
        raise SystemExit("Could not find _public_base_raw block to patch.")

    backup = TEMPLATE.with_name(TEMPLATE.name + ".bak-public-url-truth-lock-v1")
    if not backup.exists():
        backup.write_text(text, encoding="utf-8")

    updated = pattern.sub(replacement, text, count=1)
    TEMPLATE.write_text(updated, encoding="utf-8")

    print(f"✅ patched {TEMPLATE}")
    print(f"🛟 backup: {backup}")

if __name__ == "__main__":
    main()
