"""GUI for autocorrect."""
import tkinter as tk

from backend import Backend
from bktree import make_bktree_from_file
from levenshtein_automaton import LevenshteinBackend
from trie import Trie, make_trie_from_file


class App(tk.Frame):
    """The main GUI class."""
    text_area: tk.Text
    suggestions: tk.Label

    _status_bar: tk.PanedWindow
    _input_handler: "ACHandler"

    def __init__(self, master=None):
        super().__init__(master)
        self.master.title('Some Title')
        self.master.geometry('700x500')
        self._add_menu()
        self._add_elements()
        self._add_status_bar()
        self._bind_events()

        self.pack(fill=tk.BOTH, expand=1)

    def _add_elements(self) -> None:
        """Add the main elements onto the frame."""
        self.text_area = tk.Text(self, relief=tk.FLAT, wrap=tk.WORD)
        self.text_area.pack(expand=1, fill=tk.BOTH)

    def _add_menu(self) -> None:
        """Add the menu onto the frame."""
        menubar = tk.Menu(self.master)
        file_menu = tk.Menu(menubar)
        file_menu.add_command(label='Nothing')
        menubar.add_cascade(label='File', menu=file_menu)

        self.master.config(menu=menubar)

    def _add_status_bar(self) -> None:
        """Add the status bar onto the frame."""
        # setting borderwidth doesn't seem necessary
        self._status_bar = tk.PanedWindow(self, borderwidth=0)

        self.suggestions = tk.Label(self._status_bar, text='Type something...')
        self._status_bar.add(self.suggestions)
        self.suggestions.pack(fill=tk.X, expand=1)

        self._status_bar.pack(side=tk.BOTTOM)

    def _bind_events(self) -> None:
        """Bind events to the handler."""
        self._input_handler = ACHandler(self, 'lv')
        for event, func in self._input_handler.BINDINGS:
            self.text_area.bind(event, func)


class ACHandler:
    """An abstract class that handles autocorrect/autocomplete functionality
    for App."""

    BINDINGS: list
    _app: App
    _ta: tk.Text

    # CHANGE THIS FOR A DIFFERENT DICTIONARY
    DICT_FILE = 'big_dictionary.txt'

    _trie: Trie                 # dictionary of correct words
    _backend: Backend
    _prev_word: str
    _suggestions: list[str]     # keeps track of the current suggestions

    def __init__(self, app: App, which: str) -> None:
        """Note: which in {'lv', 'bk'}"""
        self.BINDINGS = [
            ('<KeyRelease>', self._key_released),
            ('<ButtonRelease>', self._button_pressed),
            ('<Control-Key>', self._replace)
        ]
        self._app = app
        self._ta = self._app.text_area
        self._ta.mark_set('start', '1.0')
        self._ta.mark_gravity('start', tk.LEFT)
        self._ta.tag_config('cur', foreground='red')

        self._trie = make_trie_from_file(self.DICT_FILE)
        if which == 'lv':
            self._backend = LevenshteinBackend(self._trie)
        else:
            self._backend = make_bktree_from_file(self.DICT_FILE)

        self._prev_word = ''
        self._suggestions = []

    def _key_released(self, event: tk.Event) -> None:
        """Handle updates associated with key presses, such as updating suggestions."""
        self._set_word_start()
        self._update_suggestions()

    def _button_pressed(self, event: tk.Event) -> None:
        self._set_word_start()
        self._update_suggestions()

    def _replace(self, event: tk.Event) -> None:
        if event.keysym in '123456':
            choice = int(event.keysym)
            # valid choice
            if choice <= len(self._suggestions):
                self._ta.delete('start', tk.INSERT)
                self._ta.insert('start', self._suggestions[choice - 1])

    def _set_word_start(self) -> None:
        """Set the mark 'start' to the beginning of the word containing or right before the cursor.

        A word is either a string of consecutive letter, digit, or _, or a single character that
        is none of these types.
        """
        cursor_ind = self._ta.index(tk.INSERT)
        # if cursor is at start
        if cursor_ind == ('1.0'):
            self._ta.mark_set('start', '1.0')
        elif self._ta.index(cursor_ind + ' wordstart') == cursor_ind:
            self._ta.mark_set('start', cursor_ind + '-1c wordstart')
            # if self._ta.index(cursor_ind + '-1c' + ' wordstart') == self._ta.index(cursor_ind + '-1c'):
        else:
            self._ta.mark_set('start', cursor_ind + ' wordstart')

    def _update_suggestions(self) -> None:
        cur_word = self._ta.get('start', tk.INSERT)
        print('-> ' + cur_word)

        if cur_word == self._prev_word:
            return
        else:
            self._prev_word = cur_word

        # by the specification of 'wordstart', only alphanumeric characters and '_' are
        # connected to form words
        # do not give suggestions on punctuation, etc.
        if not cur_word or (len(cur_word) == 1 and not cur_word.isalnum()):
            self._suggestions = []
        else:
            completions = self._trie.get_suggestions(cur_word, 3)
            corrections = []
            # don't offer corrections if the word is spelled correctly
            if not self._trie.lookup_word(cur_word):
                corrections = self._backend.get_suggestions(cur_word, 3)
            self._suggestions = completions + corrections

        self._app.suggestions['text'] = self._format_suggestions(
            self._suggestions)

    def _format_suggestions(self, sug: list[str]):
        """A helper for formatting suggestions."""
        output = ''
        for ind, word in enumerate(sug):
            output += f'{ind + 1}: {word}  '

        if not output:
            return 'No suggestions...'
        return output


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
