#!/usr/bin/env python3
"""Summarise LCOV by crate without hiding missing hits or unmeasured branches."""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path


def package(path: str) -> str:
    norm = path.replace('\\', '/')
    for prefix in ('crates/', 'apps/'):
        pos = norm.find('/' + prefix)
        tail = norm if norm.startswith(prefix) else (norm[pos + 1:] if pos >= 0 else '')
        parts = tail.split('/')
        if len(parts) >= 3 and tail.startswith(prefix):
            return '/'.join(parts[:2])
    if norm.startswith('xtask/') or '/xtask/' in norm:
        return 'xtask'
    return '(other)'


def parse_lcov(content: str) -> dict:
    """Use the instrumenter's LF/LH and FNF/FNH totals: regions may share lines."""
    files = defaultdict(lambda: {'lines': {}, 'functions': {}, 'branches': {}, 'reported': {}})
    filename = None
    for raw in content.splitlines():
        if raw.startswith('SF:'):
            filename = raw[3:].replace('\\', '/')
        elif raw == 'end_of_record':
            filename = None
        elif filename is None:
            continue
        elif raw.startswith('DA:'):
            fields = raw[3:].split(',')
            if len(fields) >= 2 and fields[0].isdigit() and fields[1].isdigit():
                line, count = int(fields[0]), int(fields[1])
                hit = files[filename]['lines']
                hit[line] = max(hit.get(line, 0), count)
        elif raw.startswith('FNDA:'):
            count, name = raw[5:].split(',', 1)
            if count.isdigit():
                hit = files[filename]['functions']
                hit[name] = max(hit.get(name, 0), int(count))
        elif raw[:3] in ('LF:', 'LH:') and raw[3:].isdigit():
            key = raw[:2]
            reported = files[filename]['reported']
            reported[key] = max(int(raw[3:]), reported.get(key, 0))
        elif raw[:4] in ('FNF:', 'FNH:', 'BRF:', 'BRH:') and raw[4:].isdigit():
            key = raw[:3]
            reported = files[filename]['reported']
            reported[key] = max(int(raw[4:]), reported.get(key, 0))
        elif raw.startswith('BRDA:'):
            fields = raw[5:].split(',', 3)
            if len(fields) == 4:
                line, block, branch, count = fields
                key = (line, block, branch)
                hit = files[filename]['branches']
                taken = 0 if count == '-' else int(count)
                hit[key] = max(hit.get(key, 0), taken)
    return files


def summarise(files: dict) -> dict:
    def blank():
        return {'files': 0, 'lines': 0, 'lines_hit': 0,
                'functions': 0, 'functions_hit': 0,
                'branches': 0, 'branches_hit': 0}

    packages = defaultdict(blank)
    for filename, items in files.items():
        row = packages[package(filename)]
        row['files'] += 1
        for label, total_key, hit_key in (
            ('lines', 'LF', 'LH'), ('functions', 'FNF', 'FNH'), ('branches', 'BRF', 'BRH')
        ):
            row[label] += items['reported'].get(total_key, len(items[label]))
            row[label + '_hit'] += items['reported'].get(
                hit_key, sum(count > 0 for count in items[label].values())
            )
    total = {key: sum(row[key] for row in packages.values()) for key in blank()}
    return {'total': total, 'packages': dict(sorted(packages.items()))}


def ratio(row: dict, label: str) -> str:
    n = row[label]
    if n == 0:
        return 'not measured'
    hits = row[label + '_hit']
    return f'{hits}/{n} ({hits * 100 / n:.2f}%)'


def markdown(summary: dict) -> str:
    lines = [
        '# Instrumented workspace coverage', '',
        'Only instrumented source files are counted. A crate absent from LCOV is **unmeasured**, not 100% covered.',
        'Branch coverage is **not measured** when LCOV has no branch records.', '',
        '| Package | Files | Lines | Functions | Branches |',
        '|---|---:|---:|---:|---:|',
    ]
    for name, data in [*summary['packages'].items(), ('**Total**', summary['total'])]:
        lines.append(
            f'| {name} | {data["files"]} | {ratio(data, "lines")} | '
            f'{ratio(data, "functions")} | {ratio(data, "branches")} |'
        )
    return '\n'.join(lines) + '\n'


def main(args: list[str]) -> int:
    if len(args) != 4:
        print('usage: quality_coverage.py <input.lcov> <output.md> <output.json>', file=sys.stderr)
        return 2
    source, md, out_json = (Path(path) for path in args[1:])
    if not source.is_file():
        print(f'LCOV report missing: {source}', file=sys.stderr)
        return 1
    result = summarise(parse_lcov(source.read_text(encoding='utf-8')))
    if result['total']['lines'] == 0:
        print('No instrumented lines; refusing to report an empty measurement', file=sys.stderr)
        return 1
    for path, payload in (
        (md, markdown(result)),
        (out_json, json.dumps(result, indent=2, sort_keys=True) + '\n'),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding='utf-8')
    print(markdown(result))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
