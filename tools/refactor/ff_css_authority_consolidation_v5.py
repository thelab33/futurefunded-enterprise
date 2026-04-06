from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
FF = ROOT / "apps/web/app/static/css/ff.css"
ABOVE = ROOT / "apps/web/app/static/css/ff-above-main-premium.css"

START = "/* FF_AUTHORITY_PROMOTED_FROM_ABOVE_V5_START */"
END = "/* FF_AUTHORITY_PROMOTED_FROM_ABOVE_V5_END */"

PROMOTE_SELECTORS = [
    ".ff-donate-btn",
    ".ff-iconbtn",
    ".ff-meter",
    ".ff-meter__progress",
    ".ff-nav--pill",
]

DEDUPE_SELECTORS = [
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
    ".ff-donate-btn",
    ".ff-iconbtn",
    ".ff-meter",
    ".ff-meter__progress",
    ".ff-nav--pill",
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

def extract_blocks(css: str, selectors: list[str]) -> tuple[list[str], str]:
    working = css
    moved: list[str] = []

    for selector in selectors:
        pattern = re.compile(
            rf'(^|\n)([^\n{{}}]*body\[data-ff-page="fundraiser"\][^{{}}]*{re.escape(selector)}[^{{}}]*)\s*\{{',
            re.M
        )

        while True:
            m = pattern.search(working)
            if not m:
                break

            start = m.start(2)
            brace_open = working.find("{", m.end(2) - 1)
            if brace_open == -1:
                break

            depth = 0
            i = brace_open
            end = None
            while i < len(working):
                ch = working[i]
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

            block = working[start:end].strip()
            moved.append(block)
            working = (working[:start] + "\n" + working[end:]).strip() + "\n"

    return moved, working

def unscope(block: str) -> str:
    block = re.sub(r'html\[data-theme="dark"\]\s+body\[data-ff-page="fundraiser"\]\s+', 'html[data-theme="dark"] ', block)
    block = re.sub(r'body\[data-ff-page="fundraiser"\]\s+', '', block)
    block = re.sub(r'\n{3,}', '\n\n', block)
    return block.strip()

def remove_older_duplicate_blocks(ff_css: str, selectors: list[str], protected_start: str, protected_end: str) -> str:
    protected = None
    if protected_start in ff_css and protected_end in ff_css:
        m = re.search(re.escape(protected_start) + r".*?" + re.escape(protected_end), ff_css, flags=re.S)
        if m:
            protected = (m.start(), m.end())

    for selector in selectors:
        pattern = re.compile(
            rf'(^|\n)([^\n{{}}]*{re.escape(selector)}[^{{}}]*)\s*\{{',
            re.M
        )

        matches = list(pattern.finditer(ff_css))
        if len(matches) <= 1:
            continue

        removable_ranges = []
        for m in matches[:-1]:
            start = m.start(2)
            if protected and protected[0] <= start <= protected[1]:
                continue

            brace_open = ff_css.find("{", m.end(2) - 1)
            if brace_open == -1:
                continue

            depth = 0
            i = brace_open
            end = None
            while i < len(ff_css):
                ch = ff_css[i]
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break
                i += 1

            if end is not None:
                removable_ranges.append((start, end))

        for start, end in sorted(removable_ranges, reverse=True):
            ff_css = ff_css[:start] + "\n" + ff_css[end:]

    ff_css = re.sub(r'\n{3,}', '\n\n', ff_css).rstrip() + "\n"
    return ff_css

def main() -> None:
    if not FF.exists() or not ABOVE.exists():
        raise SystemExit("❌ missing ff.css or ff-above-main-premium.css")

    ff_orig = read(FF)
    above_orig = read(ABOVE)

    moved, above_new = extract_blocks(above_orig, PROMOTE_SELECTORS)

    promoted = []
    seen = set()
    for block in moved:
        cleaned = unscope(block)
        if cleaned not in seen:
            promoted.append(cleaned)
            seen.add(cleaned)

    ff_work = ff_orig
    if promoted:
        authority_block = (
            START + "\n" +
            "/* Additional canonical fundraiser selectors promoted from ff-above-main-premium.css */\n\n" +
            "\n\n".join(promoted).strip() + "\n" +
            END
        )

        if START in ff_work and END in ff_work:
            ff_work = re.sub(
                re.escape(START) + r".*?" + re.escape(END),
                authority_block,
                ff_work,
                flags=re.S
            )
        else:
            ff_work = ff_work.rstrip() + "\n\n" + authority_block + "\n"

    ff_new = remove_older_duplicate_blocks(ff_work, DEDUPE_SELECTORS, START, END)

    ff_bak = backup(FF)
    above_bak = backup(ABOVE)

    write(FF, ff_new)
    write(ABOVE, above_new)

    print("== FF CSS AUTHORITY CONSOLIDATION V5 ==")
    print(f"✅ promoted blocks : {len(promoted)}")
    print(f"✅ dedupe targets  : {len(DEDUPE_SELECTORS)}")
    print(f"✅ patched ff.css  : {FF}")
    print(f"✅ patched shim    : {ABOVE}")
    print(f"🛟 ff backup       : {ff_bak}")
    print(f"🛟 shim backup     : {above_bak}")
    print("promoted selectors:")
    for s in PROMOTE_SELECTORS:
        print(f" - {s}")

if __name__ == "__main__":
    main()
