"""Autocorrect, Backend

This module contains an abstract class that represents the common backend structure to
all autocomplete data structures.

Copyright (c) 2021 Akshat Naik and Tony (Juntao) Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""


class Backend:
    """A class representing an interface common to all data structures used for
    autocorrect/autocomplete features.
    """

    def get_suggestions(self, word: str, lim: int = 3) -> list[str]:
        """Get a list of suggestions for autocomplete/autocorrect for the current word.

        The length of the list is maximum 'lim'.
        """
        raise NotImplementedError


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(
        config={
            "extra-imports": [],
            "allowed-io": [],
            "max-line-length": 100,
            "disable": ["E1136"],
        }
    )
