from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
SHELL = ROOT / "apps/web/app/templates/platform/shells/marketing_base.html"

if not SHELL.exists():
    raise SystemExit(f"Missing file: {SHELL}")

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
shutil.copy2(SHELL, SHELL.with_name(f"{SHELL.name}.{timestamp}.bak"))

src = SHELL.read_text(encoding="utf-8")

old = """{% set _platform_logo = (
  platform_logo_url
  |default(_cfg.get('FF_PLATFORM_LOGO_URL'), true)
  |default(_cfg.get('FF_LOGO_URL'), true)
  |default('', true)
)|string|trim %}
"""

new = """{% set _platform_logo = (
  platform_logo_url
  |default(_cfg.get('FF_PLATFORM_LOGO_URL'), true)
  |default(_cfg.get('FF_LOGO_URL'), true)
  |default(url_for('static', filename='images/futurefunded-mark.svg'), true)
)|string|trim %}
"""

if old not in src:
    raise SystemExit("Could not find _platform_logo block in marketing_base.html")

src = src.replace(old, new, 1)
SHELL.write_text(src, encoding="utf-8")

print("== FF PLATFORM DEFAULT LOGO ASSET V1 ==")
print("patched:", SHELL)
print("done.")
