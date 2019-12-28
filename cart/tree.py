# -*- coding: utf-8 -*-

from .utils import classification_error_rate
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

    def post_prune(self, prune_set):
        """Prune the tree with prune set using Reduced Error Pruning method."""

        self.post_prune_recursively(self.root, prune_set)

    def post_prune_recursively(self, node, prune_set):
        """
        Prune tree with Reduced Error Pruning method.

        Args:
            node: Subtree
            prune_set: Sequence of records with class tag at index -1
        """

        if node.is_leaf():
            return
        # recurse till leafs
        self.post_prune_recursively(node.left, prune_set)
        self.post_prune_recursively(node.right, prune_set)
        # prune if beneficial
        node.left.prune_if_necessary(self, prune_set)
        node.right.prune_if_necessary(self, prune_set)

    def formatted_repr(self, header_file=None):
        """
        Optionally format __repr__ output.

        Args:
            header_file: format representation replacing
                '*. column' substrings with the corresponding header.
        Returns:
            Formatted __repr__ output if header_file passed.
            Else standard __repr__ output.
        """

        output = self.__repr__()
        if header_file:  # replace '*. column' with header tag
            headers = None
            with open(header_file) as file:
                headers = file.readline().strip().split(',')
            output = output.split('. column')
            for i in range(len(output) - 1):  # exclude last one
                index_len = 1
                while output[i][-index_len - 1] != '(':
                    index_len += 1
                output[i] = output[i][:-index_len] + headers[int(output[i][-index_len:]) - 1]
            output = ''.join(output)
        return output

    def __repr__(self):
        """Use TreeNode.print_tree_recursively."""

        print_list = list()
        self.root.repr_of_tree_recursively(print_list)
        return ''.join(print_list)
