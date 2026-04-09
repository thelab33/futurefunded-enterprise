from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Set

ROOT = Path.cwd()

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

REPORT_DIR = ROOT / "artifacts" / "repo_audit"
JSON_REPORT = REPORT_DIR / "repo_inventory_report.json"
MD_REPORT = REPORT_DIR / "repo_inventory_report.md"

TEMPLATES_ROOT = ROOT / "apps/web/app/templates"
STATIC_ROOT = ROOT / "apps/web/app/static"
ROUTES_ROOT = ROOT / "apps/web/app/routes"
SCRIPTS_ROOT = ROOT / "scripts"
TOOLS_ROOT = ROOT / "tools"
TESTS_ROOT = ROOT / "tests"

ROOT_PATCH_REVIEW_RE = re.compile(
    r"(patch|proof|rescue|bak|backup|legacy|old|tmp|temp|apply_|fix_|refactor)",
    re.I,
)

ROUTE_PATTERNS = [
    re.compile(r'render_template\(\s*["\']([^"\']+)["\']'),
    re.compile(r'template_name\s*=\s*["\']([^"\']+)["\']'),
]

JINJA_PATTERNS = [
    re.compile(r'{%\s*extends\s+["\']([^"\']+)["\']'),
    re.compile(r'{%\s*include\s+["\']([^"\']+)["\']'),
    re.compile(r'{%\s*import\s+["\']([^"\']+)["\']'),
    re.compile(r'{%\s*from\s+["\']([^"\']+)["\']\s+import'),
]

STATIC_URLFOR_PATTERN = re.compile(
    r"url_for\(\s*['\"]static['\"]\s*,\s*filename\s*=\s*['\"]([^'\"]+)['\"]"
)
STATIC_RAW_PATTERN = re.compile(r'["\'](/static/[^"\']+)["\']')

PLAYWRIGHT_PROJECT_RE = re.compile(r"name\s*:\s*['\"]([^'\"]+)['\"]")
SCRIPT_PROJECT_FLAG_RE = re.compile(r"--project=([A-Za-z0-9_-]+)")

ALLOWED_ROOT_FILES = {
    "README.md",
    "package.json",
    "package-lock.json",
    "requirements.txt",
    "requirements-dev.txt",
    "run.py",
    ".gitignore",
    ".env.example",
    "Makefile",
    "playwright.config.ts",
}


@dataclass
class Report:
    repo_root: str
    totals: Dict[str, int]
    route_template_refs: List[Dict[str, str]]
    missing_route_templates: List[Dict[str, str]]
    jinja_template_refs: List[Dict[str, str]]
    missing_jinja_templates: List[Dict[str, str]]
    platform_pages: List[str]
    platform_shells: List[str]
    platform_partials: List[str]
    shared_macros: List[str]
    shared_partials: List[str]
    campaign_templates: List[str]
    referenced_assets: List[str]
    unreferenced_css_candidates: List[str]
    unreferenced_js_candidates: List[str]
    backup_files_in_live_tree: List[str]
    root_loose_review_candidates: List[str]
    playwright_projects: List[str]
    package_script_project_refs: Dict[str, str]
    package_script_project_mismatches: List[Dict[str, str]]


def should_skip(path: Path) -> bool:
    return any(part in IGNORE_DIR_NAMES for part in path.parts)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def walk_files(root: Path) -> List[Path]:
    out: List[Path] = []
    for p in root.rglob("*"):
        if should_skip(p):
            continue
        if p.is_file():
            out.append(p)
    return out


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return path.read_text(encoding="utf-8", errors="ignore")


def list_template_files(subdir: str) -> List[str]:
    base = TEMPLATES_ROOT / subdir
    if not base.exists():
        return []
    return sorted(
        rel(p)
        for p in base.rglob("*.html")
        if p.is_file() and ".bak" not in p.name and not should_skip(p)
    )


def collect_route_template_refs() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    refs: List[Dict[str, str]] = []
    missing: List[Dict[str, str]] = []
    active_templates = {
        p.relative_to(TEMPLATES_ROOT).as_posix()
        for p in TEMPLATES_ROOT.rglob("*.html")
        if ".bak" not in p.name and p.is_file()
    }

    for py in ROUTES_ROOT.rglob("*.py"):
        if should_skip(py):
            continue
        text = read_text(py)
        for pat in ROUTE_PATTERNS:
            for match in pat.findall(text):
                item = {"file": rel(py), "template": match}
                refs.append(item)
                if match.endswith(".html") and match not in active_templates:
                    missing.append(item)
    return refs, missing


