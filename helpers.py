"""This module contains helper functions used across other modules."""
import string

PUNCTUATIONS = string.punctuation + '–”“'

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
