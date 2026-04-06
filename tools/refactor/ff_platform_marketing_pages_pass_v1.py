from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"

HOME = ROOT / "apps/web/app/templates/platform/pages/home.html"
PRICING = ROOT / "apps/web/app/templates/platform/pages/pricing.html"
DEMO = ROOT / "apps/web/app/templates/platform/pages/demo.html"

FILES = [HOME, PRICING, DEMO]


def backup(path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    bak = path.with_name(f"{path.name}.bak.{ts}")
    shutil.copy2(path, bak)
    return bak


def write_text(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def replace_once(text: str, old: str, new: str, *, label: str) -> tuple[str, bool]:
    if old in text:
        return text.replace(old, new, 1), True
    if new in text:
        return text, False
    raise RuntimeError(f"could not find expected block for: {label}")


def patch_home(path: Path) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8")
    original = text
    notes: list[str] = []

    replacements = [
        (
            'hero.get("secondary_cta_label", "Open dashboard")',
            'hero.get("secondary_cta_label", "View live example")',
            "hero secondary CTA label",
        ),
        (
            'hero.get("secondary_cta_href", "/platform/dashboard")',
            'hero.get("secondary_cta_href", "/c/spring-fundraiser")',
            "hero secondary CTA href",
        ),
        (
            'id="platformLaunchStatusTitle">Operator readout</h2>',
            'id="platformLaunchStatusTitle">Launch snapshot</h2>',
            "launch snapshot heading",
        ),
        (
            'next_move.get("secondary_cta_label", "Manage platform")',
            'next_move.get("secondary_cta_label", "View pricing")',
            "next move secondary CTA label",
        ),
        (
            'next_move.get("secondary_cta_href", "/platform/dashboard")',
            'next_move.get("secondary_cta_href", "/platform/pricing")',
            "next move secondary CTA href",
        ),
    ]

    for old, new, label in replacements:
        text, changed = replace_once(text, old, new, label=label)
        if changed:
            notes.append(f"updated {label}")

    changed_any = text != original
    if changed_any:
        write_text(path, text)
    return changed_any, notes


def patch_pricing(path: Path) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8")
    original = text
    notes: list[str] = []

    old_block = """</section>

    <div class="ff-card ff-glass ff-pad ff-mt-3" aria-labelledby="platformPricingCloseTitle">
      <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
        <div class="ff-minw-0">
          <p class="ff-kicker ff-m-0">Ready to launch?</p>
          <h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformPricingCloseTitle">Get your program live this week.</h2>
          <p class="ff-help ff-muted ff-mt-2 ff-mb-0">
            Start with founder pricing, launch the public fundraiser first, then expand into sponsor packages and optional support plans as the program grows.
          </p>
        </div>
        <div class="ff-row ff-wrap ff-gap-2">
          <a class="ff-btn ff-btn--primary ff-btn--pill" href="/platform/onboarding">Start guided launch</a>
          <a class="ff-btn ff-btn--secondary ff-btn--pill" href="/platform/demo">Open guided demo</a>
        </div>
      </div>
    </div>
{% endblock %}"""

    new_block = """</section>

<section class="ff-section" aria-labelledby="platformPricingCloseTitle">
  <div class="ff-container">
    <div class="ff-card ff-glass ff-pad" aria-labelledby="platformPricingCloseTitle">
      <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
        <div class="ff-minw-0">
          <p class="ff-kicker ff-m-0">Ready to launch?</p>
          <h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformPricingCloseTitle">Get your program live this week.</h2>
          <p class="ff-help ff-muted ff-mt-2 ff-mb-0">
            Start with founder pricing, launch the public fundraiser first, then expand into sponsor packages and optional support plans as the program grows.
          </p>
        </div>
        <div class="ff-row ff-wrap ff-gap-2">
          <a class="ff-btn ff-btn--primary ff-btn--pill" href="/platform/onboarding">Start guided launch</a>
          <a class="ff-btn ff-btn--secondary ff-btn--pill" href="/platform/demo">Open guided demo</a>
        </div>
      </div>
    </div>
  </div>
</section>
{% endblock %}"""

    text, changed = replace_once(text, old_block, new_block, label="pricing close section wrap")
    if changed:
        notes.append("wrapped pricing close card in section/container")

    changed_any = text != original
    if changed_any:
        write_text(path, text)
    return changed_any, notes


def patch_demo(path: Path) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8")
    original = text
    notes: list[str] = []

    old_block = """</section>

    <div class="ff-card ff-glass ff-pad ff-mt-3" aria-labelledby="platformDemoFounderCloseTitle">
      <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
        <div class="ff-minw-0">
          <p class="ff-kicker ff-m-0">Founder close</p>
          <h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformDemoFounderCloseTitle">Show this flow, then ask for the launch.</h2>
          <p class="ff-help ff-muted ff-mt-2 ff-mb-0">
            The simplest founder close is: this is your live page, this is your setup flow, this is your dashboard, and this is the pricing to get started.
          </p>
        </div>
        <div class="ff-row ff-wrap ff-gap-2">
          <a class="ff-btn ff-btn--primary ff-btn--pill" href="/platform/onboarding">Start guided launch</a>
          <a class="ff-btn ff-btn--secondary ff-btn--pill" href="/platform/pricing">Review pricing</a>
        </div>
      </div>
    </div>
{% endblock %}"""

    new_block = """</section>

<section class="ff-section" aria-labelledby="platformDemoFounderCloseTitle">
  <div class="ff-container">
    <div class="ff-card ff-glass ff-pad" aria-labelledby="platformDemoFounderCloseTitle">
      <div class="ff-row ff-row--between ff-ais ff-wrap ff-gap-2">
        <div class="ff-minw-0">
          <p class="ff-kicker ff-m-0">Founder close</p>
          <h2 class="ff-h2 ff-mt-2 ff-mb-0" id="platformDemoFounderCloseTitle">Show this flow, then ask for the launch.</h2>
          <p class="ff-help ff-muted ff-mt-2 ff-mb-0">
            The simplest founder close is: this is your live page, this is your setup flow, this is your dashboard, and this is the pricing to get started.
          </p>
        </div>
        <div class="ff-row ff-wrap ff-gap-2">
          <a class="ff-btn ff-btn--primary ff-btn--pill" href="/platform/onboarding">Start guided launch</a>
          <a class="ff-btn ff-btn--secondary ff-btn--pill" href="/platform/pricing">Review pricing</a>
        </div>
      </div>
    </div>
  </div>
</section>
{% endblock %}"""

    text, changed = replace_once(text, old_block, new_block, label="demo founder close section wrap")
    if changed:
        notes.append("wrapped demo founder close card in section/container")

    changed_any = text != original
    if changed_any:
        write_text(path, text)
    return changed_any, notes


def main() -> int:
    print("== FF PLATFORM MARKETING PAGES PASS V1 ==")

    backups = []
    for path in FILES:
        if not path.exists():
            raise FileNotFoundError(path)
        backups.append((path, backup(path)))

    changed_any = False

    changed, notes = patch_home(HOME)
    changed_any = changed_any or changed
    print(f"patched: {HOME}")
    for note in notes:
        print(f"  - {note}")

    changed, notes = patch_pricing(PRICING)
    changed_any = changed_any or changed
    print(f"patched: {PRICING}")
    for note in notes:
        print(f"  - {note}")

    changed, notes = patch_demo(DEMO)
    changed_any = changed_any or changed
    print(f"patched: {DEMO}")
    for note in notes:
        print(f"  - {note}")

    print("\\nbackups:")
    for path, bak in backups:
        print(f"  - {path.name} -> {bak.name}")

    print("\\nresult:")
    print("  - changed" if changed_any else "  - no-op (already aligned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
