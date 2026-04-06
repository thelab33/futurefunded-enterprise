from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
FF = ROOT / "apps/web/app/static/css/ff.css"
ABOVE = ROOT / "apps/web/app/static/css/ff-above-main-premium.css"

START = "/* FF_AUTHORITY_PROMOTED_FROM_ABOVE_V4_START */"
END = "/* FF_AUTHORITY_PROMOTED_FROM_ABOVE_V4_END */"

PROMOTE_SELECTORS = [
    ".ff-backtotop",
    ".ff-callout",
    ".ff-checkoutCard",
    ".ff-checkoutLayout",
    ".ff-display",
    ".ff-faqEndcap",
    ".ff-faqEndcap__header",
    ".ff-faqList",
    ".ff-footerShell",
    ".ff-chip",
    ".ff-chip--impact",
    ".ff-disclosure",
    ".ff-disclosure__panel",
    ".ff-disclosure__sum",
    ".ff-donationSuccessMount",
]

def backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = path.with_name(path.name + f".bak.{stamp}")
    shutil.copy2(path, bak)
    return bak

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")

def extract_rule_blocks(css: str, selectors: list[str]) -> tuple[list[str], str]:
    kept_css = css
    moved_blocks: list[str] = []

    for selector in selectors:
        pattern = re.compile(
            rf'(^|\n)([^\n{{}}]*body\[data-ff-page="fundraiser"\][^{{}}]*{re.escape(selector)}[^{{}}]*)\s*\{{',
            re.M
        )

        while True:
            m = pattern.search(kept_css)
            if not m:
                break

            start = m.start(2)
            brace_open = kept_css.find("{", m.end(2) - 1)
            if brace_open == -1:
                break

            depth = 0
            i = brace_open
            end = None
            while i < len(kept_css):
                ch = kept_css[i]
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break
                i += 1

            if end is None:
                break

            block = kept_css[start:end].strip()
            moved_blocks.append(block)
            kept_css = (kept_css[:start] + "\n" + kept_css[end:]).strip() + "\n"

    return moved_blocks, kept_css

def unscope_block(block: str) -> str:
    block = re.sub(
        r'body\[data-ff-page="fundraiser"\]\s+',
        '',
        block
    )
    block = re.sub(r'\n{3,}', '\n\n', block)
    return block.strip()

def main() -> None:
    if not FF.exists():
        raise SystemExit(f"❌ missing: {FF}")
    if not ABOVE.exists():
        raise SystemExit(f"❌ missing: {ABOVE}")

    ff_orig = read(FF)
    above_orig = read(ABOVE)

    moved_blocks, above_new = extract_rule_blocks(above_orig, PROMOTE_SELECTORS)

    if not moved_blocks:
        print("== FF CSS AUTHORITY CONSOLIDATION V4 ==")
        print("✔ no eligible blocks found to promote")
        raise SystemExit(0)

    promoted = []
    seen = set()
    for block in moved_blocks:
        uns = unscope_block(block)
        if uns not in seen:
            promoted.append(uns)
            seen.add(uns)

    authority_block = (
        START + "\n" +
        "/* Promoted from ff-above-main-premium.css into ff.css so fundraiser authority lives in one place. */\n\n" +
        "\n\n".join(promoted).strip() + "\n" +
        END
    )

    if START in ff_orig and END in ff_orig:
        ff_new = re.sub(
            re.escape(START) + r".*?" + re.escape(END),
            authority_block,
            ff_orig,
            flags=re.S
        )
    else:
        ff_new = ff_orig.rstrip() + "\n\n" + authority_block + "\n"

    ff_bak = backup(FF)
    above_bak = backup(ABOVE)

    write(FF, ff_new)
    write(ABOVE, above_new)

    print("== FF CSS AUTHORITY CONSOLIDATION V4 ==")
    print(f"✅ promoted blocks : {len(promoted)}")
    print(f"✅ patched ff.css  : {FF}")
    print(f"✅ patched shim    : {ABOVE}")
    print(f"🛟 ff backup       : {ff_bak}")
    print(f"🛟 shim backup     : {above_bak}")
    print("promoted selectors:")
    for s in PROMOTE_SELECTORS:
        print(f" - {s}")

if __name__ == "__main__":
    main()
