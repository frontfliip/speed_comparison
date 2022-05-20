"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from math import log
from random import choice
import time
import sys
sys.setrecursionlimit(100000)

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            sig = ""
            if node != None:
                sig += recurse(node.right, level + 1)
                sig += "| " * level
                sig += str(node.data) + "\n"
                sig += recurse(node.left, level + 1)
            return sig

        return recurse(self._root, 0)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return lyst

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top.left is None and top.right is None:
                return 0
            if top.left is not None:
                left_sum = height1(top.left)
            else:
                left_sum = -1
            if top.right is not None:
                right_sum = height1(top.right)
            else:
                right_sum = -1
            return max(left_sum, right_sum) + 1

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2 * log(int(len(self.inorder())) + 1, 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        elements = self.inorder()
        for i in range(len(elements)):
            if elements[i] == low:
                elements = elements[i:]
                break
        for j in range(len(elements)):
            if elements[j] == high:
                elements = elements[:j+1]
                break
        return elements

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        elements = self.inorder()

        def rebalance1(elements):
            if len(elements) == 0:
                return None
            i = len(elements) // 2

            node = BSTNode(elements[i])

            node.left = rebalance1(elements[:i])
            node.right = rebalance1(elements[i + 1 :])

            return node

        self._root = rebalance1(elements)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        elements = self.inorder()
        for i in range(len(elements)):
            if elements[i] == item:
                try:
                    return elements[i+1]
                except IndexError:
                    return None
    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        elements = self.inorder()
        prev_elem = None
        for elem in elements:
            if elem == item:
                return prev_elem
            prev_elem = elem

    def list_speed_check(self, rand_words, all_words):
        begin_time = time.time()
        for word in rand_words:
            for word_checker in all_words:
                if word_checker == word:
                    break
        return time.time() - begin_time

    def bst_default_speed(self, rand_words, all_words):
        bst = LinkedBST()
        for word in all_words:
            bst.add(word)
        begin_time = time.time()
        for word in rand_words:
            bst.find(word)
        return time.time() - begin_time

    def bst_nonsorted_speed(self, rand_words, all_words):
        bst = LinkedBST()
        for word in all_words:
            to_add = choice(all_words)
            bst.add(to_add)
            all_words.remove(to_add)
        begin_time = time.time()
        for word in rand_words:
            bst.find(word)
        return time.time() - begin_time
    def bst_rebalanced_speed(self, rand_words, all_words):
        bst = LinkedBST()
        for word in all_words:
            bst.add(word)
        bst.rebalance()
        begin_time = time.time()
        for word in rand_words:
            bst.find(word)
        return time.time() - begin_time

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path) as f:
            lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].replace("\n", "")
        rand_words = []
        for _ in range(1000):
            rand_words.append(choice(lines))
        list_time =  self.list_speed_check(rand_words, lines)
        bst_default_time = self.bst_default_speed(rand_words, lines)
        bst_nonsorted_time = self.bst_nonsorted_speed(rand_words, lines)
        bst_rebalanced_time = self.bst_rebalanced_speed(rand_words, lines)
        print("\n")
        print("The time for finding 1000 words in around 25000 words(otherwise it is not enough memory)")
        print("\n")
        print(f"Time with list: {list_time} sec")
        print(f"Time with alphabet bst: {bst_default_time} sec")
        print(f"Time with random bst: {bst_nonsorted_time} sec")
        print(f"Time with rebalanced bst: { bst_rebalanced_time} sec")
        print("\n")
        print("As we can see the best time is using rebalanced bst and the worst is with alphabet bst(because the time to find elem is maximum here)")

if __name__ == '__main__':
    bst = LinkedBST()
    bst.demo_bst("check.txt")