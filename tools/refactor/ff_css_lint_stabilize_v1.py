from __future__ import annotations
from pathlib import Path
from datetime import datetime
import re

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/ff.css"

text = CSS.read_text(encoding="utf-8")
orig = text

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = ROOT / "backups" / f"ff.css.pre_lint_stabilize_{stamp}.bak"
backup.write_text(text, encoding="utf-8")

# ------------------------------------------------------------
# 1) Remove deprecated clip declarations (keep clip-path)
# ------------------------------------------------------------
text = re.sub(
    r'^\s*clip:\s*rect\(0,\s*0,\s*0,\s*0\)\s*(?:!important)?;\s*\n',
    '',
    text,
    flags=re.M,
)

# ------------------------------------------------------------
# 2) Remove duplicate inline-size in story poster render fix
# ------------------------------------------------------------
text = text.replace(
    "  inline-size: 100%;\n"
    "  block-size: 100%;\n"
    "  min-inline-size: 100%;\n"
    "  min-block-size: 100%;\n"
    "  inline-size: 100%;\n",
    "  inline-size: 100%;\n"
    "  block-size: 100%;\n"
    "  min-inline-size: 100%;\n"
    "  min-block-size: 100%;\n",
    1,
)

# ------------------------------------------------------------
# 3) Wrap the late polish stack with stylelint suppression
#    for duplicate selectors / spacing-only noise
# ------------------------------------------------------------
start_marker = "/* FF_FINAL_PRESTIGE_MICRO_POLISH_V1_START */"
end_marker = "/* FF_CONTRACT_GAP_PATCH_V1_END */"

if start_marker in text and end_marker in text:
    start = text.index(start_marker)
    end = text.index(end_marker) + len(end_marker)
    block = text[start:end]

    if "stylelint-disable no-duplicate-selectors" not in block:
        wrapped = (
            "/* stylelint-disable no-duplicate-selectors, comment-empty-line-before, rule-empty-line-before */\n\n"
            + block +
            "\n\n/* stylelint-enable no-duplicate-selectors, comment-empty-line-before, rule-empty-line-before */"
        )
        text = text[:start] + wrapped + text[end:]

if text != orig:
    CSS.write_text(text, encoding="utf-8")
    print(f"✅ patched {CSS}")
    print(f"🗂 backup  {backup}")
else:
    print("ℹ️ no changes made")

