"""Functions specific to factorio pyanodons mods."""

import re


def add_numeral_preserve_leading_zeroes(s: str, increment: int):
    """Example: s="01" increment=1 -> return "02"."""
    length = len(s)
    old_num = int(s)
    num = old_num + increment
    if num < 0:
        return None
    return str(num).zfill(length)


def guess_upgraded_name(name: str) -> str:
    m = re.search(r'(\D+)(\d+)', name)
    if m:
        suffix = add_numeral_preserve_leading_zeroes(m.group(2), 1)
        return m.group(1) + suffix if suffix is not None else None
    # Some mk01 recipes are missing the -mk01 prefix
    return name + '-mk02'


def guess_downgraded_name(name: str) -> str:
    m = re.search(r'(\D+)(\d+)', name)
    if m:
        suffix = add_numeral_preserve_leading_zeroes(m.group(2), -1)
        return m.group(1) + suffix if suffix is not None else None
