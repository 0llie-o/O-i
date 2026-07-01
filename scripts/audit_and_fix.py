"""Audit script to verify config imports and deprecated Text filter usage.

Run this locally (or in CI) after pulling main to verify there are no missing
config variables and no remaining usages of aiogram.filters.Text.

Usage:
    python scripts/audit_and_fix.py

It reports:
 - Missing config imports: files that import names from config.py but those names
   are not defined in config.py.
 - Remaining usages of Text(...) in handlers/ and keyboards/.

This script does NOT modify files automatically; it reports issues so you can
review and fix them. Use it as a final safety check before deploying.
"""

from pathlib import Path
import ast
import re
import sys

ROOT = Path('.')
CONFIG_FILE = ROOT / 'config.py'

def get_config_vars():
    src = CONFIG_FILE.read_text(encoding='utf-8')
    tree = ast.parse(src)
    names = set()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    names.add(t.id)
    return names


def find_from_config_imports():
    pattern = re.compile(r'^from\s+config\s+import\s+(.*)$')
    results = []
    for p in ROOT.rglob('*.py'):
        # skip virtualenvs and .git
        if any(part.startswith('.') or part == 'venv' or part == '__pycache__' for part in p.parts):
            continue
        src = p.read_text(encoding='utf-8')
        for line in src.splitlines():
            m = pattern.match(line.strip())
            if m:
                names = [n.strip() for n in m.group(1).split(',') if n.strip()]
                results.append((str(p), names))
    return results


def find_text_usages():
    usages = []
    for p in ROOT.rglob('*.py'):
        if any(part.startswith('.') or part == 'venv' or part == '__pycache__' for part in p.parts):
            continue
        src = p.read_text(encoding='utf-8')
        if 'Text(' in src or 'from aiogram.filters import' in src:
            usages.append(str(p))
    return usages


def main():
    print('Running audit...')
    config_vars = get_config_vars()
    print('\nConfig variables found in config.py:')
    print(', '.join(sorted(config_vars)))

    imports = find_from_config_imports()
    missing = []
    for fname, names in imports:
        for n in names:
            if n not in config_vars:
                missing.append((fname, n))

    if missing:
        print('\nERROR: Missing config names imported in code:')
        for f,n in missing:
            print(f' - {f}: {n}')
    else:
        print('\nOK: No missing config imports detected.')

    text_usages = find_text_usages()
    if text_usages:
        print('\nWARNING: Files that may use deprecated Text filter or import it:')
        for f in text_usages:
            print(' -', f)
        print('\nPlease review and replace Text(...) with F equivalents (F.data, F.text, etc.).')
    else:
        print('\nOK: No Text usages detected.')

    # Syntax check
    print('\nRunning python -m py_compile on handlers/ keyboards/ database/ ...')
    import subprocess
    paths = ['handlers', 'keyboards', 'database']
    failed = False
    for p in paths:
        if Path(p).exists():
            res = subprocess.run([sys.executable, '-m', 'py_compile'] + [str(x) for x in Path(p).rglob('*.py')], capture_output=True, text=True)
            if res.returncode != 0:
                failed = True
                print(f'py_compile errors in {p}:')
                print(res.stderr)
    if not failed:
        print('OK: Syntax check passed for handlers, keyboards, database.')

if __name__ == '__main__':
    main()
