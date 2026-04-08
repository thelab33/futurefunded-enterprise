from __future__ import annotations

import re
import sys
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path.home() / "futurefunded-enterprise"
DEFAULT_TARGET = ROOT / "apps/web/app/templates/campaign/index.html"

VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

OPEN_JINJA = {
    "if", "for", "block", "macro", "with", "call",
    "filter", "autoescape", "raw", "trans",
}
MID_JINJA = {"else", "elif"}
CLOSE_JINJA = {
    "endif", "endfor", "endblock", "endmacro", "endwith",
    "endcall", "endfilter", "endautoescape", "endraw", "endtrans",
}

TOKEN_RE = re.compile(
    r"({#.*?#}|{%.*?%}|{{.*?}}|<!--.*?-->|<!DOCTYPE.*?>|</?[^>]+>)",
    re.S | re.I,
)


def backup_file(path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_name(f"{path.name}.{ts}.bak")
    shutil.copy2(path, backup)
    return backup


def normalize(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    # only split fully minified adjacent tags
    text = re.sub(r">\s*<", ">\n<", text)
    # keep Jinja statements/comments on their own lines
    text = re.sub(r"\s*({%.*?%}|{#.*?#})\s*", r"\n\1\n", text, flags=re.S)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def jinja_word(line: str) -> str | None:
    s = line.strip()
    if not (s.startswith("{%") and s.endswith("%}")):
        return None
    inner = s[2:-2].strip()
    if not inner:
        return None
    return inner.split()[0]


def is_html_close(line: str) -> bool:
    return bool(re.match(r"^</[a-zA-Z][\w:-]*\s*>\s*$", line.strip()))


def html_open_tag_name(line: str) -> str | None:
    s = line.strip()
    if not s.startswith("<") or s.startswith("</") or s.startswith("<!--") or s.startswith("<!DOCTYPE"):
        return None
    m = re.match(r"^<([a-zA-Z][\w:-]*)\b", s)
    if not m:
        return None
    return m.group(1).lower()


def is_html_open_only(line: str) -> bool:
    s = line.strip()
    tag = html_open_tag_name(s)
    if not tag or tag in VOID_TAGS:
        return False
    if s.endswith("/>"):
        return False
    if re.search(rf"</{re.escape(tag)}\s*>", s):
        return False
    return True


def format_lines(text: str) -> str:
    lines = [ln.rstrip() for ln in text.split("\n")]
    out: list[str] = []
    indent = 0

    for raw in lines:
        line = raw.strip()
        if not line:
            if out and out[-1] != "":
                out.append("")
            continue

        # Jinja closing / mid blocks dedent first
        jw = jinja_word(line)
        if jw in CLOSE_JINJA or jw in MID_JINJA:
            indent = max(0, indent - 1)

        # HTML closing tags dedent first
        if is_html_close(line):
            indent = max(0, indent - 1)

        out.append(("  " * indent) + line)

        # Jinja opening / mid blocks indent after
        if jw in OPEN_JINJA or jw in MID_JINJA:
            indent += 1
            continue

        # plain set/include/import/etc stay neutral
        if jw:
            continue

        # HTML opening tags indent after
        if is_html_open_only(line):
            indent += 1

    # collapse excessive blank lines
    formatted = "\n".join(out)
    formatted = re.sub(r"\n{3,}", "\n\n", formatted).rstrip() + "\n"
    return formatted


def main() -> int:
    target = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_TARGET
    if not target.exists():
        print(f"missing: {target}", file=sys.stderr)
        return 1

    original = target.read_text(encoding="utf-8")
    source = normalize(original)
    formatted = format_lines(source)

    if formatted == original:
        print(f"no changes: {target}")
        return 0

    backup = backup_file(target)
    target.write_text(formatted, encoding="utf-8")

    print(f"changed: {target}")
    print(f"backup:  {backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
