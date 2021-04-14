"""GUI for autocorrect."""
import tkinter as tk
from tkinter.constants import INSERT

from trie import Trie, make_trie_from_file
from bktree import BKTree, make_bktree_from_file

class App(tk.Frame):
    """The main GUI class."""
    _text_area: tk.Text
    _status_bar: tk.PanedWindow
    _suggestions: tk.Label
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
        self._text_area = tk.Text(self, relief=tk.FLAT, wrap=tk.WORD)
        self._text_area.pack(expand=1, fill=tk.BOTH)

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

        self._suggestions = tk.Label(self._status_bar, text='Type something...')
        self._status_bar.add(self._suggestions)

        self._status_bar.pack(side=tk.BOTTOM)

    def _bind_events(self) -> None:
        """Bind events to the handler."""
        # TODO: change this
        self._input_handler = BKTreeHandler(self)
        for event, func in self._input_handler.BINDINGS:
            self._text_area.bind(event, func)

class ACHandler:
    """An abstract class that handles autocorrect/autocomplete functionality
    for App."""

    BINDINGS: list
    _app: App
    _ta: tk.Text

    # dictionary of correct words
    _trie: Trie

    def __init__(self, app: App) -> None:
        self.BINDINGS = [
            ('<KeyRelease>', self._key_pressed),
            ('<ButtonRelease>', self._button_pressed)
        ]
        self._app = app
        self._ta = self._app._text_area
        self._ta.mark_set('start', '1.0')
        self._ta.mark_gravity('start', tk.LEFT)
        self._ta.tag_config('cur', foreground='red')

        self._trie = make_trie_from_file('dictionary.txt')

    def _key_pressed(self, event: tk.Event) -> None:
        """Handle updates associated with key presses, such as updating suggestions."""
        # TODO: backspace doesn't work yet
        # TODO: moving cursor doesn't work yet
        # this is to avoid it accepting values like 'space'
        # if len(event.keysym) == 1 and event.keysym.isalnum():
        #     return
        # otherwise
        # self._ta.tag_add('cur', self._ta.index('start'), tk.END)
        self._set_word_start()
        self._update_suggestions()

    def _button_pressed(self, event: tk.Event) -> None:
        self._set_word_start()
        self._update_suggestions()

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


    # TODO: note on some improvements
    # Learn the word as soon as the user finishes typing
    # Prioritize completion over correction
    # no past tense or something?
    def _update_suggestions(self) -> None:
        """Update self._app._suggestions to show autocorrect/autocomplete options."""
        raise NotImplementedError


class BKTreeHandler(ACHandler):
    """A class that implements ACHandler using a BKTree."""

    BINDINGS: list
    _bktree: BKTree

    def __init__(self, app: App) -> None:
        super().__init__(app)
        self._bktree = make_bktree_from_file('dictionary.txt')

    # def key_pressed(self, event: tk.Event) -> None:
    #     pass

    def _update_suggestions(self) -> None:
        cur_word = self._ta.get(self._ta.index('start'), tk.INSERT)
        print('-> ' + cur_word)
        # print(self._ta.index('start'))

        # by the specification of 'wordstart', only alphanumeric characters and '_' are
        # connected to form words
        # do not give suggestions on punctuation, etc.
        if not cur_word or (len(cur_word) == 1 and not cur_word.isalnum()):
            self._app._suggestions['text'] = 'No suggestions...'
        elif not self._trie.lookup_word(cur_word):
            sug = self._bktree.get_similar_words_ordered(cur_word)
            if not sug:
                self._app._suggestions['text'] = 'No suggestions...'
            else:
                self._app._suggestions['text'] = str(sug[0])
        else:   # if the word is correctly spelled
            self._app._suggestions['text'] = '...'


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
