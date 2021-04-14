"""This module contains an abstract class that represents the common backend structure to
all autocomplete data structures.
"""

class Backend:
    """A class."""
    def get_suggestions(self, word: str, lim: int = 3) -> list[str]:
        """Get a list of suggestions for autocomplete/autocorrect for the current word.

        The length of the list is maximum 'lim'.
        """
        raise NotImplementedError