#!python3.8
# -*- coding: utf-8 -*-

from cart import parse
from cart import utils
from cart.tree import CartTree


def main():
    import random
    train_set = parse.parse_set('train_set.csv')
    decision_tree = CartTree(train_set)
    result = utils.test_classifier(decision_tree)
    printable_test_result = utils.format_test_result(result)
    print(printable_test_result)
    print("# Decision Tree #")
    print(decision_tree)

if __name__ == "__main__":
    main()