def collect_jinja_refs() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    refs: List[Dict[str, str]] = []
    missing: List[Dict[str, str]] = []
    active_templates = {
        p.relative_to(TEMPLATES_ROOT).as_posix()
        for p in TEMPLATES_ROOT.rglob("*.html")
        if ".bak" not in p.name and p.is_file()
    }

    for tpl in TEMPLATES_ROOT.rglob("*.html"):
        if should_skip(tpl) or ".bak" in tpl.name:
            continue
        text = read_text(tpl)
        for pat in JINJA_PATTERNS:
            for match in pat.findall(text):
                item = {"file": rel(tpl), "template": match}
                refs.append(item)
                if match.endswith(".html") and match not in active_templates:
                    missing.append(item)
    return refs, missing


def collect_referenced_assets() -> Set[str]:
    assets: Set[str] = set()
    for tpl in TEMPLATES_ROOT.rglob("*.html"):
        if should_skip(tpl) or ".bak" in tpl.name:
            continue
        text = read_text(tpl)

        for match in STATIC_URLFOR_PATTERN.findall(text):
            assets.add(match.lstrip("/"))

        for raw in STATIC_RAW_PATTERN.findall(text):
            assets.add(raw.replace("/static/", "", 1).lstrip("/"))

    return assets


def collect_unreferenced_assets(referenced_assets: Set[str]) -> tuple[list[str], list[str]]:
    css_candidates: List[str] = []
    js_candidates: List[str] = []

    css_root = STATIC_ROOT / "css"
    js_root = STATIC_ROOT / "js"

    if css_root.exists():
        for p in css_root.rglob("*.css"):
            rp = p.relative_to(STATIC_ROOT).as_posix()
            if rp not in referenced_assets:
                css_candidates.append(rel(p))

    if js_root.exists():
        for p in js_root.rglob("*.js"):
            rp = p.relative_to(STATIC_ROOT).as_posix()
            if rp not in referenced_assets:
                js_candidates.append(rel(p))

    return sorted(css_candidates), sorted(js_candidates)


def collect_backups_in_live_tree() -> List[str]:
    out: List[str] = []
    live_roots = [
        ROOT / "apps/web/app",
        ROOT / "tests",
        ROOT / "scripts",
    ]
    for base in live_roots:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if should_skip(p) or not p.is_file():
                continue
            if ".bak" in p.name:
                out.append(rel(p))
    return sorted(out)


def collect_root_loose_review_candidates() -> List[str]:
    out: List[str] = []
    for p in ROOT.iterdir():
        if p.is_dir():
            continue
        if p.name in ALLOWED_ROOT_FILES:
            continue
        if ROOT_PATCH_REVIEW_RE.search(p.name):
            out.append(rel(p))
    return sorted(out)


def collect_playwright_mismatches() -> tuple[list[str], dict[str, str], list[dict[str, str]]]:
    projects: List[str] = []
    script_refs: Dict[str, str] = {}
    mismatches: List[Dict[str, str]] = []

    pw_config = ROOT / "playwright.config.ts"
    if pw_config.exists():
        text = read_text(pw_config)
        projects = sorted(set(PLAYWRIGHT_PROJECT_RE.findall(text)))

    pkg = ROOT / "package.json"
    if pkg.exists():
        data = json.loads(read_text(pkg))
        scripts = data.get("scripts", {})
        for name, cmd in scripts.items():
            m = SCRIPT_PROJECT_FLAG_RE.search(cmd)
            if m:
                project = m.group(1)
                script_refs[name] = project
                if project not in projects:
                    mismatches.append(
                        {
                            "script": name,
                            "project": project,
                            "available_projects": ", ".join(projects),
                        }
                    )

    return projects, script_refs, mismatches


