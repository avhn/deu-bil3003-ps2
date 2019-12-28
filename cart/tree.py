# -*- coding: utf-8 -*-

import copy
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

    def post_prune(self, prune_set, node=None):
        """
        Prune tree with Reduced Error Pruning method.

        Args:
            prune_set: Sequence of records with class tag at index -1
        """

        if not node:
            node = self.root
        elif node and node.is_leaf():
            return

        def return_test_node(node):
            test_node = copy.copy(node)
            test_node.prune()
            return node, test_node

        if not node.left.is_leaf():
            original_error_rate = classification_error_rate(self, prune_set)
            original_node, test_node = return_test_node(node.left)
            # test new node
            node.left = test_node
            test_error_rate = classification_error_rate(self, prune_set)
            # decide to prune permanently
            node.left = test_node if test_error_rate <= original_error_rate \
                else original_node

        if not node.right.is_leaf():
            original_error_rate = classification_error_rate(self, prune_set)
            original_node, test_node = return_test_node(node.right)
            # test new node
            node.right = test_node
            test_error_rate = classification_error_rate(self, prune_set)
            # decide to prune permanently
            node.right = test_node if test_error_rate <= original_error_rate \
                else original_node

        self.post_prune(prune_set, node.left)
        self.post_prune(prune_set, node.right)

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
