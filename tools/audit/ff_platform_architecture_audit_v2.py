from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

ROOT = Path.cwd()
REPORT_DIR = ROOT / "artifacts" / "platform_architecture_audit"
JSON_REPORT = REPORT_DIR / "platform_architecture_audit_v2.json"
MD_REPORT = REPORT_DIR / "platform_architecture_audit_v2.md"

APP_ROOT = ROOT / "apps" / "web" / "app"
ROUTES_ROOT = APP_ROOT / "routes"
TEMPLATES_ROOT = APP_ROOT / "templates"
STATIC_ROOT = APP_ROOT / "static"
TESTS_ROOT = ROOT / "tests"
TOOLS_ROOT = ROOT / "tools"
SCRIPTS_ROOT = ROOT / "scripts"

IGNORE_DIR_NAMES = {
    ".git",
    ".venv",
    "node_modules",
    "playwright-report",
    "test-results",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
}

ROUTE_DECORATOR_RE = re.compile(
    r"@(?P<blueprint>[A-Za-z_][A-Za-z0-9_]*)\.(?P<method>get|post|put|delete|patch|route)\((?P<args>.*?)\)\s*\n"
    r"def\s+(?P<func>[A-Za-z_][A-Za-z0-9_]*)\s*\(",
    re.S,
)

FUNC_DEF_RE = re.compile(r"^def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", re.M)
TEMPLATE_LITERAL_RE = re.compile(r"render_template\(\s*[\"\']([^\"\']+\.html)[\"\']")
TEMPLATE_KW_RE = re.compile(r"template_name\s*=\s*[\"\']([^\"\']+\.html)[\"\']")
HELPER_CALL_RE = re.compile(r"return\s+([A-Za-z_][A-Za-z0-9_]*)\((.*?)\)", re.S)
STRING_KWARG_RE = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*[\"\']([^\"\']+)[\"\']")
PAGE_KEY_TEMPLATE_FSTRING_RE = re.compile(
    r"[fF][\"\']platform/pages/\{([A-Za-z_][A-Za-z0-9_]*)\}\.html[\"\']"
)
DICT_ASSIGN_RE = re.compile(
    r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{(.*?)\}\s*", re.S
)
DICT_PAIR_RE = re.compile(r"[\"\']([^\"\']+)[\"\']\s*:\s*[\"\']([^\"\']+)[\"\']")

JINJA_PATTERNS = {
    "extends": re.compile(r'{%\s*extends\s+["\']([^"\']+)["\']'),
    "include": re.compile(r'{%\s*include\s+["\']([^"\']+)["\']'),
    "import": re.compile(r'{%\s*import\s+["\']([^"\']+)["\']'),
    "from_import": re.compile(r'{%\s*from\s+["\']([^"\']+)["\']\s+import'),
}

STATIC_URLFOR_PATTERN = re.compile(
    r"url_for\(\s*['\"]static['\"]\s*,\s*filename\s*=\s*['\"]([^'\"]+)['\"]"
)
STATIC_RAW_PATTERN = re.compile(r'["\'](/static/[^"\']+)["\']')

HTTP_METHODS = {"get", "post", "put", "delete", "patch", "route"}


@dataclass
class RouteRecord:
    file: str
    blueprint: str
    method: str
    path: str
    function: str
    resolved_template: Optional[str] = None
    resolution: str = "unresolved"
    helper_call: Optional[str] = None
    notes: List[str] = field(default_factory=list)


@dataclass
class TemplateRecord:
    template: str
    extends: List[str] = field(default_factory=list)
    includes: List[str] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    referenced_assets: List[str] = field(default_factory=list)
    referenced_by_routes: List[str] = field(default_factory=list)
    reachable_from_routes: bool = False


@dataclass
class Report:
    repo_root: str
    totals: Dict[str, int]
    route_inventory: List[Dict[str, object]]
    route_templates_resolved: List[str]
    route_templates_unresolved: List[Dict[str, object]]
    reachable_templates: List[str]
    unreachable_platform_templates: List[str]
    unreachable_shared_templates: List[str]
    template_graph: List[Dict[str, object]]
    referenced_assets_from_reachable_templates: List[str]
    unreferenced_css_candidates: List[str]
    unreferenced_js_candidates: List[str]
    notes: List[str]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def should_skip(path: Path) -> bool:
    return any(part in IGNORE_DIR_NAMES for part in path.parts)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return path.read_text(encoding="utf-8", errors="ignore")


def list_template_files() -> List[Path]:
    if not TEMPLATES_ROOT.exists():
        return []
    return sorted(
        p for p in TEMPLATES_ROOT.rglob("*.html")
        if p.is_file() and ".bak" not in p.name and not should_skip(p)
    )


