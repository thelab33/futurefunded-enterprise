from __future__ import annotations

from pathlib import Path

ROOT = Path.home() / "futurefunded-enterprise"
ROUTE = ROOT / "apps/web/app/routes/campaign.py"

NEEDLES = [
    'ctx["campaign_url"] = campaign_url',
    'ctx["canonical"] = campaign_url',
    'ctx["share_url"] = campaign_url',
    'ctx["_share_url_resolved"] = campaign_url',
    'ctx["_stripe_return"] = campaign_url',
]

INSERT_AFTER = 'ctx["campaign_url"] = campaign_url'
INSERT_BLOCK = """    # Public-surface source of truth for the Jinja contract.
    # The campaign template reads these early for canonical/meta/schema/return wiring.
    ctx["ff_public_base_url"] = base
    ctx["canonical_url"] = campaign_url
    ctx["stripe_return_url"] = campaign_url
"""

def main() -> None:
    if not ROUTE.exists():
        raise SystemExit(f"Missing route file: {ROUTE}")

    text = ROUTE.read_text(encoding="utf-8")

    if 'ctx["ff_public_base_url"] = base' in text and 'ctx["canonical_url"] = campaign_url' in text:
        raise SystemExit("Route surface contract already wired.")

    missing = [n for n in NEEDLES if n not in text]
    if missing:
        raise SystemExit(
            "Expected route lines missing. Refusing to patch blindly:\\n- " +
            "\\n- ".join(missing)
        )

    anchor = INSERT_AFTER
    replacement = anchor + "\n" + INSERT_BLOCK.rstrip()

    if replacement in text:
        raise SystemExit("Insert block already present next to campaign_url anchor.")

    updated = text.replace(anchor, replacement, 1)

    backup = ROUTE.with_name(ROUTE.name + ".bak-route-surface-contract-v2")
    if not backup.exists():
        backup.write_text(text, encoding="utf-8")

    ROUTE.write_text(updated, encoding="utf-8")

    print(f"✅ patched {ROUTE}")
    print(f"🛟 backup: {backup}")

if __name__ == "__main__":
    main()
