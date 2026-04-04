from pathlib import Path
import re
import json

ROOT = Path(".").resolve()

SEARCH_DIRS = [
    ROOT / "apps/web/app/templates",
    ROOT / "apps/web/templates",
    ROOT / "apps/web/src/routes",
]

EXTS = {".html", ".jinja", ".j2", ".jinja2", ".svelte"}

def collect_files():
    out = []
    for base in SEARCH_DIRS:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix.lower() in EXTS:
                out.append(p)
    return sorted(set(out))

def classify(path: Path, text: str):
    s = str(path).lower()
    t = text.lower()
    if any(x in s for x in ["dashboard", "admin"]):
        return "dashboard"
    if "onboarding" in s:
        return "onboarding"
    if any(x in s for x in ["campaign", "fundraiser"]) or "/c/" in s or "donate" in s:
        return "campaign"
    if any(x in s for x in ["index", "home"]):
        return "home"
    if "launch your first organization" in t or "futurefunded flagship" in t:
        return "home"
    if "launch outcome" in t or "create org + campaign" in t:
        return "onboarding"
    if "command center" in t or "membership plans" in t:
        return "dashboard"
    if "support the season" in t or "donate now" in t or "become a sponsor" in t:
        return "campaign"
    return "other"

def count(pattern, text):
    return len(re.findall(pattern, text, flags=re.I | re.M))

def metrics(text: str):
    return {
        "sections": count(r"<section\b", text),
        "forms": count(r"<form\b", text),
        "dialogs": count(r'role=["\\\']dialog["\\\']|data-ff-[a-z0-9_-]*(sheet|modal|drawer)', text),
        "cards": count(r'ff-card|ff-glass|ff-panel|ff-tile', text),
        "pills": count(r'ff-pill|ff-chip|ff-badge|ff-tag', text),
        "buttons": count(r'ff-btn|ff-button|type=["\\\']submit["\\\']', text),
        "inputs": count(r"<input\b|<select\b|<textarea\b", text),
        "links": count(r"<a\b", text),
        "data_hooks": count(r'data-ff-[a-z0-9_-]+', text),
        "ids": count(r'\sid=["\\\'][^"\\\']+["\\\']', text),
        "headings": count(r"<h[1-6]\b", text),
        "money_strings": count(r"\$|donate|goal|raised|sponsor|membership", text),
    }

def weight(m):
    return (
        m["sections"] * 8
        + m["forms"] * 14
        + m["dialogs"] * 10
        + m["cards"] * 2
        + m["pills"] * 1
        + m["buttons"] * 2
        + m["inputs"] * 4
        + m["data_hooks"] * 1
        + m["headings"] * 2
        + m["money_strings"] * 1
    )

files = collect_files()
if not files:
    raise SystemExit("No template/route files found in expected locations.")

rows = []
for p in files:
    text = p.read_text(encoding="utf-8", errors="ignore")
    kind = classify(p, text)
    m = metrics(text)
    row = {
        "file": str(p.relative_to(ROOT)),
        "kind": kind,
        **m,
        "weight": weight(m),
    }
    rows.append(row)

rows.sort(key=lambda r: (-r["weight"], r["file"]))

out = ROOT / "docs/audits/pages-unification-audit.md"
lines = ["# FutureFunded pages unification audit", ""]
lines.append("| kind | weight | sections | forms | dialogs | cards | pills | buttons | inputs | file |")
lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")
for r in rows:
    lines.append(
        f"| {r['kind']} | {r['weight']} | {r['sections']} | {r['forms']} | {r['dialogs']} | {r['cards']} | {r['pills']} | {r['buttons']} | {r['inputs']} | `{r['file']}` |"
    )

lines += ["", "## Heaviest files", ""]
for r in rows[:12]:
    lines.append(f"- **{r['kind']}** `{r['file']}` → weight {r['weight']}")

by_kind = {}
for r in rows:
    by_kind.setdefault(r["kind"], []).append(r)

lines += ["", "## Summary by page type", ""]
for kind, items in sorted(by_kind.items()):
    avg = round(sum(x["weight"] for x in items) / len(items), 1)
    lines.append(f"- **{kind}**: {len(items)} file(s), avg weight {avg}")

campaigns = [r for r in rows if r["kind"] == "campaign"]
if campaigns:
    lines += ["", "## Campaign verdict", ""]
    top = campaigns[0]
    lines.append(
        f"- Heaviest campaign file: `{top['file']}` → weight {top['weight']}, sections={top['sections']}, forms={top['forms']}, dialogs={top['dialogs']}, cards={top['cards']}, pills={top['pills']}, buttons={top['buttons']}, inputs={top['inputs']}"
    )
    if top["weight"] > 120:
        lines.append("- Verdict: campaign is likely carrying too many responsibilities in one template.")
    elif top["weight"] > 85:
        lines.append("- Verdict: campaign is moderately heavy and likely needs consolidation.")
    else:
        lines.append("- Verdict: campaign complexity looks controlled.")

out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"✅ wrote {out}")
