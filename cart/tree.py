# -*- coding: utf-8 -*-


class Node(object):
    """
    Binary split node.
    """

    def __init__(self, t: set):
        """
        Args:
            t: records this node encapsulates.

        """
        self.t = t
        self.left, self.right = None, None

    def set_leafs(self, left=None, right=None, /):
        """
        Args:
            Takes 2 positional(!) arguments to set as leafs.
            Arguments should be instance of Node, this class.
        """

        self.left, self.right = left, right


class ClassificationTree(object):
    """

    """

    pass
