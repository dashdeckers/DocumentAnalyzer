import tkinter as tk
import tkinter.ttk as ttk
from functools import partial

class ExtractTab(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self.filename_var = tk.StringVar(self, value='filename')
        self.filenumber_var = tk.StringVar(self, value='1/10') # should maybe be blank?
        self.extract_filefield = ttk.Frame(self)
        self.extract_filename = ttk.Label(self.extract_filefield, textvar=self.filename_var, anchor='w')
        self.extract_filenumber = ttk.Label(self.extract_filefield, textvar=self.filenumber_var, anchor='e')
        self.extract_text = tk.Text(self, bg='white', fg='black', font=(None, self.master.font_size))
        self.scrollbar = tk.Scrollbar(self, orient='vertical')
        self.extract_text.configure(yscrollcommand=self.scrollbar.set)
        self.extract_text.tag_configure("misspelled", foreground="red", underline=True)
        self.extract_text.insert('1.0', 'Import files via the menu to get started')
        self.extract_text.bind('<ButtonRelease-1>', self.show_corrections)
        self.extract_text.bind('<Escape>', self.hide_corrections)
        self.extract_text.bind('<Button-1>', self.spellcheck)
        self.extract_text.focus_force()

        # Packing
        self.extract_filename.pack(side='left', fill='both')
        self.extract_filenumber.pack(side='right', fill='both')
        self.extract_filefield.pack(side='bottom', fill='both')
        self.scrollbar.pack(side='right', fill='y')
        self.extract_text.pack(side='top', fill='both', expand=1)

    def refresh_extract(self):
        # TODO: This should check the file list and put the extracted text of the first file if there are files
        self.hide_corrections()
        self.extract_text.delete('1.0', 'end')
        self.extract_text.insert('1.0', 'Import files via the menu to get started')

    def get_correction_menu_coords(self, num_entries):
        # TODO: Investigate this. How does the offset work exactly? do it based on mouse position?
        print(num_entries)
        bbox = self.extract_text.bbox('insert')
        print(bbox)
        offset = ((num_entries+1) * self.master.font_size)
        menu_x = bbox[0] + self.winfo_x() + self.extract_text.winfo_x()
        menu_y = bbox[1] + self.winfo_y() + self.extract_text.winfo_y() + offset
        return (menu_x, menu_y)

    def get_corrections(self, word):
        # TODO: This needs to be filtered to show suggestions ranked based on distance
        candidates = list(self.master.spell.candidates(word))
        if len(candidates) > 10:
            return candidates[:10]
        else:
            return candidates

    def show_corrections(self, event=None):
        # Make sure we don't have two menus open
        self.hide_corrections()

        # Get the word at the index
        index = self.extract_text.index('insert')
        try:
            word = self.extract_text.get(index + ' wordstart', index + ' wordend')
        except tk.TclError:
            word = ''

        # If the word is spelled incorrectly
        if word and len(word) > 1 and self.master.spell.unknown([word]):

            # Get the possible corrections and add them to the menu
            self.corrections_menu = tk.Menu(self, tearoff=0)
            corrections = self.get_corrections(word)
            for word in corrections:
                callback = partial(self.replace_word, word=word, index=index)
                self.corrections_menu.add_command(label=word, command=callback)

            # Put the menu where it belongs and bind the relevant keys
            x, y = self.get_correction_menu_coords(len(corrections))
            self.corrections_menu.post(x, y)
            self.corrections_menu.bind('<Escape>', self.hide_corrections)
            self.extract_text.bind('<Down>', self.focus_corrections_menu)

    def hide_corrections(self, event=None):
        try:
            self.corrections_menu.destroy()
            self.extract_text.unbind('<Down>')
            self.extract_text.focus_force()
        except AttributeError:
            pass

    def focus_corrections_menu(self, event=None):
        try:
            self.corrections_menu.focus_force()
            self.corrections_menu.entryconfig(0, state='active')
        except tk.TclError:
            pass

    def replace_word(self, word, index):
        self.extract_text.delete(index + ' wordstart', index + ' wordend')
        self.extract_text.insert(index + ' wordstart', word)

    def spellcheck(self, event=None):
        text = self.extract_text.get('1.0', 'end')
        words = text.split()
        spelling_errors = self.master.spell.unknown(words)

        index = "1.0"
        for word in spelling_errors:
            index = self.extract_text.search(word, "1.0", "end")
            if index == "":
                index = "1.0"
            self.extract_text.tag_add("misspelled", index, f"{index}+{len(word)}c")
