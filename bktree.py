from lv_distance import levenshtein
from helpers import clean_up_words

class _BKNode:
    """A node in a BK Tree."""
    word: str
    children: dict[int, "_BKNode"]

    def __init__(self, word: str) -> None:
        self.word = word
        self.children = {}

    def similar_words(self, word: str, tolerance: int) -> list[str]:
        """Return a list of words with levenshtein distance <= tolerance from self.word.

        Currently this function is using DFS.
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


class BKTree:
    """An implementation of the BK Tree data structure."""
    root: _BKNode

    def __init__(self, root_word: str) -> None:
        self.root = _BKNode(root_word)

    def insert(self, word: str) -> None:
        """Insert a word."""
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

def make_bktree(words: list[str]) -> BKTree:
    """Make a BKTree from a list of words.

    The argument words should NOT be empty.
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
