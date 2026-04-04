from __future__ import annotations

from pathlib import Path

ROOT = Path.home() / "futurefunded-enterprise"
ROUTE = ROOT / "apps/web/app/routes/campaign.py"
TEMPLATE = ROOT / "apps/web/app/templates/campaign/index.html"

ROUTE_NEEDLE = 'return configured or "http://127.0.0.1:5000"'
ROUTE_REPLACEMENT = 'return configured or "https://getfuturefunded.com"'

TEMPLATE_NEEDLE = '<div class="ff-checkoutCard__head"><h3 class="ff-label ff-m-0" id="checkoutSummaryTitle">Summary</h3><span class="ff-pill ff-pill--soft">Live preview</span></div>'
TEMPLATE_REPLACEMENT = '<div class="ff-checkoutCard__head"><h3 class="ff-label ff-m-0" id="checkoutSummaryTitle">Summary</h3><span class="ff-pill ff-pill--soft">{% if ff_data_mode == "live" %}Live{% else %}Preview{% endif %}</span></div>'


def patch_file(path: Path, needle: str, replacement: str, backup_suffix: str) -> None:
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")

    text = path.read_text(encoding="utf-8")
    if needle not in text:
        raise SystemExit(f"Needle not found in {path}: {needle}")

    backup = path.with_name(path.name + backup_suffix)
    if not backup.exists():
        backup.write_text(text, encoding="utf-8")

    updated = text.replace(needle, replacement, 1)
    path.write_text(updated, encoding="utf-8")

    print(f"✅ patched {path}")
    print(f"🛟 backup: {backup}")


def main() -> None:
    patch_file(ROUTE, ROUTE_NEEDLE, ROUTE_REPLACEMENT, ".bak-truth-lock-v1")
    patch_file(TEMPLATE, TEMPLATE_NEEDLE, TEMPLATE_REPLACEMENT, ".bak-truth-lock-v1")


if __name__ == "__main__":
    main()