def extract_python_functions(text: str) -> Dict[str, str]:
    lines = text.splitlines()
    out: Dict[str, str] = {}
    current_name: Optional[str] = None
    current_indent: Optional[int] = None
    buf: List[str] = []

    def flush() -> None:
        nonlocal current_name, current_indent, buf
        if current_name is not None:
            out[current_name] = "\n".join(buf)
        current_name = None
        current_indent = None
        buf = []

    for line in lines:
        m = re.match(r"^(\s*)def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", line)
        if m:
            flush()
            current_indent = len(m.group(1))
            current_name = m.group(2)
            buf = [line]
            continue

        if current_name is not None:
            stripped = line.strip()
            indent = len(line) - len(line.lstrip(" "))
            if stripped and indent <= (current_indent or 0) and not line.lstrip().startswith(("#", "@")):
                flush()
                if re.match(r"^(\s*)def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", line):
                    m2 = re.match(r"^(\s*)def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", line)
                    current_indent = len(m2.group(1))
                    current_name = m2.group(2)
                    buf = [line]
                continue
            buf.append(line)

    flush()
    return out


def parse_python_literal_maps(text: str) -> Dict[str, Dict[str, str]]:
    maps: Dict[str, Dict[str, str]] = {}
    for name, body in DICT_ASSIGN_RE.findall(text):
        pairs = dict(DICT_PAIR_RE.findall(body))
        if pairs:
            maps[name] = pairs
    return maps


def resolve_template_from_function(
    func_name: str,
    functions: Dict[str, str],
    literal_maps: Dict[str, Dict[str, str]],
    call_kwargs: Optional[Dict[str, str]] = None,
    seen: Optional[Set[str]] = None,
) -> Tuple[Optional[str], str, Optional[str], List[str]]:
    seen = seen or set()
    notes: List[str] = []
    if func_name in seen:
        return None, "cycle", None, [f"cycle detected at {func_name}"]
    seen.add(func_name)

    body = functions.get(func_name, "")
    if not body:
        return None, "missing_function_body", None, [f"no body found for {func_name}"]

    literal = TEMPLATE_LITERAL_RE.search(body)
    if literal:
        return literal.group(1), "direct_render_template", None, notes

    kw = TEMPLATE_KW_RE.search(body)
    if kw:
        return kw.group(1), "template_name_kwarg", None, notes

    fstring = PAGE_KEY_TEMPLATE_FSTRING_RE.search(body)
    if fstring and call_kwargs:
        page_var = fstring.group(1)
        page_val = call_kwargs.get(page_var)
        if page_val:
            return f"platform/pages/{page_val}.html", "page_key_fstring_inference", None, notes
        notes.append(f"found page-key f-string but no kwarg for {page_var}")

    for map_name, pairs in literal_maps.items():
        if map_name in body and call_kwargs:
            for kwarg_name, kwarg_val in call_kwargs.items():
                if kwarg_val in pairs and pairs[kwarg_val].endswith(".html"):
                    return pairs[kwarg_val], f"dict_map_inference:{map_name}", None, notes

    helper_match = HELPER_CALL_RE.search(body)
    if helper_match:
        helper_name = helper_match.group(1)
        helper_args_raw = helper_match.group(2)
        helper_kwargs = dict(STRING_KWARG_RE.findall(helper_args_raw))
        resolved, how, _, child_notes = resolve_template_from_function(
            helper_name,
            functions,
            literal_maps,
            call_kwargs=helper_kwargs,
            seen=seen,
        )
        notes.extend(child_notes)
        return resolved, how, helper_name, notes

    return None, "unresolved", None, notes


def extract_route_path(args_raw: str) -> str:
    m = re.search(r"[\"\']([^\"\']+)[\"\']", args_raw)
    return m.group(1) if m else "<dynamic_or_unresolved>"


def build_route_inventory() -> List[RouteRecord]:
    records: List[RouteRecord] = []
    if not ROUTES_ROOT.exists():
        return records

    for py in sorted(ROUTES_ROOT.rglob("*.py")):
        if should_skip(py):
            continue
        text = read_text(py)
        functions = extract_python_functions(text)
        literal_maps = parse_python_literal_maps(text)

        for m in ROUTE_DECORATOR_RE.finditer(text):
            method = m.group("method")
            if method not in HTTP_METHODS:
                continue
            func_name = m.group("func")
            path = extract_route_path(m.group("args"))
            resolved, resolution, helper_call, notes = resolve_template_from_function(
                func_name,
                functions,
                literal_maps,
            )
            records.append(
                RouteRecord(
                    file=rel(py),
                    blueprint=m.group("blueprint"),
                    method=method,
                    path=path,
                    function=func_name,
                    resolved_template=resolved,
                    resolution=resolution,
                    helper_call=helper_call,
                    notes=notes,
                )
            )
    return records


