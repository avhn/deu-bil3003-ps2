#!python3.8
# -*- coding: utf-8 -*-

import unittest
import random

from cart import utils
from cart import parse
from cart.node import CartNode


class UtilTests(unittest.TestCase):
    string_float = '0.34243'
    string_int = '12341234'
    string = '234asdf.2340sdfs'

    def test_normalize(self):
        assert isinstance(utils.normalize(self.string_int), int)
        assert isinstance(utils.normalize(self.string_float), float)
        assert isinstance(utils.normalize(self.string), str)


class ParseTests(unittest.TestCase):
    files = './train_set.csv', './test_set.csv'

    def test_parse_set(self):
        for file_path in self.files:
            D = parse.parse_set(file_path)
            assert D and len(D) > 1 and len(D.pop()) > 1


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
        assert node.value and node.value is value
        assert node.left is None and node.right is None
        return node

    def test_is_leaf(self):
        assert self.test_set_branches().is_leaf() is False
        assert self.test_set_as_leaf().is_leaf()

    def test_is_node_valid(self):
        empty_node = self.test_init()
        assert empty_node.is_node_valid() is False
        node = self.test_set_branches()
        assert node.is_node_valid() is True
        node.value = 'some val'
        assert node.is_node_valid() is False


if __name__ == '__main__':
    unittest.main()
