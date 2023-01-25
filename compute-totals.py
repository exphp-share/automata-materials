#!/usr/bin/env python3

import argparse
import os
import sys
from collections import Counter
from ruamel.yaml import YAML
import typing as tp
yaml = YAML(typ='safe')

PROG = os.path.basename(sys.argv[0])

def main():
    parser = argparse.ArgumentParser(
        description='compute total weapon upgrade requirements',
    )
    parser.add_argument('--file', default='weapon-upgrades.yaml', help='ingredients yaml file')
    parser.add_argument('--current-levels', metavar='YAMLFILE', help='read current levels from a YAML file, so that the displayed counts do not count upgrades you already have')
    parser.add_argument('--markdown', action='store_true')
    args = parser.parse_args()

    weapons = read_weapons(args.file)
    current_levels = None
    if args.current_levels is not None:
        current_levels = read_current_levels(args.current_levels)
        validate_current_levels(weapons, current_levels, current_levels_path=args.current_levels)

    counts = count_ingredients(weapons, current_levels)
    if args.markdown:
        display_counts_md(counts)
    else:
        display_counts(counts)

def read_weapons(path: str):
    with open(path) as f:
        return yaml.load(f)

def read_current_levels(path: str) -> dict[str, int]:
    with open(path) as f:
        d = yaml.load(f)
    if not isinstance(d, dict):
        die(f'{path}: file must be a YAML mapping from weapon names to level numbers, got a {type(d)}')
    for key, level in d.items():
        if not isinstance(level, int):
            die(f'{path}: at {repr(key)}: level must be integer')
        if level < 1:
            die(f'{path}: at {repr(key)}: minimum level is 1')
    return d

def count_ingredients(weapons: list, current_levels: dict[str, int] | None):
    counter = Counter()
    for weapon in weapons:
        name = weapon['name']
        skipped_levels = 0 if current_levels is None else current_levels.get(name, 1) - 1
        for upgrade in weapon['ingredients'][skipped_levels:]:
            counter.update(upgrade)
    return counter

def validate_current_levels(weapons: list, current_levels: dict[str, int], current_levels_path: str):
    all_names = set(weapon['name'] for weapon in weapons)
    for name in current_levels:
        if name not in all_names:
            die(f'{current_levels_path}: {repr(name)} is not a known weapon')

def display_counts(counts: Counter[str]):
    maxlen = max(len(key) for key in counts)
    for ingredient, count in counts.most_common():
        print(f'{ingredient:>{maxlen}} : {count}')

def display_counts_md(counts: Counter[str]):
    maxlen = max(len(key) for key in counts)
    print('| Material | Count |')
    print('| ---:| ---:|')
    for ingredient, count in counts.most_common():
        print(f'| {ingredient:>{maxlen}} | {count:3} |')

# ------------------------------------------------------

def warn(*args, **kw):
    print(f'{PROG}:', *args, file=sys.stderr, **kw)

def die(*args, code=1):
    warn('Fatal:', *args)
    sys.exit(code)

# ------------------------------------------------------

if __name__ == '__main__':
    main()
