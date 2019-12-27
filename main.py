#!python3.8
# -*- coding: utf-8 -*-

from cart import parse
from cart.tree import CartTree

def main():
    train_set = parse.parse_set('train_set.csv')
    test_set = parse.parse_set('test_set.csv')

    decision_tree = CartTree(train_set)
    count = 0
    for record in test_set:
        if record[-1] == decision_tree.decide(record):
            count += 1

    print(f"{count / len(test_set)} accuracy.")


if __name__ == "__main__":
    main()
