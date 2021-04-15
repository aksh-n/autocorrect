"""Autocorrect, Main

This module is the main module for access to the functionalities of this project.

Copyright (c) 2021 Akshat Naik and Tony (Juntao) Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""


if __name__ == '__main__':
    from gui import run

    print('Welcome to AutoC by Akshat Naik and Tony (Juntao) Hu.')
    print('Choose an option from the two below:')
    print('    1. View and compare timing results for BKTree and Levenshtein Automaton')
    print('    2. Try to GUI -> a text editor that supports autocomplete/autocorrect')

    inp = input(': ')
    while inp != '1' and inp != '2':
        inp = input(': ')

    choice = int(inp)
    if choice == 1:
        pass
        # ADD TIMING RESULT CODE HERE
    else:
        print('NOTE: The GUI may take a bit of time to load. '
              'It may also not load in the foreground. Check the background!'
              )
        run()
