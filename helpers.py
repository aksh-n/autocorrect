"""Autocorrect, Helpers

This module contains helper functions used across other modules.

Copyright (c) 2021 Akshat Naik and Tony (Juntao) Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""
import string


def clean_up_words(words: list) -> list:
    """Returns a list of words after filtering the list words.
    Words that are solely numbers and/or punctuations are filtered out.
    """
    PUNCTUATIONS = string.punctuation + '–”“'

    new_words = []
    for word in words:
        if all(letr in PUNCTUATIONS or letr.isnumeric() for letr in word):
            pass
        else:  # you could technically do it without pass, but it seems clearer to me like this.
            if word[-2:] == "'s":  # removes the possessive 's
                word = word[:-2]
            new_word = word.strip(PUNCTUATIONS)  # note hypenated words are allowed
            new_words.append(new_word)
    return new_words


def levenshtein(s1: str, s2: str) -> int:
    """Returns the minimum edit distance between strings s1 and s2.
    This function implements the Levenshtein distance algorithm using Dynamic Programming.
    """
    dp = list(range(0, len(s2) + 1))  # dp stands for dynamic programming
    # technically, I can reduce len(dp) to min(len(s1), len(s2)), but its not necessary.

    for i in range(len(s1)):
        for d in range(len(dp) - 1, 0, -1):
            j = d - 1
            dp[d] = min(dp[d] + 1, dp[d - 1] + (s1[i] != s2[j]))
        dp[0] = i + 1
        for d in range(1, len(dp)):
            dp[d] = min(dp[d], dp[d - 1] + 1)
        # print(dp)
    return dp[-1]


def tol(word: str) -> int:
    """Return the tolerance (max number of edits) accepted for the specific word
    based on its length.
    """
    return min(3, max(len(word) // 2, 1))


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['string'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
