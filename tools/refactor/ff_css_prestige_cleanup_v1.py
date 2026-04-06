from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/ff.css"

PRESTIGE_START = "/* FF_PRESTIGE_ENHANCEMENTS_START */"
PRESTIGE_END = "/* FF_PRESTIGE_ENHANCEMENTS_END */"

def backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = path.with_name(path.name + f".bak.{stamp}")
    shutil.copy2(path, bak)
    return bak

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")

def clean_header(text: str) -> str:
    text = re.sub(
        r"/\* ==========================================================================\s*FutureFunded — ff\.css.*?@layer ff\.tokens, ff\.base, ff\.layout, ff\.components, ff\.sections, ff\.overlays, ff\.utilities;\s*",
        """/* ==========================================================================
   FutureFunded — ff.css
   Version: v6.0.0 "Unified Fundraiser Authority"
   --------------------------------------------------------------------------
   Scope:
   - canonical fundraiser authority file
   - mobile-first, accessible, reduced-motion safe
   - premium glass / flagship fundraising presentation
   - single-source ownership for the campaign surface
   ========================================================================== */

@layer ff.tokens, ff.base, ff.layout, ff.components, ff.sections, ff.overlays, ff.utilities;

""",
        text,
        count=1,
        flags=re.S,
    )
    return text

def remove_embedded_shim_artifacts(text: str) -> str:
    patterns = [
        r"/\* ==========================================================================\s*FutureFunded — ff-above-main-premium\.css.*?\*/",
        r"/\* FF_CSS_AUTHORITY_CONSOLIDATION_V2 merged into later canonical rule:.*?\*/",
        r"/\* FF_CSS_AUTHORITY_CONSOLIDATION_V3 moved to ff\.css authority block:.*?\*/",
    ]
    for pat in patterns:
        text = re.sub(pat, "", text, flags=re.S)
    return text

def extract_prestige_region(text: str) -> tuple[str, str]:
    start_match = re.search(r"/\* FF_FUNDRAISER_AUTHORITY_V3_START \*/", text)
    end_match = re.search(r"/\* FF_FUNDRAISER_AUTHORITY_V3_END \*/", text)

    if not start_match or not end_match or end_match.start() <= start_match.start():
        return "", text

    block = text[start_match.end():end_match.start()].strip()
    text = text[:start_match.start()].rstrip() + "\n"
    return block, text

def normalize_prestige_block(block: str) -> str:
    if not block:
        return ""

    block = block.strip()

    replacements = [
        (r"\n{3,}", "\n\n"),
        (r"[ \t]+\n", "\n"),
    ]
    for pat, repl in replacements:
        block = re.sub(pat, repl, block)

    header = f"""{PRESTIGE_START}
/* Premium fundraiser enhancements and final flagship refinements.
   These rules remain intentionally scoped to the fundraiser surface
   while living inside the single ff.css authority file. */

"""
    footer = f"\n{PRESTIGE_END}\n"

    return header + block.strip() + footer

def insert_prestige_before_utilities(text: str, prestige: str) -> str:
    if not prestige:
        return text

    marker = "/* ==========================================================================\n   UTILITIES + RESPONSIVE\n   ========================================================================== */"
    idx = text.find(marker)
    if idx == -1:
        return text.rstrip() + "\n\n" + prestige + "\n"

    return text[:idx].rstrip() + "\n\n" + prestige + "\n\n" + text[idx:]

def tidy_whitespace(text: str) -> str:
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    return text.rstrip() + "\n"

def main() -> None:
    if not CSS.exists():
        raise SystemExit(f"❌ missing css file: {CSS}")

    orig = read(CSS)

    cleaned = orig
    cleaned = clean_header(cleaned)
    cleaned = remove_embedded_shim_artifacts(cleaned)

    prestige_block, cleaned = extract_prestige_region(cleaned)
    prestige_block = normalize_prestige_block(prestige_block)
    cleaned = insert_prestige_before_utilities(cleaned, prestige_block)
    cleaned = tidy_whitespace(cleaned)

    if cleaned == orig:
        print("== FF CSS PRESTIGE CLEANUP V1 ==")
        print("✔ no changes needed")
        raise SystemExit(0)

    bak = backup(CSS)
    write(CSS, cleaned)

    print("== FF CSS PRESTIGE CLEANUP V1 ==")
    print(f"✅ patched css : {CSS}")
    print(f"🛟 backup      : {bak}")
    print("done:")
    print(" - unified header")
    print(" - removed embedded shim artifact comments")
    print(" - extracted legacy bottom authority block")
    print(" - reinserted as a single premium enhancements region")
    print(" - normalized whitespace")
    print(f"marker start   : {PRESTIGE_START}")
    print(f"marker end     : {PRESTIGE_END}")

if __name__ == "__main__":
    main()
