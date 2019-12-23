# -*- coding: utf-8 -*-


class CartNode(object):
    """Binary split node."""

    def __init__(self, t: set):
        """
        Args:
            t: records this node encapsulates
        """

        self.t = t
        self.value = None
        self.left, self.right = None, None

    def set_leafs(self, left=None, right=None, /):
        """
        Set this node as subtree.

        Args:
            Takes 2 positional(!) arguments to set as leafs.
            Arguments should be instance of Node, this class.
        """

        self.left, self.right, self.value = left, right
        self.value = None

    def set_as_value(self, value):
        """Set this node as a leaf."""

        self.left, self.right = None, None
        self.value = value

    def is_node_valid(self):
        """Return if node is valid."""

        return self.right is None and self.left is None \
               != self.value is None

    def is_leaf(self):
        """Return corresponding boolean indicator."""

        if not self.is_node_valid():
            raise ValueError("Node is just initialized or leaf pointers and value aren't compatible.")
        return not (self.left or self.right)

    def split(self):
        pass

    def split_recursively(self):
        pass
