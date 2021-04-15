"""Autocorrect, BKTree

This module contains the BKTree class, a data structure (a tree) for implementing autocorrection.

Copyright (c) 2021 Akshat Naik and Tony (Juntao) Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""
from backend import Backend
from helpers import clean_up_words, levenshtein, tol


class _BKNode:
    """A node in a Burkhard Keller Tree.

    Instance Attributes:
        - word: the word that this node represents
        - children: the children of this node

    Each edge is associated with an integer represeting the levenshtein distance between the
    parent and child.
    """

    word: str
    children: dict[int, '_BKNode']

    def __init__(self, word: str) -> None:
        self.word = word
        self.children = {}

    def similar_words(self, word: str, tolerance: int) -> list[str]:
        """Return a list of words with levenshtein distance <= tolerance from self.word.

        This function uses DFS.
        """
        lst = []
        dist = levenshtein(self.word, word)

        if dist <= tolerance:
            lst.append(self.word)

        for child_dist, child in self.children.items():
            if dist - tolerance <= child_dist <= dist + tolerance:
                sub_lst = child.similar_words(word, tolerance)
                lst.extend(sub_lst)

        return lst

    def similar_words_ordered(self, word: str, tolerance: int) -> list[str]:
        """Return a list of words with levenshtein distance <= tolerance from self.word,
        in ascending order of their lv distance.
        """
        lst = self._similar_helper(word, tolerance)
        lst.sort(key=lambda each: each[1])
        return [each[0] for each in lst]

    def _similar_helper(self, word: str, tolerance: int) -> list[tuple[str, int]]:
        """Helper for similar_words_ordered, returning tuples of (word, distance)."""
        lst = []
        dist = levenshtein(self.word, word)

        if dist <= tolerance:
            lst.append((self.word, dist))

        for child_dist, child in self.children.items():
            if dist - tolerance <= child_dist <= dist + tolerance:
                sub_lst = child._similar_helper(word, tolerance)
                lst.extend(sub_lst)

        return lst


class BKTree(Backend):
    """An implementation of the Burkhard Keller Tree data structure, which is a tree used for
    implementing autocorrection.

    Instance Attributes:
        - root: the root of this BKTree

    In this implementation, an empty BKTree is impossible. A BKTree instance must contain at least
    one word, the root.
    """
    root: _BKNode

    def __init__(self, root_word: str) -> None:
        self.root = _BKNode(root_word)

    def insert(self, word: str) -> None:
        """Insert a word into the BKTree."""
        # be sensible, we don't need an empty word
        if word == "":
            return
        curr = self.root
        dist = levenshtein(curr.word, word)

        # if there is collision
        while dist in curr.children:
            curr = curr.children[dist]
            dist = levenshtein(curr.word, word)

        # no node can have a child with distance 0
        # so this means the word already exists in the tree
        if dist == 0:
            return

        curr.children[dist] = _BKNode(word)

    def get_similar_words(self, word: str, tolerance: int = 2) -> list[str]:
        """Return a list of words with editing distance <= tolerance from the root."""
        return self.root.similar_words(word, tolerance)

    def get_similar_words_ordered(self, word: str, tolerance: int = 2) -> list[str]:
        """Return a list of words with editing distance <= tolerance from the root
        in ascending order of their lv distance.
        """
        return self.root.similar_words_ordered(word, tolerance)

    def get_suggestions(self, word: str, lim: int = 3) -> list[str]:
        """Implementation of the abstract method from the Backend interface."""
        results = self.get_similar_words_ordered(word, tol(word))
        return results[:lim]


def make_bktree(words: list[str]) -> BKTree:
    """Make a BKTree from a list of words.

    Preconditions:
        - len(words) != 0
    """
    tree = BKTree(words[0])

    for each in words[1:]:
        tree.insert(each)

    return tree


def make_bktree_from_file(filename: str) -> BKTree:
    """Make a BKTree from a file."""
    with open(filename, "r", encoding='utf-8', errors='ignore') as f:
        text = f.read()
        words = text.split()
        new_words = clean_up_words(words)

    return make_bktree(new_words)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(
        config={
            "extra-imports": ['backend', 'helpers'],
            "allowed-io": ['make_bktree_from_file'],
            "max-line-length": 100,
            "disable": ["E1136"],
        }
    )

    # uncomment the following for a demo

    # a = make_bktree_from_file('dictionary.txt')
    # print(a.get_similar_words_ordered('teh', 3)[:3])
