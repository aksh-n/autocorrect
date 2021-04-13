"""GUI for autocorrect."""
import tkinter as tk

class App(tk.Frame):

    _text_area: tk.Text

    def __init__(self, master=None):
        super().__init__(master)
        self.master.title('Some Title')
        self.master.geometry('700x500')
        self._add_menu()
        self._add_elements()

        self.pack(fill=tk.BOTH, expand=1)

    def _add_elements(self) -> None:
        """Add the main elements onto the frame."""
        self._text_area = tk.Text(self, relief=tk.FLAT)
        self._text_area.pack(expand=1, fill=tk.BOTH)

    def _add_menu(self) -> None:
        """Add the menu onto the frame."""
        menubar = tk.Menu(self.master)
        file_menu = tk.Menu(menubar)
        file_menu.add_command(label='Nothing')
        menubar.add_cascade(label='File', menu=file_menu)

        self.master.config(menu=menubar)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
