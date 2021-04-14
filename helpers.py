"""This module contains helper functions used across other modules."""
import string

PUNCTUATIONS = string.punctuation + '–”“'

def clean_up_words(words: list) -> list:
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
