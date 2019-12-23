# -*- coding: utf-8 -*-

import csv
from . import utils


def parse_set(filepath="train_set.csv"):
    """
    Parse .csv file and try to use int or float when possible.

    Args:
        filepath: Relative path of the .csv data file. File should indicate
            the class as last value at every line.

    Returns:
        All rows as tuples in a set object. Values are normalized.
        Representation:
            set{tuple(v1, ..., class), tuple(v1, ..., class), ...}
    """

    D = set()
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(reader):
            if 0 < i:
                D.add(tuple([utils.normalize(val) for val in row]))
    return D
