#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

JINJA_EXPR_RE = re.compile(r'{{.*?}}|{#.*?#}|{%.*?%}', re.S)
ATTR_RE = re.compile(r'(\b[\w:-]+)\s*=\s*"([^"]*)"', re.S)
SCRIPT_RE = re.compile(r'<script\b[^>]*\bid\s*=\s*"([^"]+)"[^>]*>(.*?)</script>', re.I | re.S)
TAG_RE = re.compile(r'<\s*([a-zA-Z][\w:-]*)\b')
DATA_HOOK_RE = re.compile(r'\b(data-ff-[a-zA-Z0-9_-]+)\b')
CLASS_TOKEN_RE = re.compile(r'(?<![\w-])\.([_a-zA-Z][-_a-zA-Z0-9]*)')
ID_TOKEN_RE = re.compile(r'(?<![\w-])#([_a-zA-Z][-_a-zA-Z0-9]*)')
ATTR_SELECTOR_RE = re.compile(r'\[\s*(data-ff-[a-zA-Z0-9_-]+)(?:[~|^$*]?=[^\]]+)?\s*\]')
STRING_RE = re.compile(r'(["\'])(?P<val>(?:\\.|(?!\1).)*)\1')
VALID_IDISH_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9:_-]*$')
HEXISH_RE = re.compile(r'^[a-fA-F0-9]{3,8}$')

SELECTOR_METHOD_PATTERNS = [
    re.compile(r'\b(?:querySelector|querySelectorAll|matches|closest)\s*\(\s*(["\'])(?P<sel>(?:\\.|(?!\1).)*)\1\s*\)'),
    re.compile(r'\bgetElementById\s*\(\s*(["\'])(?P<sel>(?:\\.|(?!\1).)*)\1\s*\)'),
    re.compile(r'\b(?:setAttribute|getAttribute|hasAttribute|removeAttribute)\s*\(\s*(["\'])(?P<sel>(?:\\.|(?!\1).)*)\1'),
]

REF_ATTRS = ("href", "aria-controls", "aria-labelledby", "aria-describedby")
IGNORE_CLASS_TOKENS = {
    'if', 'else', 'endif', 'not', 'true', 'false', 'none', 'and', 'or', '%}', '{%', '{{', '}}'
}


@dataclass
class Surface:
    ids_static: set[str]
    ids_dynamic: set[str]
    classes_static: set[str]
    classes_dynamic: set[str]
    hooks: set[str]
    tags: set[str]
    refs_static: dict[str, list[str]]
    refs_dynamic: dict[str, list[str]]
    ffselectors_hooks: set[str]
    ffselectors_ids: set[str]
    ffselectors_classes: set[str]


@dataclass
class AuditResult:
    template: str
    css_files: list[str]
    js_files: list[str]
    counts: dict
    hard_drift: dict
    broken_static_refs: list[str]
    js_ids_missing_in_template: list[str]
    js_hooks_missing_in_template: list[str]
    js_classes_missing_in_template: list[str]
    css_hooks_missing_in_template: list[str]
    css_ids_missing_in_template: list[str]
    css_classes_missing_in_template: list[str]
    template_hooks_missing_in_js: list[str]
    template_ids_missing_in_js: list[str]
    template_classes_missing_in_css: list[str]
    ignored_notes: list[str]


def strip_jinja(text: str) -> str:
    return JINJA_EXPR_RE.sub(' ', text)


def looks_like_hex(token: str) -> bool:
    return bool(HEXISH_RE.fullmatch(token))


def is_valid_ref_target(token: str) -> bool:
    if not token or '{{' in token or '{%' in token or '://' in token or '/' in token:
        return False
    token = token.strip()
    return bool(VALID_IDISH_RE.fullmatch(token))


def normalize_template_class_attr(value: str) -> tuple[set[str], set[str]]:
    dynamic = set()
    if '{{' in value or '{%' in value:
        dynamic.add('(jinja-class-expression)')
    cleaned = strip_jinja(value)
    static = set()
    for token in re.split(r'\s+', cleaned.strip()):
        token = token.strip()
        if not token or token in IGNORE_CLASS_TOKENS:
            continue
        if token.startswith(('{', '}', '%')) or '|' in token:
            continue
        if not re.fullmatch(r'[-_a-zA-Z0-9:]+', token):
            continue
        static.add(token)
    return static, dynamic


