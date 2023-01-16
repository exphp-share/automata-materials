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
    parser.add_argument('--markdown', action='store_true')
    args = parser.parse_args()

    with open(args.file) as f:
        weapons = yaml.load(f)

    counts = count_ingredients(weapons)
    if args.markdown:
        display_counts_md(counts)
    else:
        display_counts(counts)

def count_ingredients(weapons: list):
    counter = Counter()
    for weapon in weapons:
        for upgrade in weapon['ingredients']:
            counter.update(upgrade)
    return counter

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
