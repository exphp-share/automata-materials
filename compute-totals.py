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
    parser.add_argument('--item-list', dest='order_file', metavar='TXTFILE', help='order the ingredients by this file')
    args = parser.parse_args()

    weapons = read_weapons(args.file)
    current_levels = None
    if args.current_levels is not None:
        current_levels = CurrentLevelsFile.from_path(args.current_levels)
        current_levels.validate_against_weapons(weapons)

    order = None
    if args.order_file is not None:
        order = OrderFile.from_path(args.order_file)

    counts = count_ingredients(weapons, current_levels)
    counts = apply_ordering(counts, order)
    if args.markdown:
        display_counts_md(counts)
    else:
        display_counts(counts)

def read_weapons(path: str):
    with open(path) as f:
        return yaml.load(f)

class CurrentLevelsFile:
    def __init__(self, levels: dict[str, int], path: str):
        self.levels = levels
        self.path = path

    @classmethod
    def from_path(cls, path: str):
        with open(path) as f:
            d = yaml.load(f)
        if not isinstance(d, dict):
            die(f'{path}: file must be a YAML mapping from weapon names to level numbers, got a {type(d)}')
        for key, level in d.items():
            if not isinstance(level, int):
                die(f'{path}: at {repr(key)}: level must be integer')
            if level < 1:
                die(f'{path}: at {repr(key)}: minimum level is 1')
        return cls(d, path)

    def validate_against_weapons(self, weapons: list):
        all_names = set(weapon['name'] for weapon in weapons)
        for name in self.levels:
            if name not in all_names:
                die(f'{self.path}: {repr(name)} is not a known weapon')

class OrderFile:
    def __init__(self, order: list[str], path: str):
        self.order = order
        self.path = path

    @classmethod
    def from_path(cls, path: str):
        with open(path) as f:
            order = list(f)
            order = [line.strip() for line in order]
            order = [line for line in order if line]
        return cls(order, path)

def count_ingredients(weapons: list, current_levels: CurrentLevelsFile | None):
    counter = Counter()
    for weapon in weapons:
        name = weapon['name']
        skipped_levels = 0 if current_levels is None else current_levels.levels.get(name, 1) - 1
        for upgrade in weapon['ingredients'][skipped_levels:]:
            counter.update(upgrade)
    return counter

def apply_ordering(counts: Counter[str], order: OrderFile | None) -> list[tuple[str, int]]:
    if order is None:
        return counts.most_common()
    else:
        return [(key, counts[key]) for key in order.order if counts[key] > 0]

def display_counts(counts: list[tuple[str, int]]):
    maxlen = max(len(key) for (key, _) in counts)
    for ingredient, count in counts:
        print(f'{ingredient:>{maxlen}} : {count}')

def display_counts_md(counts: list[tuple[str, int]]):
    maxlen = max(len(key) for (key, _) in counts)
    print('| Material | Count |')
    print('| ---:| ---:|')
    for ingredient, count in counts:
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