def extract_selector_tokens(selector: str) -> tuple[set[str], set[str], set[str]]:
    ids = {x for x in ID_TOKEN_RE.findall(selector) if not looks_like_hex(x)}
    classes = set(CLASS_TOKEN_RE.findall(selector))
    hooks = set(ATTR_SELECTOR_RE.findall(selector))
    return ids, classes, hooks


def extract_template_surface(text: str) -> Surface:
    ids_static: set[str] = set()
    ids_dynamic: set[str] = set()
    classes_static: set[str] = set()
    classes_dynamic: set[str] = set()
    hooks = set(DATA_HOOK_RE.findall(text))
    tags = {m.group(1).lower() for m in TAG_RE.finditer(text)}
    refs_static: dict[str, list[str]] = defaultdict(list)
    refs_dynamic: dict[str, list[str]] = defaultdict(list)
    ffselectors_hooks: set[str] = set()
    ffselectors_ids: set[str] = set()
    ffselectors_classes: set[str] = set()

    for attr, raw in ATTR_RE.findall(text):
        attr_l = attr.lower()
        if attr_l == 'id':
            target = raw.strip()
            if '{{' in target or '{%' in target:
                ids_dynamic.add(target)
            elif is_valid_ref_target(target):
                ids_static.add(target)
        elif attr_l == 'class':
            s, d = normalize_template_class_attr(raw)
            classes_static |= s
            classes_dynamic |= d
        elif attr_l.startswith('data-ff-'):
            hooks.add(attr_l)

        if attr_l not in REF_ATTRS:
            continue
        if attr_l == 'href':
            if not raw.startswith('#'):
                continue
            targets = [raw[1:]]
        else:
            targets = raw.split()

        for target in targets:
            target = target.strip()
            if not target:
                continue
            if '{{' in target or '{%' in target:
                refs_dynamic[target].append(attr_l)
            elif is_valid_ref_target(target):
                refs_static[target].append(attr_l)

    for script_id, body in SCRIPT_RE.findall(text):
        if script_id != 'ffSelectors':
            continue
        try:
            payload = json.loads(body.strip())
        except Exception:
            continue
        hook_map = payload.get('hooks', {}) if isinstance(payload, dict) else {}
        if isinstance(hook_map, dict):
            for selector in hook_map.values():
                if not isinstance(selector, str):
                    continue
                sid, sclass, shook = extract_selector_tokens(selector)
                ffselectors_ids |= sid
                ffselectors_classes |= sclass
                ffselectors_hooks |= shook

    return Surface(
        ids_static=ids_static,
        ids_dynamic=ids_dynamic,
        classes_static=classes_static,
        classes_dynamic=classes_dynamic,
        hooks=hooks,
        tags=tags,
        refs_static=dict(refs_static),
        refs_dynamic=dict(refs_dynamic),
        ffselectors_hooks=ffselectors_hooks,
        ffselectors_ids=ffselectors_ids,
        ffselectors_classes=ffselectors_classes,
    )


def extract_css_surface(texts: Iterable[str]) -> tuple[Counter, Counter, Counter]:
    ids = Counter()
    classes = Counter()
    hooks = Counter()
    for text in texts:
        stripped = re.sub(r'/\*.*?\*/', ' ', text, flags=re.S)
        for token in ID_TOKEN_RE.findall(stripped):
            if looks_like_hex(token):
                continue
            ids[token] += 1
        for token in CLASS_TOKEN_RE.findall(stripped):
            classes[token] += 1
        for token in ATTR_SELECTOR_RE.findall(stripped):
            hooks[token] += 1
    return ids, classes, hooks


def extract_js_surface(texts: Iterable[str]) -> tuple[Counter, Counter, Counter, set[str]]:
    ids = Counter()
    classes = Counter()
    hooks = Counter()
    selector_strings: set[str] = set()
    for text in texts:
        for pattern in SELECTOR_METHOD_PATTERNS:
            for m in pattern.finditer(text):
                raw = m.group('sel')
                selector_strings.add(raw)
                if pattern.pattern.startswith('\\bgetElementById'):
                    if is_valid_ref_target(raw):
                        ids[raw] += 1
                    continue
                if raw.startswith('data-ff-'):
                    hooks[raw] += 1
                sid, sclass, shook = extract_selector_tokens(raw)
                for token in sid:
                    ids[token] += 1
                for token in sclass:
                    classes[token] += 1
                for token in shook:
                    hooks[token] += 1
        for m in STRING_RE.finditer(text):
            raw = m.group('val')
            if raw.startswith('data-ff-'):
                hooks[raw] += 1
    return ids, classes, hooks, selector_strings


