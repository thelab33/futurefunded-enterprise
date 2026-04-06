from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re
import shutil

ROOT = Path.home() / "futurefunded-enterprise"
CSS = ROOT / "apps/web/app/static/css/ff.css"

START = "/* FF_PRESTIGE_ENHANCEMENTS_START */"
END = "/* FF_PRESTIGE_ENHANCEMENTS_END */"

def backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = path.with_name(path.name + f".bak.{stamp}")
    shutil.copy2(path, bak)
    return bak

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")

def clean_block(block: str) -> str:
    block = re.sub(r"/\*\s*FF_[A-Z0-9_]+_START\s*\*/", "", block)
    block = re.sub(r"/\*\s*FF_[A-Z0-9_]+_END\s*\*/", "", block)
    block = re.sub(r"/\*\s*Canonical fundraiser component ownership migrated from ff-above-main-premium\.css\s*\*/", "", block)
    block = re.sub(r"\n{3,}", "\n\n", block)
    return block.strip()

def classify_snippet(snippet: str) -> str:
    s = snippet

    if any(x in s for x in [
        ".ff-topbar", ".ff-topbarGoal", ".ff-themeToggle", ".ff-topbarBrand",
        ".ff-topbar__capsule", ".ff-topbar__mainRow", ".ff-topbar__brandCluster",
        ".ff-topbar__desktopActions", ".ff-topbar__rightCluster"
    ]):
        return "topbar"

    if any(x in s for x in [
        ".ff-hero", "#heroTitle", "#heroAccentLine", ".ff-heroAccent",
        ".ff-heroName", ".ff-heroPanel", ".ff-heroLine", ".ff-heroHeader",
        ".ff-heroFooter", ".ff-heroSnapshotGrid", ".ff-storySupportGrid"
    ]):
        return "hero"

    if any(x in s for x in [
        ".ff-teamCard", ".ff-teamStat", ".ff-teamGrid"
    ]):
        return "teams"

    if any(x in s for x in [
        ".ff-sponsor", ".ff-sponsorGhost", ".ff-sponsorWallRail", ".ff-sponsorEmptyState"
    ]):
        return "sponsors"

    if any(x in s for x in [
        ".ff-faq", ".ff-disclosure", ".ff-proofMini", ".ff-mutedStrong",
        ".ff-help.ff-muted", ".ff-heroTrustCue", ".ff-faqTrustCue"
    ]):
        return "trust_faq"

    if any(x in s for x in [
        ".ff-footer", ".ff-backtotop"
    ]):
        return "footer"

    if "html[data-theme=\"dark\"]" in s:
        return "dark_mode"

    if "@media" in s:
        return "responsive"

    return "misc"

def split_into_snippets(block: str) -> list[str]:
    snippets = []
    lines = block.splitlines()
    current = []

    def flush():
        nonlocal current
        text = "\n".join(current).strip()
        if text:
            snippets.append(text)
        current = []

    for line in lines:
        if line.strip().startswith("/*") and current:
            flush()
            current.append(line)
        else:
            current.append(line)

    flush()
    return [s for s in snippets if s.strip()]

def group_snippets(snippets: list[str]) -> dict[str, list[str]]:
    buckets = {
        "topbar": [],
        "hero": [],
        "teams": [],
        "sponsors": [],
        "trust_faq": [],
        "footer": [],
        "dark_mode": [],
        "responsive": [],
        "misc": [],
    }
    for snippet in snippets:
        buckets[classify_snippet(snippet)].append(snippet.strip())
    return buckets

def build_prestige_block(old_block: str) -> str:
    cleaned = clean_block(old_block)
    snippets = split_into_snippets(cleaned)
    buckets = group_snippets(snippets)

    parts = [START]
    parts.append("/* Premium fundraiser enhancements and flagship refinements.")
    parts.append("   Organized for maintainability inside the single ff.css authority file. */")
    parts.append("")

    sections = [
        ("TOPBAR", "topbar"),
        ("HERO", "hero"),
        ("TEAMS", "teams"),
        ("SPONSORS", "sponsors"),
        ("TRUST / FAQ", "trust_faq"),
        ("FOOTER", "footer"),
        ("DARK MODE", "dark_mode"),
        ("RESPONSIVE PREMIUM ADJUSTMENTS", "responsive"),
        ("MISC", "misc"),
    ]

    for label, key in sections:
        if not buckets[key]:
            continue
        parts.append(f"/* --------------------------------------------------------------------------")
        parts.append(f"   {label}")
        parts.append(f"   -------------------------------------------------------------------------- */")
        parts.append("")
        parts.append("\n\n".join(buckets[key]).strip())
        parts.append("")

    parts.append(END)
    return "\n".join(parts).strip() + "\n"

def main() -> None:
    if not CSS.exists():
        raise SystemExit(f"❌ missing css file: {CSS}")

    orig = read(CSS)

    m = re.search(re.escape(START) + r"(.*?)" + re.escape(END), orig, flags=re.S)
    if not m:
        raise SystemExit("❌ prestige enhancement region not found")

    old_inner = m.group(1)
    new_block = build_prestige_block(old_inner)

    updated = re.sub(
        re.escape(START) + r".*?" + re.escape(END),
        new_block,
        orig,
        flags=re.S,
    )
    updated = re.sub(r"\n{4,}", "\n\n\n", updated).rstrip() + "\n"

    if updated == orig:
        print("== FF CSS PRESTIGE CLEANUP V2 ==")
        print("✔ no changes needed")
        raise SystemExit(0)

    bak = backup(CSS)
    write(CSS, updated)

    print("== FF CSS PRESTIGE CLEANUP V2 ==")
    print(f"✅ patched css : {CSS}")
    print(f"🛟 backup      : {bak}")
    print("done:")
    print(" - reorganized prestige region into labeled groups")
    print(" - removed old patch-wave wrapper comments inside prestige block")
    print(" - kept single authority structure intact")
    print(f"marker start   : {START}")
    print(f"marker end     : {END}")

if __name__ == "__main__":
    main()