def build_template_graph() -> Dict[str, TemplateRecord]:
    records: Dict[str, TemplateRecord] = {}
    for tpl in list_template_files():
        key = tpl.relative_to(TEMPLATES_ROOT).as_posix()
        text = read_text(tpl)
        record = TemplateRecord(template=key)
        record.extends = sorted(set(JINJA_PATTERNS["extends"].findall(text)))
        record.includes = sorted(set(JINJA_PATTERNS["include"].findall(text)))
        record.imports = sorted(
            set(JINJA_PATTERNS["import"].findall(text)) | set(JINJA_PATTERNS["from_import"].findall(text))
        )
        assets = set(STATIC_URLFOR_PATTERN.findall(text))
        assets |= {raw.replace("/static/", "", 1).lstrip("/") for raw in STATIC_RAW_PATTERN.findall(text)}
        record.referenced_assets = sorted(assets)
        records[key] = record
    return records


def mark_reachable_templates(route_inventory: List[RouteRecord], template_graph: Dict[str, TemplateRecord]) -> Set[str]:
    reachable: Set[str] = set()
    queue: List[str] = []

    for route in route_inventory:
        if route.resolved_template and route.resolved_template in template_graph:
            queue.append(route.resolved_template)
            template_graph[route.resolved_template].referenced_by_routes.append(
                f"{route.method.upper()} {route.path} ({route.file}:{route.function})"
            )

    while queue:
        current = queue.pop(0)
        if current in reachable:
            continue
        reachable.add(current)
        rec = template_graph.get(current)
        if not rec:
            continue
        rec.reachable_from_routes = True
        for dep in rec.extends + rec.includes + rec.imports:
            if dep in template_graph and dep not in reachable:
                queue.append(dep)

    return reachable


def collect_reachable_assets(template_graph: Dict[str, TemplateRecord], reachable: Set[str]) -> Set[str]:
    assets: Set[str] = set()
    for name in reachable:
        rec = template_graph.get(name)
        if rec:
            assets.update(rec.referenced_assets)
    return assets


def collect_unreferenced_static_candidates(reachable_assets: Set[str]) -> Tuple[List[str], List[str]]:
    css_candidates: List[str] = []
    js_candidates: List[str] = []

    css_root = STATIC_ROOT / "css"
    js_root = STATIC_ROOT / "js"

    if css_root.exists():
        for p in sorted(css_root.rglob("*.css")):
            rp = p.relative_to(STATIC_ROOT).as_posix()
            if rp not in reachable_assets:
                css_candidates.append(rel(p))

    if js_root.exists():
        for p in sorted(js_root.rglob("*.js")):
            rp = p.relative_to(STATIC_ROOT).as_posix()
            if rp not in reachable_assets:
                js_candidates.append(rel(p))

    return css_candidates, js_candidates


