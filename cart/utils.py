# -*- coding: utf-8 -*-

import random
from collections import defaultdict
from itertools import chain
from itertools import combinations


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
        records: Any record sequence
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


def generate_splits_string(column: int, records):
    """
    Generate decision functions from a string column.

    Args:
        column: Corresponding index
        records: Any sequence of record tuples

    Yields:
        Corresponding lambda function.
    """

    if column == len(random.sample(records, 1)[0]):
        raise ValueError("Invalid index.")

    distinct = set()
    for record in records:
        distinct.add(str(record[column]))
    max_antecedent_len = len(distinct) // 2
    antecedents = [combinations(distinct, l) for l in range(1, max_antecedent_len + 1)]
    duplicates = set()
    for left_branch in chain.from_iterable(antecedents):
        # use frozenset to be able to hash sets to detect duplicates
        left_branch = frozenset(left_branch)
        if left_branch not in duplicates:  # no need to check both branches
            yield lambda r: r[column] in left_branch
        if len(left_branch) == max_antecedent_len:
            duplicates.add(frozenset(distinct.difference(left_branch)))


def generate_splits_number(column: int, records):
    """
    Generate decision functions from a number column.

    Args:
        column: Corresponding index
        records: Any sequence of record tuples

    Yields:
        Corresponding lambda function.
    """

    if column == len(random.sample(records, 1)[0]):
        raise ValueError("Invalid index.")

    distinct = set()
    for record in records:
        distinct.add(float(record[column]))
    sorted_distinct = list(distinct)
    sorted_distinct.sort()
    for split_point in sorted_distinct:
        yield lambda r: r[column] <= split_point


def generate_splits(records, class_tag_included=True):
    """
    Generate all possible decision functions from the records.

    Args:
        records: Any sequence of record tuples
        class_tag_included: Class tag at the index -1
    Yields:
        All decision functions for the records.
    """

    record = random.sample(records, 1)[0]

    for column in range(0, len(record) - (1 if class_tag_included else 0)):
        generator = generate_splits_string if isinstance(record[column], str) \
            else generate_splits_number
        for decision_function in generator(column, records):
            yield decision_function


def gini_index_split(decision_function, records):
    """
    Calculate gini index of the split.

    Args:
        decision_function: lambda function for decision
        records: Any sequence of record tuples

    Returns:
        (left gini index, left set), (right gini index, right set)
    """

    left_set, right_set = set(), set()
    for record in records:
        left_set.add(record) if decision_function(record) else right_set.add(record)
    left_gini, right_gini = gini_index(left_set), gini_index(right_set)
    return (left_gini, left_set), (right_gini, right_set)


def best_split(records, impurity: float):
    """
    Find the best split.

    Args:
        records: Any sequence of records
        impurity: Gini index of the passed records
    Returns:
        Best of gini_index_split's output and corresponding decision function.
        Representation:
            (Gain of the split, left branch's record set, right branch's record set,
            decision function)
    """

    result = None
    for decision_function in generate_splits(records):
        (left_gini, left_set), (right_gini, right_set) = \
            gini_index_split(decision_function, records)
        # weight impurities with the length of the sets
        # to calculate more accurate gain values
        left_weight = len(left_set) / len(records)
        gain = impurity - left_weight * left_gini - (1 - left_weight) * right_gini
        if 0 < gain and (not result or result[0] < gain):
            result = gain, left_set, right_set, decision_function
    return result
