# -*- coding: utf-8 -*-

from collections import defaultdict
from itertools import chain
from itertools import combinations
import math


def is_convertible(val: str):
    """Test if string is convertible to a number."""

    split = [s.isnumeric() for s in val.split('.')]
    return 0 < len(split) < 3 and False not in split


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


def generate_splits_numbered(column: int, records):
    distinct = set()
    for record in records:
        distinct.add(float(record[column]))
    sorted_distinct = list(distinct)
    sorted_distinct.sort()
    for split_point in sorted_distinct:
        yield split_point
        # yield lambda l: l <= split_point, lambda r: split_point < r


def generate_splits_string(column: int, records):
    distinct = set()
    for record in records:
        distinct.add(str(record[column]))

    duplicates = set()
    print(distinct)
    max_len_combination = math.ceil(len(distinct) / 2)
    for left_branch in chain([combinations(distinct, l) for l in range(1, max_len_combination)]):
        # use frozenset to be able to hash sets to detect duplicates
        left_branch = frozenset(left_branch)
        right_branch = frozenset(distinct.difference(left_branch))
        duplicates.add(right_branch)
        duplicates.add(left_branch)
        if left_branch not in duplicates:
            yield left_branch, right_branch


def generate_splits(records):
    pass