def list_files(root: Path, glob_pattern: str, exclude: list[str]) -> list[Path]:
    out = []
    for p in sorted(root.glob(glob_pattern)):
        rel = p.relative_to(root).as_posix()
        if any(fnmatch.fnmatch(rel, pat) for pat in exclude):
            continue
        out.append(p)
    return out


def build_result(template_path: Path, css_paths: list[Path], js_paths: list[Path]) -> AuditResult:
    template_text = template_path.read_text(encoding='utf-8', errors='replace')
    css_texts = [p.read_text(encoding='utf-8', errors='replace') for p in css_paths]
    js_texts = [p.read_text(encoding='utf-8', errors='replace') for p in js_paths]

    template = extract_template_surface(template_text)
    css_ids, css_classes, css_hooks = extract_css_surface(css_texts)
    js_ids, js_classes, js_hooks, _js_selector_strings = extract_js_surface(js_texts)

    template_ids_all = set(template.ids_static) | set(template.ffselectors_ids)
    template_classes_all = set(template.classes_static) | set(template.ffselectors_classes)
    template_hooks_all = set(template.hooks) | set(template.ffselectors_hooks)

    broken_static_refs = sorted(k for k in template.refs_static if k not in template.ids_static)

    # only hard-report template hooks/ids missing in JS; template-only ids are often a11y headings and fine
    template_hooks_missing_in_js = sorted(x for x in template_hooks_all if x not in js_hooks)
    template_ids_missing_in_js = sorted(x for x in template.ffselectors_ids if x not in js_ids)
    template_classes_missing_in_css = sorted(x for x in template.classes_static if x not in css_classes)

    css_ids_missing_in_template = sorted(x for x in css_ids if x not in template_ids_all)
    css_hooks_missing_in_template = sorted(x for x in css_hooks if x not in template_hooks_all)
    css_classes_missing_in_template = sorted(x for x in css_classes if x not in template_classes_all)

    js_ids_missing_in_template = sorted(x for x in js_ids if x not in template_ids_all)
    js_hooks_missing_in_template = sorted(x for x in js_hooks if x not in template_hooks_all)
    js_classes_missing_in_template = sorted(x for x in js_classes if x not in template_classes_all)

    hard_drift = {
        'broken_static_refs': len(broken_static_refs),
        'js_ids_missing_in_template': len(js_ids_missing_in_template),
        'js_hooks_missing_in_template': len(js_hooks_missing_in_template),
        'css_hooks_missing_in_template': len(css_hooks_missing_in_template),
    }

    counts = {
        'template': {
            'ids_static': len(template.ids_static),
            'ids_dynamic': len(template.ids_dynamic),
            'classes_static': len(template.classes_static),
            'classes_dynamic': len(template.classes_dynamic),
            'hooks': len(template.hooks),
            'tags': len(template.tags),
            'ffselectors_ids': len(template.ffselectors_ids),
            'ffselectors_hooks': len(template.ffselectors_hooks),
        },
        'css': {'files': len(css_paths), 'ids': len(css_ids), 'classes': len(css_classes), 'hooks': len(css_hooks)},
        'js': {'files': len(js_paths), 'ids': len(js_ids), 'classes': len(js_classes), 'hooks': len(js_hooks)},
    }

    ignored_notes = [
        'External URLs and non-hash href values are ignored for ref-target checks.',
        'Hex color values like #fff are filtered out of CSS id extraction.',
        'Jinja expressions inside class attributes are stripped before class tokenization.',
        'Template-only semantic ids are not treated as hard drift by default.',
    ]

    return AuditResult(
        template=str(template_path),
        css_files=[str(p) for p in css_paths],
        js_files=[str(p) for p in js_paths],
        counts=counts,
        hard_drift=hard_drift,
        broken_static_refs=broken_static_refs,
        js_ids_missing_in_template=js_ids_missing_in_template,
        js_hooks_missing_in_template=js_hooks_missing_in_template,
        js_classes_missing_in_template=js_classes_missing_in_template,
        css_hooks_missing_in_template=css_hooks_missing_in_template,
        css_ids_missing_in_template=css_ids_missing_in_template,
        css_classes_missing_in_template=css_classes_missing_in_template,
        template_hooks_missing_in_js=template_hooks_missing_in_js,
        template_ids_missing_in_js=template_ids_missing_in_js,
        template_classes_missing_in_css=template_classes_missing_in_css,
        ignored_notes=ignored_notes,
    )


