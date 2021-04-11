import string

PUNCTUATIONS = string.punctuation + '–”“'

class _Trie_Node:
    """A Trie Node.

    Instance Attributes:
        - letter: The letter this Trie Node corresponds to.
        - childred: A dictionary which denotes the children of the Trie Node. 
        It stores letter and its corresponding Trie Node as a key-value.
        - is_word: A bool indicating whether a word is formed at the Trie Node.
    """
    def __init__(self, letter: str = None) -> None:
        """Initializes an Trie Node.

        """
        self.letter = letter  # this is not strictly needed; may remove due to space constraints
        self.children = {}
        self.is_word = False

    def _all_words_helper(self, string_so_far: str = "") -> list:
        """Returns a list of strings.

        Each string is a concatenation of string_so_far and a string whose last letter 
        is the end of word.
        """
        words_so_far = []

        if self.is_word:
            words_so_far.append(string_so_far)

        for child, child_node in self.children.items():
            words_from_child = child_node._all_words_helper(string_so_far + child)
            words_so_far.extend(words_from_child)

        return words_so_far

class Trie:
    """A Trie."""
    def __init__(self) -> None:
        """Initializes an empty Trie."""
        self.root = _Trie_Node()  # The root node doesn't correspond to a letter

    def insert(self, word: str) -> None:
        """Inserts a word in the Trie."""
        word = word.lower()
        curr_node = self.root
        for i in range(len(word)):
            letter = word[i]

            if letter not in curr_node.children:
                curr_node.children[letter] = _Trie_Node(letter)
            curr_node = curr_node.children[letter]

            if i == len(word) - 1:
                curr_node.is_word = True

    def lookup_word(self, _string: str) -> bool:
        """Returns whether the string is a word in the Trie."""
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
        """Returns all the words in the Trie."""
        return self.root._all_words_helper()
    
    def autocomplete_from_prefix(self, prefix: str) -> str:
        """Returns a word inserted in the trie from the given prefix."""
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
            


# Helper methds relating to Trie
def make_trie(words: list) -> Trie:
    """Returns a Trie with all the words in the list words inserted."""
    trie = Trie()
    for word in words:
        trie.insert(word)
    return trie


def make_trie_from_file(filename: str) -> Trie:
    """Returns a Trie with all the words in the file specified, inserted."""
    with open(filename, "r", encoding='utf-8', errors='ignore') as f:
        text = f.read()
        words = text.split()
        new_words = _clean_up_words(words)
    return make_trie(new_words)


def _clean_up_words(words: list) -> list:
    """Returns a list of words after filtering the list words.
    Words that are solely numbers and/or punctuations are filtered out.
    """
    new_words = []
    for word in words:
        if all(l in PUNCTUATIONS or l.isnumeric() for l in word):
            pass
        else:  # you could technically do it without pass, but it seems clearer to me like this.
            if word[-2:] == "'s":  # removes the possessive 's
                word = word[:-2]
            new_word = word.strip(PUNCTUATIONS)  # note hypenated words are allowed
            new_words.append(new_word)
    return new_words
