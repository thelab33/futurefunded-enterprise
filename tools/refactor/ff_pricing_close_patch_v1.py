from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
PRICING = ROOT / "apps/web/app/templates/platform/pages/pricing.html"
DEMO = ROOT / "apps/web/app/templates/platform/pages/demo.html"

for path in (PRICING, DEMO):
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
for path in (PRICING, DEMO):
    shutil.copy2(path, path.with_name(f"{path.name}.{timestamp}.bak"))

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old in text:
        print(f"changed: {label}")
        return text.replace(old, new, 1)
    print(f"MISS: {label}")
    return text

pricing_text = PRICING.read_text(encoding="utf-8")
demo_text = DEMO.read_text(encoding="utf-8")

pricing_replacements = [
    (
        "First five programs get founder pricing.",
        "Get founder pricing and launch this week.",
        "pricing founder offer title",
    ),
    (
        "Start with founder pricing, get live fast, and grow into sponsor packages, recurring support, and a cleaner operator workflow without rebuilding your system later.",
        "Start with founder pricing, launch the public fundraiser this week, and upgrade into sponsor packages and recurring support when the program is ready.",
        "pricing founder offer body",
    ),
    (
        "Easy to explain. Easy to buy.",
        "Easy to explain. Easy to say yes.",
        "pricing why it converts title",
    ),
    (
        "The strongest pricing story is simple: launch the public fundraiser first, prove the sponsor-ready surface, then expand into recurring support and broader platform value as the program grows.",
        "The strongest pricing story is simple: launch the public fundraiser first, prove the value with a live buyer-facing example, then upgrade into sponsor packages and recurring support as the program grows.",
        "pricing why it converts body",
    ),
    (
        "The fastest way to get a premium public fundraiser live and start selling the system.",
        "Best for getting the public fundraiser live fast and proving the offer with a real buyer-facing example.",
        "pricing starter positioning",
    ),
    (
        "The best upgrade path when you want sponsor lanes, recurring support, and a stronger operator story.",
        "Best long-term value when you want sponsor packages, recurring support, and a stronger operator story.",
        "pricing growth positioning",
    ),
    (
        "The path for institutions that want the platform to feel like their own branded operating system.",
        "Best for institutions that want procurement-ready presentation and a fuller branded operating system.",
        "pricing white-label positioning",
    ),
    (
        "Get your program live this week.",
        "Start with Starter. Upgrade when the program is ready.",
        "pricing close title",
    ),
    (
        "Start with founder pricing, launch the public fundraiser first, then expand into sponsor packages and optional support plans as the program grows.",
        "Most programs should start on Starter, prove the fundraiser, then upgrade to Growth when sponsor packages and recurring support start driving revenue.",
        "pricing close body",
    ),
    (
        "Claim founder setup",
        "Start founder setup",
        "pricing founder CTA",
    ),
    (
        "View live demo",
        "Open guided demo",
        "pricing demo CTA",
    ),
    (
        "Start with Starter",
        "Choose Starter",
        "pricing starter button",
    ),
]

for old, new, label in pricing_replacements:
    pricing_text = replace_once(pricing_text, old, new, label)

demo_replacements = [
    (
        "This guided demo shows the public fundraiser, the onboarding flow, the operator dashboard, and the founder-ready pricing model as one connected revenue system.",
        "Use this exact sequence in calls: public fundraiser, onboarding, operator dashboard, pricing, then ask for the launch.",
        "demo hero body",
    ),
    (
        "Use this as your guided sales flow.",
        "Use this as your launch-closing sales flow.",
        "demo hero side title",
    ),
    (
        "Start with the fundraiser, move through onboarding, show the operator dashboard, then close on pricing. It gives buyers a full picture without making the product feel complicated.",
        "Start with the fundraiser, move through onboarding, show the operator dashboard, then close on pricing. This gives buyers the full picture and makes the launch ask feel natural.",
        "demo hero side body",
    ),
    (
        "Before FutureFunded: scattered fundraising, weak sponsor presentation, no clear operator story. After FutureFunded: one branded launch surface with cleaner trust, revenue lanes, and expansion room.",
        "Before FutureFunded: scattered fundraising, weak sponsor presentation, and no clean operator story. After FutureFunded: one branded launch surface with trust, revenue lanes, and room to grow.",
        "demo founder angle body",
    ),
    (
        "Start guided launch with FutureFunded.",
        "Show this flow, then ask for the launch this week.",
        "demo close title",
    ),
    (
        "Use this page in DMs, calls, and founder outreach to show the full product in one clean sequence — then move directly into launch.",
        "Use this page to walk a buyer through the public page, launch flow, operator dashboard, and pricing — then ask for the launch while momentum is high.",
        "demo close body",
    ),
    (
        "Launch your program",
        "Start guided launch",
        "demo primary close CTA",
    ),
    (
        "View live example",
        "Open live fundraiser",
        "demo secondary close CTA",
    ),
    (
        "The cleanest founder close is: this is your live page, this is your setup flow, this is your operator workspace, and this is the pricing to get started today.",
        "The cleanest founder close is: here is your public fundraiser, here is your launch flow, here is your operator workspace, and here is the pricing to get live this week.",
        "demo founder close body",
    ),
    (
        "Review pricing",
        "Open pricing",
        "demo footer CTA",
    ),
]

for old, new, label in demo_replacements:
    demo_text = replace_once(demo_text, old, new, label)

PRICING.write_text(pricing_text, encoding="utf-8")
DEMO.write_text(demo_text, encoding="utf-8")

print("done.")
