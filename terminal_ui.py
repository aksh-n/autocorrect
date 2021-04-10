import cmd
from trie_and_helpers import Trie, make_trie_from_file

addresses = [
    'here@blubb.com',
    'foo@bar.com',
    'whatever@wherever.org',
]

class KoalaShell(cmd.Cmd):
    intro = 'Welcome to the koala shell of the autocorrect project.   Type help or ? to list commands.\n'
    prompt = '(koala) '

    def __init__(self, trie: Trie):
        super().__init__()
        self._trie = trie

    # ----- basic koala commands -----
    def do_autocomplete(self, arg: str):
        pass

    def complete_autocomplete(self, text: str, line: str, start_index: int, end_index: int):
        """Autocompletes the word after autocomplete command using the words in self.trie."""
        text = text.strip()
        return [self._trie.autocomplete_from_prefix(text)]

    def do_send(self, arg: str):
        print(arg, type(arg))
        pass

    def complete_send(self, text: str, line: str, start_index: int, end_index: int):
        if text:
            return [
                address for address in addresses
                if address.startswith(text)
            ]
        else:
            return addresses
    
    def do_quit(self, arg):
        """Exiting the command line shell."""
        print("Thank you for using koala.\nBye!")
        return True


if __name__ == '__main__':
    trie = make_trie_from_file("test_files/wiener_summary.txt")
    # print(trie.lookup_word('cybernetics'))
    # print(trie.autocomplete_from_prefix('cyber'))
    my_cmd = KoalaShell(trie)
    my_cmd.cmdloop()