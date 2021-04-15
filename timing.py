"""Autocorrect, Timing Experiments

This module contains methods used to perform timing experiments on BKTree
and LevenshteinNFA. It also contains methods to draw graphs to visually represent the results.

Copyright (c) 2021 Akshat Naik and Tony (Juntao) Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""
from timeit import timeit
import random
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from trie import Trie, make_trie_from_file
from levenshtein import LevenshteinNFA
from bktree import BKTree, make_bktree_from_file
from helpers import clean_up_words


def initial_setup() -> tuple[Trie, BKTree]:
    """Return a Trie and BKTree using dictionary.txt."""
    trie = make_trie_from_file("dictionary.txt")
    bktree = make_bktree_from_file("dictionary.txt")
    return trie, bktree


def read_results_from_file() -> list[tuple[int]]:
    """Read the results from time_results.txt."""
    with open("time_results.txt", "r", encoding="utf-8", errors="ignore") as f:
        results = []
        for result in f:
            result = tuple(float(time) for time in result.split(", "))
            results.append(result)
    return results


def write_results_to_file(results: list[tuple[int]]) -> None:
    """Write the results to time_results.txt."""
    with open("time_results.txt", "w", encoding="utf-8", errors="ignore") as f:
        for result in results:
            f.write(str(result[0]) + ", " + str(result[1]) + "\n")
    return None


def plot_time_statistics(results: list[tuple[float, float]]) -> None:
    """Plot the time taken by Levenshtein Automata and BKTree in each timing experiment
    from a given list of results.
    """
    time_lev_nfa = []
    time_bktree = []
    for res in results:
        time_lev_nfa.append(res[0])
        time_bktree.append(res[1])

    fig = make_subplots(rows=1, cols=1)
    name1 = "Average time taken by Levenshtein Automaton"
    fig.add_trace(go.Scatter(y=time_lev_nfa, mode="markers", name=name1))
    name2 = "Average time taken by BKTree"
    fig.add_trace(go.Scatter(y=time_bktree, mode="markers", name=name2))

    fig.update_yaxes(range=[0.0, 0.1])
    fig.update_layout(
        title="Average time taken by Levenshtein Automaton and BKTree to suggest autocorrections,\
            for each misspelled words (in s)"
    )

    fig.show()


def time_multiple(D: int = 2, number: int = 10, n: int = -1) -> list[tuple]:
    """Return a list of n tuples of the runtimes of Levenshtein Automaton and BKTree
    to return suggestions for words similar to each of the randomized queries.
    """
    trie, bktree = initial_setup()
    words = scramble_from_file("dictionary.txt", n)
    res = []
    for word in words:
        res.append(time_one_query(trie, bktree, word, D, number))

    return res


def time_one_query(trie: Trie, bktree: BKTree, query: str, D: int,
                   number: int) -> tuple[float, float]:
    """Return a tuple consisting of the time taken by a Levenshtein Automaton (with a Trie) and
    a BKTree to return suggestions for words similar to query.

    Parameters:
        - trie: a Trie storing words
        - bktree: a BKTree relating words by levenshtein distance
        - query: a "misspelled" query string for which we would like suggestions
        - D: the maximum edit distance allowed, or the tolerance value
        - number: the parameter passed to timeit
    """

    def _time_levenshtein_nfa() -> list[str]:
        lev_nfa = LevenshteinNFA(query, D)
        return lev_nfa.get_similar_words(trie)

    def _time_bktree() -> list[str]:
        return bktree.get_similar_words_ordered(query, D)

    time_lev = timeit(_time_levenshtein_nfa, number=number) / number
    time_bktree = timeit(_time_bktree, number=number) / number
    return time_lev, time_bktree


def scramble_from_file(filename: str, n: int = -1) -> list[str]:
    """Return a list of n scrambled words from the words in the given file.

    If n is not specified, then all words are returned.
    """
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
        words = text.split()
        if n != -1:
            words = random.choices(words, k=n)
        new_words = clean_up_words(words)

    return scramble_multiple(new_words)


def scramble_multiple(words: list[str]) -> list[str]:
    """Return a list of scrambled words from the given list of words."""
    new_words = []
    for word in words:
        new_words.append(scramble(word))
    return new_words


def scramble(word: str) -> str:
    """Returns a scrambled word from a given word."""
    scramble_measure = random.randint(1, 3)
    letters = "abcdefghijklmnopqrstuvwxyz"
    new_word = list(word)
    for _ in range(scramble_measure):
        choice = random.randint(0, 2)
        index_random = random.randint(0, len(new_word) - 1)
        if choice == 0 and len(new_word) >= 2:  # deletion
            del new_word[index_random]
        elif choice == 1:  # insertion
            new_word = (
                new_word[:index_random]
                + [random.choice(letters)]
                + new_word[index_random:]
            )
        else:  # substition
            new_word[index_random] = random.choice(letters)
    return "".join(new_word)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # comment the below python_ta code before running the demo
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(
        config={
            "extra-imports": [
                'timeit',
                'random',
                'plotly.graph_objects',
                'plotly.subplots',
                'trie',
                'levenshtein',
                'bktree',
                'helpers'
            ],
            "allowed-io": [
                'read_results_from_file',
                'write_results_to_file',
                'scramble_from_file'
            ],
            "max-line-length": 100,
            "disable": ["E1136", "C0103"],
        }
    )
    # C0103 is added because the naming convention is common for the classes/functions used.

    # uncomment the following for a demo
    # NOTE: comment out the python_ta code so that it does not influence the timing
    # experiments.

    # res = time_multiple(number=2, n=20)
    # plot_time_statistics(res)
