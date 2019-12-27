# -*- coding: utf-8 -*-

from .node import CartNode
import re


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
        self.root.print_tree_recursively(print_list)
        return ''.join(print_list)
