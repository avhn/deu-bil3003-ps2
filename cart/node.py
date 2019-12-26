# -*- coding: utf-8 -*-

import os


class CartNode(object):
    """
    Binary split node.

    Decision is made by checking decision function, if result is true decision
    making continues from the left branch, and if false continues from the
    right branch. Leaf represented with a node with value, subtree represented
    with left and right attributes. If has value, doesn't have branches and vice versa.
    """

    def __init__(self, records: set):
        """
        Args:
            records: records this node encapsulates
        """

        if not records:
            raise ValueError("Subset isn't valid.")

        self.records = records
        self.value = None
        self.decision_function = None
        self.left, self.right = None, None

    def set_branches(self, left=None, right=None):
        """
        Set this node as subtree.

        Args:
            Arguments should be instance of Node, this class.
        """

        self.left, self.right = left, right
        self.value = None

    def set_as_leaf(self, value):
        """Set this node as a leaf."""

        self.left, self.right = None, None
        self.value = value

    def is_leaf(self):
        """Return corresponding boolean indicator."""

        return not (self.left or self.right)

    def is_node_valid(self):
        """Determine if node is valid."""

        return ((self.left or self.right or self.decision_function) is None) \
            is not (self.value is None)

    def set_decision_function(self, function):
        """Set decision function."""

        self.decision_function = function

    def decide(self, record: tuple):
        """Decide crawling through child nodes."""
        assert self.is_node_valid()
        if self.is_leaf():
            return self.value
        return self.left.decide(record) if self.decision_function(record) \
            else self.right.decide(record)

    def split(self):
        pass

    def __repr__(self):
        return f"len(t): {len(self.records)}, value: {self.value}" + os.linesep + \
               f"left: {True if self.left else self.left}" + os.linesep + \
               f"right: {True if self.right else self.right}"
