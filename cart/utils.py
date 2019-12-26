# -*- coding: utf-8 -*-

from collections import defaultdict


def is_convertible(val: str):
    return False not in [s.isnumeric() for s in val.split('.')]


def normalize(val: str):
    """Normalize a string value."""

    val = val.replace("'", "")
    return (val.isdecimal() and int(val) or float(val)) if is_convertible(val) else val


def gini_index(records):
    """
    Calculate gini index of a single dataset.

    Args:
        records: Any iterable
    Returns:
        Floating value between 0 and 1.
    """

    # count occurrences
    counts = defaultdict(lambda: 0)
    for r in records:
        counts[r[-1]] += 1
    # calculate
    result = 1
    for count in counts.values():
        result -= (count / len(records)) ** 2
    return result
