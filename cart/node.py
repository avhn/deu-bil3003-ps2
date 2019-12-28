# -*- coding: utf-8 -*-

from collections import defaultdict
import copy
import os
import random

from . import utils


class CartNode(object):
    """
    Binary split node.

    Decision is made by checking decision function, if result is true decision
    making continues from the left branch, and if false continues from the
    right branch. Leaf represented with a node with value, subtree represented
    with left and right attributes. If has value, doesn't have branches and vice versa.
    """

    def __init__(self, records):
        """
        Args:
            records: Any sequence of records this node encapsulates
        """

        if not records or not isinstance(records, (set, frozenset, tuple, list)):
            raise ValueError("Subset isn't valid.")

        self.records = records
        self.impurity = None
        self.most_frequent_class = None
        self.value = None
        self.decision_function = None
        self.split_info = None
        self.left, self.right = None, None

    def set_branches(self, left=None, right=None):
        """
        Set this node as subtree. Nullifies leaf value if exists.

        Args:
            Arguments should be instance of CartNode, this class.
        """

        self.left, self.right = left, right
        self.value = None

    def set_as_leaf(self, value):
        """Set this node as a leaf. Only effects branches and value."""

        self.left, self.right = None, None
        self.value = value

    def is_leaf(self):
        """Return corresponding boolean indicator. Only looks at branches."""

        return not (self.left or self.right)

    def is_node_valid(self):
        """Determine if node is valid. Checking with branches and value."""

        return ((self.left or self.right) is None) \
            is not (self.value is None)

    def set_decision_function(self, function):
        """Set decision function."""

        self.decision_function = function

    def split(self):
        """Split node or label it as value."""
        # check if pure to label
        self.impurity = utils.gini_index(self.records)
        if self.impurity == 0:
            self.set_as_leaf(random.sample(self.records, 1)[0][-1])
            return self.value
        # split
        _, left_set, right_set, self.decision_function, self.split_info = \
            utils.best_split(self.records, self.impurity)
        self.set_branches(CartNode(left_set), CartNode(right_set))

    def split_recursively(self):
        """Split recursively to construct decision tree."""

        self.split()
        if not self.is_leaf():
            self.left.split_recursively()
            self.right.split_recursively()

    def classify(self, record: tuple):
        """Classify crawling through child nodes."""

        if self.is_leaf():
            return self.value
        return self.left.classify(record) if self.decision_function(record) \
            else self.right.classify(record)

    def get_most_frequent_class(self):
        """Set if most_frequent_class isn't set and return."""

        if not self.most_frequent_class:
            counts = defaultdict(lambda: 0)
            for r in self.records:
                counts[r[-1]] += 1
            tag, count = None, 0
            for k, v in counts.items():
                if count < v:
                    tag, count = k, v
            self.most_frequent_class = tag
        return self.most_frequent_class

    def prune(self):
        """Make a leaf of most frequent class."""

        self.set_as_leaf(self.get_most_frequent_class())

    def prune_if_necessary(self, parent, prune_set):
        """
        If error rate decreases, prune this node.

        Args:
            parent: CartTree or CartNode
            prune_set: Sequence of records with class tag to
                calculate error rates
        """

        if self.is_leaf():
            return
        original_error_rate = utils.classification_error_rate(parent, prune_set)
        temp_left, temp_right = self.left, self.right
        self.prune()
        pruned_error_rate = utils.classification_error_rate(parent, prune_set)
        if not pruned_error_rate <= original_error_rate:
            # not beneficial, undo prune
            self.set_branches(temp_left, temp_right)

    def repr_of_tree_recursively(self, output_list, prefix='', children_prefix=''):
        """Populate output to output_list. Courtesy to Vasili Novikov."""

        output_list.append(prefix)
        output_list.append(f"({self.split_info})" if not self.is_leaf() else self.value)
        output_list.append(os.linesep)
        children = [n for n in (self.left, self.right) if n]
        for i, node in enumerate(children):
            if i == 0:
                node.repr_of_tree_recursively(output_list, children_prefix + "├(T)─ ",
                                              children_prefix + "│     ")
            else:
                node.repr_of_tree_recursively(output_list, children_prefix + "└(F)─ ",
                                              children_prefix + "      ")

    def clone(self):
        """Return shallow copy of self."""

        return copy.copy(self)

    def __repr__(self):
        """Return representation of this subtree, or leaf."""

        print_list = list()
        self.repr_of_tree_recursively(print_list)
        return ''.join(print_list)
