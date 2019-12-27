# -*- coding: utf-8 -*-

from collections import defaultdict
from itertools import chain
from itertools import combinations
import os
import random

from . import parse


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
        Corresponding lambda function, description of the function
    """

    if column == len(random.sample(records, 1)[0]):
        raise ValueError("Invalid index.")

    distinct = set()
    for record in records:
        distinct.add(str(record[column]))
    antecedents = [combinations(distinct, l) for l in range(1, len(distinct))]
    for left_branch in chain.from_iterable(antecedents):
        left_branch = frozenset(left_branch)
        yield lambda r: r[column] in left_branch, \
            f"{column + 1}. column in {{{', '.join([element for element in left_branch])}}}"


def generate_splits_number(column: int, records):
    """
    Generate decision functions from a number column.

    Args:
        column: Corresponding index
        records: Any sequence of record tuples
    Yields:
        Corresponding lambda function, description of the function
    """

    if column == len(random.sample(records, 1)[0]):
        raise ValueError("Invalid index.")

    distinct = set()
    for record in records:
        distinct.add(float(record[column]))
    sorted_distinct = list(distinct)
    sorted_distinct.sort()
    for split_point in sorted_distinct:
        yield lambda r: r[column] <= split_point, f"{column + 1}. column <= {split_point}"


def generate_splits(records, class_tag_included=True):
    """
    Generate all possible decision functions from the records.

    Args:
        records: Any sequence of record tuples
        class_tag_included: Class tag at the index -1
    Yields:
        All decision functions for the records, description of the function
    """

    record = random.sample(records, 1)[0]
    for column in range(0, len(record) - (1 if class_tag_included else 0)):
        generator = generate_splits_string if isinstance(record[column], str) \
            else generate_splits_number
        for decision_function, description in generator(column, records):
            yield decision_function, description


def gini_index_split(decision_function, records):
    """
    Calculate gini indexes and record sets of the split branches.

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
            decision function, description)
    """

    result = None
    for decision_function, description in generate_splits(records):
        (left_gini, left_set), (right_gini, right_set) = \
            gini_index_split(decision_function, records)
        # weight impurities with the size of the sets
        left_weight = len(left_set) / len(records)
        gain = impurity - left_weight * left_gini - (1 - left_weight) * right_gini
        if 0 < gain and (not result or result[0] < gain):
            result = gain, left_set, right_set, decision_function, description
    return result


def test_classifier(classifier, test_set_file='test_set.csv', positive='good'):
    """
    * Problem set specific. Only for binary class data sets.
    Test classifier object's accuracy.

    Args:
        classifier: And classifier object with the method "classify(self, record)"
        test_set_file: location of the csv file, the test set
        positive: Positive tag
    Returns:
        Sequence representing test result as below:
            (Accuracy, TP rate, TN rate, TP count, TN count)
        If not enough test data, returns None.
    """

    test_set = parse.parse_set(test_set_file)
    counts = [[0, 0], [0, 0]]  # [[TP count, FP count], [TN count, FN count]]
    for record in test_set:
        result = classifier.classify(record)
        if result == positive:
            if result == record[-1]:
                counts[0][0] += 1
            else:
                counts[0][1] += 1
        else:
            if result == record[-1]:
                counts[1][0] += 1
            else:
                counts[1][1] += 1

    try:
        return (counts[0][0] + counts[1][0]) / len(test_set), counts[0][0] / sum(counts[0]), \
            counts[1][0] / sum(counts[1]), counts[0][0], counts[1][0]
    except ZeroDivisionError:
        return None


def format_test_classifier_result(result):
    """Format output of test_classifier."""

    if not result:
        return "Not enough test data."

    return f"# Test Result #" + \
           f"{os.linesep}Accuracy: {result[0]}" + \
           f"{os.linesep}TP rate: {result[1]}" + \
           f"{os.linesep}TN rate: {result[2]}" + \
           f"{os.linesep}TP count: {result[3]}" + \
           f"{os.linesep}TN count: {result[4]}{os.linesep}"
