"""Autocorrect, Trie

This module contains a standard implementation of the Trie data structure.

Copyright (c) 2021 Akshat Naik and Tony (Juntao) Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""
from collections import deque
from typing import Optional

from helpers import clean_up_words


class _TrieNode:
    """A Trie Node.

    Instance Attributes:
        - letter: The letter this Trie Node corresponds to.
        - children: A dictionary which denotes the children of the Trie Node.
        It stores letter and its corresponding Trie Node as a key-value.
        - is_word: A bool indicating whether a word is formed at the Trie Node.
    """

    letter: Optional[str]
    children: dict[str, '_TrieNode']
    is_word: bool

    def __init__(self, letter: str = None) -> None:
        """Initialize an Trie Node. """
        self.letter = letter  # this is not strictly needed; may remove due to space constraints
        self.children = {}
        self.is_word = False

    def all_words_helper(self, string_so_far: str = "") -> list:
        """Return a list of strings.

        Each string is a concatenation of string_so_far and a string whose last letter
        is the end of word.
        """
        words_so_far = []

        if self.is_word:
            words_so_far.append(string_so_far)

        for child, child_node in self.children.items():
            words_from_child = child_node.all_words_helper(string_so_far + child)
            words_so_far.extend(words_from_child)

        return words_so_far


class Trie:
    """A Trie.

    Instance Attributes:
        - root: the root of the trie

    The root does NOT correspond to a letter.
    """

    root: _TrieNode

    def __init__(self) -> None:
        """Initialize an empty Trie."""
        self.root = _TrieNode()  # The root node doesn't correspond to a letter

    def insert(self, word: str) -> None:
        """Insert a word into the Trie."""
        word = word.lower()
        curr_node = self.root
        for i in range(len(word)):
            letter = word[i]

            if letter not in curr_node.children:
                curr_node.children[letter] = _TrieNode(letter)
            curr_node = curr_node.children[letter]

            if i == len(word) - 1:
                curr_node.is_word = True

    def lookup_word(self, _string: str) -> bool:
        """Return whether the string is a word in the Trie."""
        _string = _string.lower()
        curr_node = self.root
        for i in range(len(_string)):
            letter = _string[i]

            if letter not in curr_node.children:
                return False
            else:
                curr_node = curr_node.children[letter]

        return curr_node.is_word

    def all_words(self) -> list:
        """Return all the words in the Trie."""
        return self.root.all_words_helper()

    def complete_from_prefix(self, prefix: str) -> str:
        """Return a word in the trie from the given prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return ""
            node = node.children[char]

        suffix = ""
        while not node.is_word:
            children = list(node.children.keys())
            if len(children) == 0:
                return ""
            node = node.children[children[0]]
            suffix += node.letter
        return prefix + suffix

    def get_suggestions(self, word: str, lim: int = 3) -> list[str]:
        """Return a maximum of 'lim' words which start with given prefix.

        This function uses BFS to get the closest words to prefix.
        """
        # first try to reach the node containing the last letter of word
        node = self.root
        for char in word:
            if char not in node.children:
                return []
            node = node.children[char]

        sug = []
        queue = deque()
        queue.append(('', node))

        while queue and len(sug) < lim:
            suf, node = queue.popleft()
            if node.is_word:
                sug.append(word + suf)
            for each in node.children:
                queue.append((suf + each, node.children[each]))

        return sug


# Helper methds relating to Trie
def make_trie(words: list) -> Trie:
    """Return a Trie with all the words in the list words inserted."""
    trie = Trie()
    for word in words:
        trie.insert(word)
    return trie


def make_trie_from_file(filename: str) -> Trie:
    """Return a Trie with all the words in the file specified, inserted."""
    with open(filename, "r", encoding='utf-8', errors='ignore') as f:
        text = f.read()
        words = text.split()
        new_words = clean_up_words(words)
    return make_trie(new_words)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # the followning code causes an error
    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(
        config={
            "extra-imports": ['helpers', 'collections'],
            "allowed-io": ['make_trie_from_file'],
            "max-line-length": 100,
            "disable": ["E1136"],
        }
    )

    # uncomment the following for a demo

    # a = make_trie_from_file('dictionary.txt')
    # print(a.get_suggestions('hel', 3))
