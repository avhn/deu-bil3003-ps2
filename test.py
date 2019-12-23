#!python3.8
# -*- coding: utf-8 -*-

import unittest

from cart import utils
from cart import parse
from cart import node


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


class NodeTests(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