def print_section(title: str, items: Iterable[str], limit: int) -> None:
    items = list(items)
    print(f'\n== {title} ==')
    if not items:
        print('✅ none')
        return
    for item in items[:limit]:
        print(item)
    if len(items) > limit:
        print(f'... +{len(items) - limit} more')


def main() -> int:
    parser = argparse.ArgumentParser(description='Audit template/CSS/JS selector contract drift (Jinja-aware).')
    parser.add_argument('--root', default='.')
    parser.add_argument('--template', default='apps/web/app/templates/campaign/index.html')
    parser.add_argument('--css-glob', default='apps/web/app/static/css/**/*.css')
    parser.add_argument('--js-glob', default='apps/web/app/static/js/**/*.js')
    parser.add_argument('--exclude-css-glob', action='append', default=[], help='Glob(s) to exclude, repeatable.')
    parser.add_argument('--exclude-js-glob', action='append', default=[], help='Glob(s) to exclude, repeatable.')
    parser.add_argument('--json-out', default='')
    parser.add_argument('--limit', type=int, default=50)
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()

    root = Path(args.root).resolve()
    template_path = root / args.template
    css_paths = list_files(root, args.css_glob, args.exclude_css_glob)
    js_paths = list_files(root, args.js_glob, args.exclude_js_glob)

    if not template_path.exists():
        print(f'❌ Missing template: {template_path}', file=sys.stderr)
        return 2
    if not css_paths:
        print(f'❌ No CSS files matched: {args.css_glob}', file=sys.stderr)
        return 2
    if not js_paths:
        print(f'❌ No JS files matched: {args.js_glob}', file=sys.stderr)
        return 2

    result = build_result(template_path, css_paths, js_paths)

    print('== FF CONTRACT SURFACE AUDIT V2 ==')
    print(f'Template: {result.template}')
    print(f'CSS files: {len(result.css_files)}')
    print(f'JS files : {len(result.js_files)}')

    print('\n== COUNTS ==')
    print(json.dumps(result.counts, indent=2))

    print_section('HARD: BROKEN STATIC REF TARGETS', result.broken_static_refs, args.limit)
    print_section('HARD: JS IDS MISSING IN TEMPLATE', result.js_ids_missing_in_template, args.limit)
    print_section('HARD: JS HOOKS MISSING IN TEMPLATE', result.js_hooks_missing_in_template, args.limit)
    print_section('HARD: CSS HOOKS MISSING IN TEMPLATE', result.css_hooks_missing_in_template, args.limit)

    print_section('SOFT: TEMPLATE HOOKS MISSING IN JS', result.template_hooks_missing_in_js, args.limit)
    print_section('SOFT: TEMPLATE IDS FROM ffSelectors MISSING IN JS', result.template_ids_missing_in_js, args.limit)
    print_section('SOFT: TEMPLATE CLASSES MISSING IN CSS', result.template_classes_missing_in_css, args.limit)
    print_section('SOFT: CSS IDS MISSING IN TEMPLATE', result.css_ids_missing_in_template, args.limit)
    print_section('SOFT: CSS CLASSES MISSING IN TEMPLATE', result.css_classes_missing_in_template, args.limit)
    print_section('SOFT: JS CLASSES MISSING IN TEMPLATE', result.js_classes_missing_in_template, args.limit)

    print('\n== HARD DRIFT SCORE ==')
    print(json.dumps(result.hard_drift, indent=2))

    print('\n== NOTES ==')
    for note in result.ignored_notes:
        print(f'- {note}')

    if args.json_out:
        out_path = (root / args.json_out).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(asdict(result), indent=2), encoding='utf-8')
        print(f'\n✅ wrote JSON report: {out_path}')

    return 1 if args.strict and sum(result.hard_drift.values()) else 0


if __name__ == '__main__':
    raise SystemExit(main())
