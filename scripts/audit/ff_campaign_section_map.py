from pathlib import Path
import re
from html import unescape

p = Path("apps/web/app/templates/campaign/index.html")
if not p.exists():
    raise SystemExit(f"Missing file: {p}")

text = p.read_text(encoding="utf-8", errors="ignore")
out = Path("docs/audits/campaign-section-map.md")

section_pat = re.compile(r'(?is)<section\b([^>]*)>(.*?)</section>')
attr_pat = re.compile(r'([:@a-zA-Z0-9_-]+)\s*=\s*"([^"]*)"')
heading_pat = re.compile(r'(?is)<h[1-3]\b[^>]*>(.*?)</h[1-3]>')
strip_tags = re.compile(r'(?is)<[^>]+>')

def clean(s: str) -> str:
    s = unescape(strip_tags.sub(" ", s))
    s = re.sub(r"\s+", " ", s).strip()
    return s

def count(pat: str, s: str) -> int:
    return len(re.findall(pat, s, flags=re.I | re.M))

rows = []

for i, m in enumerate(section_pat.finditer(text), start=1):
    attr_blob = m.group(1)
    body = m.group(2)

    attrs = dict(attr_pat.findall(attr_blob))
    sid = attrs.get("id", "")
    klass = attrs.get("class", "")

    heading_m = heading_pat.search(body)
    heading = clean(heading_m.group(1))[:120] if heading_m else ""

    row = {
        "n": i,
        "id": sid,
        "class": klass[:120],
        "heading": heading,
        "buttons": count(r'ff-btn|ff-button|<button\b', body),
        "inputs": count(r'<input\b|<select\b|<textarea\b', body),
        "forms": count(r'<form\b', body),
        "dialogs": count(r'role="dialog"|data-ff-[a-z0-9_-]*(sheet|modal|drawer)', body),
        "pills": count(r'ff-pill|ff-chip|ff-badge|ff-tag', body),
        "cards": count(r'ff-card|ff-glass|ff-panel|ff-tile', body),
        "links": count(r'<a\b', body),
    }

    row["weight"] = (
        row["buttons"] * 2
        + row["inputs"] * 4
        + row["forms"] * 14
        + row["dialogs"] * 10
        + row["pills"] * 1
        + row["cards"] * 2
        + row["links"] * 1
    )

    rows.append(row)

rows.sort(key=lambda r: (-r["weight"], r["n"]))

lines = [
    "# Campaign section map",
    "",
    f"- File: `{p}`",
    "",
    "| # | weight | buttons | inputs | forms | dialogs | pills | cards | links | id | heading |",
    "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|",
]

for r in rows:
    lines.append(
        f"| {r['n']} | {r['weight']} | {r['buttons']} | {r['inputs']} | {r['forms']} | {r['dialogs']} | {r['pills']} | {r['cards']} | {r['links']} | `{r['id']}` | {r['heading']} |"
    )

lines += ["", "## Top heaviest sections", ""]

for r in rows[:12]:
    lines.append(
        f"- Section {r['n']} `{r['id']}` — weight {r['weight']} — heading: {r['heading'] or '(no heading)'}"
    )

out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"✅ wrote {out}")
