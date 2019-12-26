#!python3.8
# -*- coding: utf-8 -*-

import unittest
import random

from cart import utils
from cart import parse
from cart.node import CartNode
from cart.tree import CartTree


class ParseTests(unittest.TestCase):
    files = './train_set.csv', './test_set.csv'

    def test_parse_set(self):
        for file_path in self.files:
            d = parse.parse_set(file_path)
            assert d and len(d) > 1 and len(d.pop()) > 1


class UtilTests(unittest.TestCase):
    string_float = '0.34243'
    string_int = '12341234'
    string = '123abc.456def'
    dataset = None

    @staticmethod
    def get_instance_row(row: tuple, instance_classes: tuple):
        """Helper method. Find the corresponding row."""

        for c in range(len(row)):
            if isinstance(row[c], instance_classes):
                return c

    def get_dataset(self):
        """Helper method which caches."""

        if not self.dataset:
            self.dataset = tuple(parse.parse_set())
        return self.dataset

    def test_is_convertible(self):
        assert not utils.is_convertible(self.string)
        assert utils.is_convertible(self.string_float)
        assert utils.is_convertible(self.string_int)

    def test_normalize(self):
        assert isinstance(utils.normalize(self.string_int), int)
        assert isinstance(utils.normalize(self.string_float), float)
        assert isinstance(utils.normalize(self.string), str)

    def test_gini_index(self):
        dataset = parse.parse_set()
        index = utils.gini_index(dataset)
        assert index and isinstance(index, float)
        assert 0 <= index <= 0.5

    def test_generate_splits_string(self):
        dataset = self.get_dataset()
        column = self.get_instance_row(dataset[0], (str, ))
        for function in utils.generate_splits_string(column, dataset):
            function(random.choice(dataset))
            return True
        raise ValueError("Empty generator.")

    def test_generate_splits_number(self):
        dataset = self.get_dataset()
        column = self.get_instance_row(dataset[0], (int, float))
        for function in utils.generate_splits_number(column, dataset):
            function(random.choice(dataset))
            return True
        raise ValueError("Empty generator.")

    def test_generate_splits(self):
        dataset = self.get_dataset()
        dataset = dataset[:len(dataset) // 10]
        function = None
        for function in utils.generate_splits(dataset):
            function(random.choice(dataset))
        assert function

    def test_gini_index_split(self):
        dataset = self.get_dataset()
        for decision_function in utils.generate_splits(dataset):
            gini_index, left_set, right_set = utils.gini_index_split(decision_function, dataset)
            assert gini_index and 0 <= gini_index <= 1
            assert left_set and right_set
            return True
        raise ValueError("Empty generator.")

    def test_best_split(self):
        dataset = self.get_dataset()
        gini_index, left_set, right_set, decision_function \
            = utils.best_split(dataset)
        assert decision_function(random.sample(left_set, 1)[0]) is not None
        assert decision_function(random.sample(right_set, 1)[0]) is not None
        assert 0 <= gini_index <= 1


class CartNodeTests(unittest.TestCase):
    D = list(parse.parse_set())

    def test_init(self):
        """Also returns the node created."""

        sample_set = random.sample(CartNodeTests.D, len(CartNodeTests.D) // 3)
        node = CartNode(sample_set)
        assert node.left is None and node.right is None
        return node

    def test_set_branches(self):
        """Also returns the node created."""

        node = self.test_init()
        node_right = self.test_init()
        node.set_branches(None, node_right)
        assert node.left is None and node.right is node_right
        return node

    def test_set_as_leaf(self):
        """Also returns the node created."""

        node = self.test_set_branches()
        # node is subtree
        value = 'test value'
        node.set_as_leaf(value)
        # node is value node
        assert node.value is value
        assert node.left is None and node.right is None
        return node

    def test_is_leaf(self):
        assert not self.test_set_branches().is_leaf()
        assert self.test_set_as_leaf().is_leaf()

    def test_is_node_valid(self):
        empty_node = self.test_init()
        assert not empty_node.is_node_valid()
        node = self.test_set_branches()
        assert node.is_node_valid()
        node.value = 'some val'
        assert not node.is_node_valid()

    def test_split(self):
        node = self.test_init()
        assert not node.is_node_valid()
        node.split()
        assert node.is_node_valid()
        tag = random.sample(node.records, 1)[0][-1]
        dataset = parse.parse_set()
        pure_node = CartNode([record for record in random.sample(dataset, len(dataset) // 3)
                              if record[-1] == tag])
        pure_node.split()
        assert pure_node.is_leaf()

    def test_split_recursively(self):
        """Also returns the node created."""

        node = self.test_init()
        node.split_recursively()
        assert node.is_node_valid()
        assert node.left.is_node_valid() and node.right.is_node_valid()
        # crawl through and test at CartTree tests
        return node

    def test_decide(self):
        node = self.test_split_recursively()
        dataset = parse.parse_set('test_set.csv')
        record = random.sample(dataset, 1)[0]
        result = node.decide(record)
        assert result
        assert isinstance(result, str)


class CartTreeTests(unittest.TestCase):

    def test_init(self):
        pass

if __name__ == '__main__':
    unittest.main()
