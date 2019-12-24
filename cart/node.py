# -*- coding: utf-8 -*-

import os


class CartNode(object):
    """Binary split node."""

    def __init__(self, t: set):
        """
        Args:
            t: records this node encapsulates
        """

        if not t:
            raise ValueError("Subset isn't valid.")

        self.t = t
        self.value = None
        self.left, self.right = None, None

    def set_branches(self, left=None, right=None, /):
        """
        Set this node as subtree.

        Args:
            Takes 2 positional(!) arguments to set as leafs.
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

        return ((self.left or self.right) is None) is not (self.value is None)

    def split(self):
        pass

    def split_recursively(self):
        pass

    def __repr__(self):
        return f"len(t): {len(self.t)}, value: {self.value}" + os.linesep + \
               f"left: {True if self.left else self.left}" + os.linesep + \
               f"right: {True if self.right else self.right}"
