#!python3.8
# -*- coding: utf-8 -*-

import os
import random

from cart import parse
from cart import utils
from cart.tree import CartTree


def main():
    train_set = parse.parse_set('train_set.csv')
    decision_tree = CartTree(train_set)
    prune_set = train_set
    # comment out below line to test the impact of pruning
    decision_tree.post_prune(prune_set)
    print(f"# Decision Tree #{os.linesep}" +
          f"{decision_tree.formatted_repr(header_file='train_set.csv')}")
    test_result = utils.test_classifier(decision_tree, 'test_set.csv')
    printable_test_result = utils.format_test_classifier_result(test_result)
    print(printable_test_result)


if __name__ == "__main__":
    main()
