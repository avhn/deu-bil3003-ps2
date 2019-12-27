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

    def decide(self, record: tuple):
        """Classify the record."""

        return self.root.decide(record)

    def __repr__(self):
        return self.root.__repr__()
