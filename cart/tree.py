# -*- coding: utf-8 -*-

from .node import CartNode


class CartTree(object):

    def __init__(self, records):
        """
        Args:
            records: Any sequence of records
        """

        self.root = CartNode(records)
        self.root.split_recursively()

    def classify(self, record: tuple):
        """Classify the record."""

        return self.root.classify(record)

    def __repr__(self):
        """Use TreeNode.print_tree_recursively."""

        print_list = list()
        self.root.print_tree_recursively(print_list)
        return ''.join(print_list)
