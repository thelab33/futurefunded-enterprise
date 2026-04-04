from __future__ import annotations

from pathlib import Path

ROOT = Path.home() / "futurefunded-enterprise"
ROUTE = ROOT / "apps/web/app/routes/campaign.py"

OLD_BLOCK = """    ctx["campaign_url"] = campaign_url
    ctx["canonical"] = campaign_url
    ctx["share_url"] = campaign_url
    ctx["_share_url_resolved"] = campaign_url
    ctx["_stripe_return"] = campaign_url
"""

NEW_BLOCK = """    ctx["campaign_url"] = campaign_url
    # Public-surface source of truth for the Jinja contract.
    # The campaign template reads ff_public_base_url / canonical_url /
    # stripe_return_url early, before later hardening blocks.
    ctx["ff_public_base_url"] = base
    ctx["canonical_url"] = campaign_url
    ctx["stripe_return_url"] = campaign_url

    # Keep legacy/current keys populated too.
    ctx["canonical"] = campaign_url
    ctx["share_url"] = campaign_url
    ctx["_share_url_resolved"] = campaign_url
    ctx["_stripe_return"] = campaign_url
"""

def main() -> None:
    if not ROUTE.exists():
        raise SystemExit(f"Missing route file: {ROUTE}")

    text = ROUTE.read_text(encoding="utf-8")

    if 'ctx["canonical_url"] = campaign_url' in text and 'ctx["ff_public_base_url"] = base' in text:
        raise SystemExit("Route surface contract appears to already be wired.")

    if OLD_BLOCK not in text:
        raise SystemExit("Expected route block not found. Refusing to patch blindly.")

    backup = ROUTE.with_name(ROUTE.name + ".bak-route-surface-contract-v1")
    if not backup.exists():
        backup.write_text(text, encoding="utf-8")

    updated = text.replace(OLD_BLOCK, NEW_BLOCK, 1)
    ROUTE.write_text(updated, encoding="utf-8")

    print(f"✅ patched {ROUTE}")
    print(f"🛟 backup: {backup}")

if __name__ == "__main__":
    main()
