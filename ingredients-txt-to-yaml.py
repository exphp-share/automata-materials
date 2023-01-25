#!/usr/bin/env python3

# Converts the ad-hoc format of weapon-upgrades.txt (which is just something that was
# easy to produce by copying and pasting stuff from the wiki) into more machine-friendly yaml

import argparse
import os
import sys
import typing as tp
from ruamel.yaml import YAML
yaml = YAML(typ='rt')

PROG = os.path.basename(sys.argv[0])

def main():
    parser = argparse.ArgumentParser(
        description='convert ingredients txt to yaml',
    )
    parser.add_argument('INPUT', nargs='?', default='data/weapon-upgrades.txt', type=str)
    parser.add_argument('--output', '-o', default='data/weapon-upgrades.yaml', type=str)
    parser.add_argument('--debug', action='store_true', help='print debugging messages')
    args = parser.parse_args()

    with open(args.INPUT) as f:
        str_lines = list(f)
    if str_lines[-1].strip() != '':
        str_lines.append('\n')

    lines = [
        NumberedLine(number=number, text=text)
        for (number, text) in enumerate(str_lines, start=1)
    ]

    if args.debug:
        debug_print = lambda str: print('DEBUG:', str, file=sys.stderr)
    else:
        debug_print = lambda str: None

    weapons = parse_text(lines, debug_print=debug_print)

    with open(args.output, 'w') as f:
        yaml.dump([weapon.serialize() for weapon in weapons], f)

# =====================================================

class Ingredient(tp.NamedTuple):
    name: str
    count: int

class Weapon(tp.NamedTuple):
    category: str
    name: str
    ingredients: list[list[Ingredient]]

    def serialize(self):
        return {
            'name': self.name,
            'category': self.category,
            'ingredients': [
                {item.name: item.count for item in upgrade}
                for upgrade in self.ingredients
            ],
        }

class NumberedLine(tp.NamedTuple):
    number: int
    text: str

class LineError(RuntimeError):
    def __init__(self, line: NumberedLine, text: str):
        super().__init__(f'at line {line.number}: {text}')

PrintFunc = tp.Callable[[str], None]

def parse_text(lines: list[NumberedLine], debug_print: PrintFunc) -> list[Weapon]:
    weapons = []
    while (parsed := try_parse_weapon_type_heading(lines)) is not None:
        category, lines = parsed
        debug_print(f'category: {category}')

        weapon, lines = parse_weapon(lines, category=category, debug_print=debug_print)
        weapons.append(weapon)

        while (parsed := try_parse_weapon_separator(lines)) is not None:
            lines = parsed
            if len(lines) == 0:
                return weapons
            weapon, lines = parse_weapon(lines, category=category, debug_print=debug_print)
            weapons.append(weapon)

    # should be at end of file
    for line in lines:
        if not is_blank_line(line):
            raise LineError(line, f'syntax error at {repr(line.text)}')

def parse_weapon(lines: list[NumberedLine], category: str, debug_print: PrintFunc):
    name, lines = parse_weapon_name_heading(lines)
    debug_print(f'weapon: {name}')
    ingredients = []
    while (parsed := try_parse_ingredient_list(lines, debug_print=debug_print)) is not None:
        ingredients.append(parsed[0])
        lines = parsed[1]
    return Weapon(name=name, category=category, ingredients=ingredients), lines

def parse_weapon_name_heading(lines: list[NumberedLine]):
    if len(lines) < 2:
        raise RuntimeError('expected weapon name, got EOF')
    a, b, *rest = lines
    if not is_blank_line(b):
        raise LineError(b, 'expected blank line after weapon name')
    return a.text.strip(), rest

def try_parse_weapon_type_heading(lines: list[NumberedLine]):
    if len(lines) < 5:
        return None
    a, b, c, d, e, f, *rest = lines
    if not (
        all(is_separator_line(line) for line in [a, b, d, e])
        and is_blank_line(f)
    ):
        return None
    return c.text.strip().lower(), rest

def try_parse_weapon_separator(lines: list[NumberedLine]):
    if len(lines) < 2:
        return None
    a, b, *rest = lines
    if not (is_separator_line(a) and is_blank_line(b)):
        return None
    return rest

def try_parse_ingredient_list(lines: list[NumberedLine], debug_print: PrintFunc) -> tuple[list[Ingredient], str] | None:
    out = []
    if len(lines) < 1:
        raise RuntimeError(f'unexpected EOF at {repr(lines[0].text)}')

    if is_separator_line(lines[0]):
        return None  # no more ingredients lists

    while (parsed := try_parse_ingredient_line(lines[0])) is not None:
        debug_print(f'ingredient: {repr(lines[0])}')
        out.append(parsed)
        lines = lines[1:]
        if len(lines) < 1:
            raise RuntimeError(f'unexpected EOF in ingredient list at {repr(lines[0].text)}')

    if not is_blank_line(lines[0]):
        raise LineError(lines[0], f'syntax error in ingredient list at {repr(lines[0].text)}')
    if not out:
        raise LineError(lines[0], f'unexpected empty list')
    debug_print('end of ingredients list')
    return out, lines[1:]  # skip the blank line

def try_parse_ingredient_line(line: NumberedLine):
    text = line.text.strip()
    parts = text.rsplit('x', 1)
    if len(parts) < 2:
        return None
    if not is_numeric(parts[1]):
        return None
    if parts[0][-1] != ' ':
        return None
    return Ingredient(name=parts[0][:-1], count=int(parts[1]))

def is_numeric(s: str):
    return all(c in '0123456789' for c in s)

def is_blank_line(line: NumberedLine):
    return line.text.strip() == ''

def is_separator_line(line: NumberedLine):
    return line.text.startswith('=')

# ------------------------------------------------------

def warn(*args, **kw):
    print(f'{PROG}:', *args, file=sys.stderr, **kw)

def die(*args, code=1):
    warn('Fatal:', *args)
    sys.exit(code)

# ------------------------------------------------------

if __name__ == '__main__':
    main()