def build_markdown(report: Report) -> str:
    lines: List[str] = []
    lines.append("# FutureFunded Platform Architecture Audit v2")
    lines.append("")
    lines.append(f"Repo root: `{report.repo_root}`")
    lines.append("")
    lines.append("## Totals")
    lines.append("")
    for k, v in report.totals.items():
        lines.append(f"- **{k}**: {v}")
    lines.append("")

    lines.append("## Route inventory")
    lines.append("")
    for item in report.route_inventory:
        resolved = item.get("resolved_template") or "<unresolved>"
        helper = f" via {item['helper_call']}" if item.get("helper_call") else ""
        lines.append(
            f"- `{item['method'].upper()} {item['path']}` → `{resolved}` "
            f"[{item['resolution']}] from `{item['file']}:{item['function']}`{helper}"
        )
    lines.append("")

    lines.append("## Route templates resolved")
    lines.append("")
    if report.route_templates_resolved:
        for item in report.route_templates_resolved:
            lines.append(f"- `{item}`")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Route templates unresolved")
    lines.append("")
    if report.route_templates_unresolved:
        for item in report.route_templates_unresolved:
            lines.append(
                f"- `{item['method'].upper()} {item['path']}` from `{item['file']}:{item['function']}` [{item['resolution']}]"
            )
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Reachable templates from routes")
    lines.append("")
    for item in report.reachable_templates:
        lines.append(f"- `{item}`")
    lines.append("")

    lines.append("## Unreachable platform templates")
    lines.append("")
    if report.unreachable_platform_templates:
        for item in report.unreachable_platform_templates:
            lines.append(f"- `{item}`")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Unreachable shared templates")
    lines.append("")
    if report.unreachable_shared_templates:
        for item in report.unreachable_shared_templates:
            lines.append(f"- `{item}`")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Template graph")
    lines.append("")
    for item in report.template_graph:
        lines.append(f"### `{item['template']}`")
        lines.append(f"- reachable_from_routes: `{item['reachable_from_routes']}`")
        lines.append(f"- referenced_by_routes: `{', '.join(item['referenced_by_routes']) or 'none'}`")
        lines.append(f"- extends: `{', '.join(item['extends']) or 'none'}`")
        lines.append(f"- includes: `{', '.join(item['includes']) or 'none'}`")
        lines.append(f"- imports: `{', '.join(item['imports']) or 'none'}`")
        lines.append(f"- referenced_assets: `{', '.join(item['referenced_assets']) or 'none'}`")
        lines.append("")

    lines.append("## Referenced assets from reachable templates")
    lines.append("")
    if report.referenced_assets_from_reachable_templates:
        for item in report.referenced_assets_from_reachable_templates:
            lines.append(f"- `{item}`")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Unreferenced CSS candidates (reachable-surface aware)")
    lines.append("")
    if report.unreferenced_css_candidates:
        for item in report.unreferenced_css_candidates:
            lines.append(f"- `{item}`")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Unreferenced JS candidates (reachable-surface aware)")
    lines.append("")
    if report.unreferenced_js_candidates:
        for item in report.unreferenced_js_candidates:
            lines.append(f"- `{item}`")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Notes")
    lines.append("")
    for note in report.notes:
        lines.append(f"- {note}")
    lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    route_inventory = build_route_inventory()
    template_graph = build_template_graph()
    reachable = mark_reachable_templates(route_inventory, template_graph)
    reachable_assets = collect_reachable_assets(template_graph, reachable)
    unref_css, unref_js = collect_unreferenced_static_candidates(reachable_assets)

    unresolved = [
        asdict(r) for r in route_inventory
        if not r.resolved_template
    ]
    resolved_templates = sorted({r.resolved_template for r in route_inventory if r.resolved_template})

    unreachable_platform = sorted(
        name for name, rec in template_graph.items()
        if name.startswith("platform/") and not rec.reachable_from_routes
    )
    unreachable_shared = sorted(
        name for name, rec in template_graph.items()
        if name.startswith("shared/") and not rec.reachable_from_routes
    )

    notes = [
        "This audit is architecture-focused: it resolves routes to templates, then walks the Jinja dependency graph from route entry templates.",
        "It is stricter than a raw file inventory. A template can exist in the repo and still be unreachable from live routes.",
        "Helper-based route resolution is inferred for common patterns such as page_key -> platform/pages/{page_key}.html.",
        "Unresolved routes should be reviewed manually if they rely on highly dynamic logic.",
    ]

    report = Report(
        repo_root=str(ROOT),
        totals={
            "route_inventory_count": len(route_inventory),
            "route_templates_resolved": len(resolved_templates),
            "route_templates_unresolved": len(unresolved),
            "template_graph_nodes": len(template_graph),
            "reachable_templates": len(reachable),
            "unreachable_platform_templates": len(unreachable_platform),
            "unreachable_shared_templates": len(unreachable_shared),
            "reachable_assets": len(reachable_assets),
            "unreferenced_css_candidates": len(unref_css),
            "unreferenced_js_candidates": len(unref_js),
        },
        route_inventory=[asdict(r) for r in route_inventory],
        route_templates_resolved=resolved_templates,
        route_templates_unresolved=unresolved,
        reachable_templates=sorted(reachable),
        unreachable_platform_templates=unreachable_platform,
        unreachable_shared_templates=unreachable_shared,
        template_graph=[asdict(template_graph[k]) for k in sorted(template_graph)],
        referenced_assets_from_reachable_templates=sorted(reachable_assets),
        unreferenced_css_candidates=unref_css,
        unreferenced_js_candidates=unref_js,
        notes=notes,
    )

    JSON_REPORT.write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")
    MD_REPORT.write_text(build_markdown(report), encoding="utf-8")

    print(f"wrote: {JSON_REPORT}")
    print(f"wrote: {MD_REPORT}")
    print("\n== QUICK SUMMARY ==")
    for k, v in report.totals.items():
        print(f"{k}: {v}")
    print("\n== UNREACHABLE PLATFORM TEMPLATES ==")
    print("none" if not report.unreachable_platform_templates else "\n".join(report.unreachable_platform_templates))
    print("\n== UNREACHABLE SHARED TEMPLATES ==")
    print("none" if not report.unreachable_shared_templates else "\n".join(report.unreachable_shared_templates))


if __name__ == "__main__":
    main()