def build_markdown(report: Report) -> str:
    lines: List[str] = []
    lines.append("# FutureFunded Repo Inventory Audit")
    lines.append("")
    lines.append(f"Repo root: `{report.repo_root}`")
    lines.append("")
    lines.append("## Totals")
    lines.append("")
    for k, v in report.totals.items():
        lines.append(f"- **{k}**: {v}")
    lines.append("")
    lines.append("## Canonical platform map")
    lines.append("")
    lines.append("### Platform pages")
    for item in report.platform_pages:
        lines.append(f"- `{item}`")
    lines.append("")
    lines.append("### Platform shells")
    for item in report.platform_shells:
        lines.append(f"- `{item}`")
    lines.append("")
    lines.append("### Platform partials")
    for item in report.platform_partials:
        lines.append(f"- `{item}`")
    lines.append("")
    lines.append("### Campaign templates")
    for item in report.campaign_templates:
        lines.append(f"- `{item}`")
    lines.append("")
    lines.append("### Shared macros")
    for item in report.shared_macros:
        lines.append(f"- `{item}`")
    lines.append("")
    lines.append("### Shared partials")
    for item in report.shared_partials:
        lines.append(f"- `{item}`")
    lines.append("")
    lines.append("## Route → template refs")
    lines.append("")
    for item in report.route_template_refs:
        lines.append(f"- `{item['file']}` → `{item['template']}`")
    lines.append("")
    lines.append("## Missing route templates")
    lines.append("")
    if report.missing_route_templates:
        for item in report.missing_route_templates:
            lines.append(f"- `{item['file']}` → `{item['template']}`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Missing Jinja template refs")
    lines.append("")
    if report.missing_jinja_templates:
        for item in report.missing_jinja_templates:
            lines.append(f"- `{item['file']}` → `{item['template']}`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Referenced static assets")
    lines.append("")
    for item in report.referenced_assets:
        lines.append(f"- `{item}`")
    lines.append("")
    lines.append("## Unreferenced CSS candidates")
    lines.append("")
    if report.unreferenced_css_candidates:
        for item in report.unreferenced_css_candidates:
            lines.append(f"- `{item}`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Unreferenced JS candidates")
    lines.append("")
    if report.unreferenced_js_candidates:
        for item in report.unreferenced_js_candidates:
            lines.append(f"- `{item}`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Backup files still in live tree")
    lines.append("")
    if report.backup_files_in_live_tree:
        for item in report.backup_files_in_live_tree:
            lines.append(f"- `{item}`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Root-level review candidates")
    lines.append("")
    if report.root_loose_review_candidates:
        for item in report.root_loose_review_candidates:
            lines.append(f"- `{item}`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Playwright config drift")
    lines.append("")
    lines.append(f"- Available projects: `{', '.join(report.playwright_projects) or 'none'}`")
    lines.append("")
    if report.package_script_project_refs:
        lines.append("### Scripts using --project")
        for name, project in report.package_script_project_refs.items():
            lines.append(f"- `{name}` → `{project}`")
    lines.append("")
    if report.package_script_project_mismatches:
        lines.append("### Mismatches")
        for item in report.package_script_project_mismatches:
            lines.append(
                f"- `{item['script']}` asks for `{item['project']}`, "
                f"but available projects are `{item['available_projects']}`"
            )
    else:
        lines.append("### Mismatches")
        lines.append("- none")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    all_files = walk_files(ROOT)
    route_refs, missing_route_templates = collect_route_template_refs()
    jinja_refs, missing_jinja_templates = collect_jinja_refs()
    referenced_assets = collect_referenced_assets()
    unref_css, unref_js = collect_unreferenced_assets(referenced_assets)
    backups = collect_backups_in_live_tree()
    root_candidates = collect_root_loose_review_candidates()
    projects, script_refs, mismatches = collect_playwright_mismatches()

    report = Report(
        repo_root=str(ROOT),
        totals={
            "all_files_scanned": len(all_files),
            "route_template_refs": len(route_refs),
            "missing_route_templates": len(missing_route_templates),
            "jinja_template_refs": len(jinja_refs),
            "missing_jinja_templates": len(missing_jinja_templates),
            "referenced_assets": len(referenced_assets),
            "unreferenced_css_candidates": len(unref_css),
            "unreferenced_js_candidates": len(unref_js),
            "backup_files_in_live_tree": len(backups),
            "root_loose_review_candidates": len(root_candidates),
        },
        route_template_refs=sorted(route_refs, key=lambda x: (x["file"], x["template"])),
        missing_route_templates=sorted(missing_route_templates, key=lambda x: (x["file"], x["template"])),
        jinja_template_refs=sorted(jinja_refs, key=lambda x: (x["file"], x["template"])),
        missing_jinja_templates=sorted(missing_jinja_templates, key=lambda x: (x["file"], x["template"])),
        platform_pages=list_template_files("platform/pages"),
        platform_shells=list_template_files("platform/shells"),
        platform_partials=list_template_files("platform/partials"),
        shared_macros=list_template_files("shared/macros"),
        shared_partials=list_template_files("shared/partials"),
        campaign_templates=list_template_files("campaign"),
        referenced_assets=sorted(referenced_assets),
        unreferenced_css_candidates=unref_css,
        unreferenced_js_candidates=unref_js,
        backup_files_in_live_tree=backups,
        root_loose_review_candidates=root_candidates,
        playwright_projects=projects,
        package_script_project_refs=script_refs,
        package_script_project_mismatches=mismatches,
    )

    JSON_REPORT.write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")
    MD_REPORT.write_text(build_markdown(report), encoding="utf-8")

    print(f"wrote: {JSON_REPORT}")
    print(f"wrote: {MD_REPORT}")

    print("\n== QUICK SUMMARY ==")
    for k, v in report.totals.items():
        print(f"{k}: {v}")

    print("\n== PLAYWRIGHT PROJECTS ==")
    print(", ".join(report.playwright_projects) if report.playwright_projects else "none")

    print("\n== PACKAGE SCRIPT PROJECT MISMATCHES ==")
    if report.package_script_project_mismatches:
        for item in report.package_script_project_mismatches:
            print(
                f"{item['script']}: asks for {item['project']} "
                f"(available: {item['available_projects']})"
            )
    else:
        print("none")


if __name__ == "__main__":
    main()
