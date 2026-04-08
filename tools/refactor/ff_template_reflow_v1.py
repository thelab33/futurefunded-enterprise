from __future__ import annotations

import re
import sys
import shutil
from datetime import datetime
from pathlib import Path

VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

JINJA_CLOSE_WORDS = {
    "endif", "endfor", "endblock", "endmacro", "endwith", "endcall",
    "endfilter", "endautoescape", "endraw", "endtrans",
}
JINJA_MID_WORDS = {"else", "elif"}
JINJA_NEUTRAL_WORDS = {
    "set", "include", "import", "from", "extends", "do", "break",
    "continue",
}
JINJA_OPEN_WORDS = {
    "if", "for", "block", "macro", "with", "call", "filter",
    "autoescape", "raw", "trans",
}

ROOT = Path.home() / "futurefunded-enterprise"
DEFAULT_TARGET = ROOT / "apps/web/app/templates/campaign/index.html"


def backup_file(path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_name(f"{path.name}.{ts}.bak")
    shutil.copy2(path, backup)
    return backup


def protect(text: str):
    store: dict[str, str] = {}
    counters = {"COMM": 0, "STMT": 0, "EXPR": 0}

    def repl_comm(m: re.Match[str]) -> str:
        counters["COMM"] += 1
        token = f"__JCOMM_{counters['COMM']:05d}__"
        store[token] = m.group(0)
        return token

    def repl_stmt(m: re.Match[str]) -> str:
        counters["STMT"] += 1
        token = f"__JSTMT_{counters['STMT']:05d}__"
        store[token] = m.group(0)
        return token

    def repl_expr(m: re.Match[str]) -> str:
        counters["EXPR"] += 1
        token = f"__JEXPR_{counters['EXPR']:05d}__"
        store[token] = m.group(0)
        return token

    text = re.sub(r"{#.*?#}", repl_comm, text, flags=re.S)
    text = re.sub(r"{%.*?%}", repl_stmt, text, flags=re.S)
    text = re.sub(r"{{.*?}}", repl_expr, text, flags=re.S)

    return text, store


def restore(text: str, store: dict[str, str]) -> str:
    for token, value in store.items():
        text = text.replace(token, value)
    return text


def normalize_newlines(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def add_structural_breaks(text: str) -> str:
    # break between adjacent tags
    text = re.sub(r">\s*<", ">\n<", text)

    # keep Jinja statements/comments on their own lines
    text = re.sub(r"\s*(__(?:JSTMT|JCOMM)_\d+__)\s*", r"\n\1\n", text)

    # break before/after major HTML boundaries
    text = re.sub(r"\s*(</?(?:body|main|section|article|aside|header|footer|nav|div|form|fieldset|template)\b[^>]*>)\s*",
                  r"\n\1\n", text, flags=re.I)

    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def jinja_kind(line: str) -> str | None:
    m = re.fullmatch(r"__(JSTMT|JCOMM)_\d+__", line.strip())
    if not m:
        return None
    return m.group(1)


def jinja_stmt_word(restored_line: str) -> str | None:
    s = restored_line.strip()
    if not (s.startswith("{%") and s.endswith("%}")):
        return None
    inner = s[2:-2].strip()
    if not inner:
        return None
    return inner.split()[0]


def line_is_closing_html(line: str) -> bool:
    return bool(re.match(r"^\s*</[a-zA-Z][\w:-]*\s*>\s*$", line))


def line_is_opening_html(line: str) -> bool:
    s = line.strip()
    if not s.startswith("<") or s.startswith("</") or s.startswith("<!--") or s.startswith("<!DOCTYPE"):
        return False
    m = re.match(r"^<([a-zA-Z][\w:-]*)\b", s)
    if not m:
        return False
    tag = m.group(1).lower()
    if tag in VOID_TAGS:
        return False
    if s.endswith("/>"):
        return False
    if re.search(rf"</{re.escape(tag)}\s*>", s):
        return False
    return True


def tidy_line_spacing(line: str) -> str:
    line = re.sub(r"\s{2,}", " ", line).strip()
    return line


def format_template(text: str, store: dict[str, str]) -> str:
    text = normalize_newlines(text)
    text = add_structural_breaks(text)

    raw_lines = [ln for ln in text.split("\n") if ln.strip()]
    out: list[str] = []
    indent = 0

    for raw in raw_lines:
        line = raw.strip()

        # Restore only for logic checks, not output yet
        restored_line = restore(line, store)

        jk = jinja_kind(line)
        if jk == "COMM":
            out.append(("  " * indent) + restored_line)
            continue

        if jk == "STMT":
            word = jinja_stmt_word(restored_line)
            if word in JINJA_CLOSE_WORDS or word in JINJA_MID_WORDS:
                indent = max(0, indent - 1)

            out.append(("  " * indent) + restored_line)

            if word in JINJA_OPEN_WORDS or word in JINJA_MID_WORDS:
                indent += 1
            continue

        if line_is_closing_html(restored_line):
            indent = max(0, indent - 1)

        out.append(("  " * indent) + restore(tidy_line_spacing(line), store))

        if line_is_opening_html(restored_line):
            indent += 1

    formatted = "\n".join(out).rstrip() + "\n"

    # final whitespace cleanup
    formatted = re.sub(r"[ \t]+\n", "\n", formatted)
    formatted = re.sub(r"\n{3,}", "\n\n", formatted)

    return formatted


def main() -> int:
    target = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_TARGET
    if not target.exists():
        print(f"missing: {target}", file=sys.stderr)
        return 1

    original = target.read_text(encoding="utf-8")
    protected, store = protect(original)
    formatted = format_template(protected, store)

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
