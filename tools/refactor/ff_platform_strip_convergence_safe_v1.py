from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"

CSS = ROOT / "apps/web/app/static/css/platform-pages.css"

FOUNDER_PARTIAL = ROOT / "apps/web/app/templates/platform/partials/_founder_demo_flow_strip.html"
DASH_PARTIAL = ROOT / "apps/web/app/templates/platform/partials/_dashboard_operator_premium_strip.html"

FOUNDER_TARGETS = [
    ROOT / "apps/web/app/templates/platform/pages/home.html",
    ROOT / "apps/web/app/templates/platform/pages/pricing.html",
    ROOT / "apps/web/app/templates/platform/pages/demo.html",
    ROOT / "apps/web/app/templates/platform/pages/onboarding.html",
]

DASH_TARGET = ROOT / "apps/web/app/templates/platform/pages/dashboard.html"

FOUNDER_INCLUDE = '{% include "platform/partials/_founder_demo_flow_strip.html" %}'
DASH_INCLUDE = '{% include "platform/partials/_dashboard_operator_premium_strip.html" %}'

FOUNDER_MARKER = "FF_PLATFORM_FOUNDER_DEMO_FLOW_V1"
DASH_MARKER = "FF_PLATFORM_DASHBOARD_OPERATOR_PREMIUM_V1"

def backup(path: Path) -> None:
    if path.exists():
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        shutil.copy2(path, path.with_name(f"{path.name}.{ts}.bak"))

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def ensure_single_include(path: Path, include_line: str) -> None:
    text = read(path)
    count = text.count(include_line)

    if count > 1:
        lines = text.splitlines()
        seen = 0
        new_lines = []
        for line in lines:
            if line.strip() == include_line:
                seen += 1
                if seen > 1:
                    continue
            new_lines.append(line)
        backup(path)
        write(path, "\n".join(new_lines) + ("\n" if text.endswith("\n") else ""))
        print(f"deduped include: {path}")
        return

    if count == 1:
        print(f"skip include already present: {path}")
        return

    backup(path)
    if "</main>" in text:
        text = text.replace("</main>", f"\n  {include_line}\n</main>", 1)
    elif "{% endblock %}" in text:
        text = text.replace("{% endblock %}", f"\n{include_line}\n{% endblock %}", 1)
    else:
        print(f"MISS no insertion anchor: {path}")
        return

    write(path, text)
    print(f"inserted include: {path}")

css_text = read(CSS)

founder_count = css_text.count(FOUNDER_MARKER)
dash_count = css_text.count(DASH_MARKER)

print("== SAFE STRIP CONVERGENCE ==")

print(f"founder_css_marker_count: {founder_count}")
print(f"dashboard_css_marker_count: {dash_count}")

if founder_count > 1 or dash_count > 1:
    raise SystemExit("Refusing to modify CSS because duplicate markers already exist. Clean CSS first.")

for target in FOUNDER_TARGETS:
    ensure_single_include(target, FOUNDER_INCLUDE)

ensure_single_include(DASH_TARGET, DASH_INCLUDE)

print("done.")
