import tkinter as tk
import tkinter.ttk as ttk
from functools import partial
from utility import text_extracter

class ExtractTab(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.default_text = 'Import files via the menu to get started '

        self.filename_var = tk.StringVar(self, value='')
        self.filenumber_var = tk.StringVar(self, value='')
        self.extract_filefield = ttk.Frame(self)
        self.extract_filename = ttk.Label(self.extract_filefield, textvar=self.filename_var, anchor='w')
        self.extract_filenumber = ttk.Label(self.extract_filefield, textvar=self.filenumber_var, anchor='e')
        self.extract_text = tk.Text(self, bg='white', fg='black', font=(None, self.master.font_size))
        self.scrollbar = tk.Scrollbar(self, orient='vertical')
        self.extract_text.configure(yscrollcommand=self.scrollbar.set)
        self.extract_text.tag_configure("misspelled", foreground="red", underline=True)
        self.extract_text.insert('1.0', self.default_text)
        self.extract_text.bind('<ButtonRelease-1>', self.show_corrections)
        self.extract_text.bind('<Escape>', self.hide_corrections)
        self.extract_text.bind('<FocusOut>', self.hide_corrections)
        self.extract_text.bind('<Control-p>', self.spellcheck)
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
        if self.master.files_todo and self.extract_text.get('1.0', 'end') != self.default_text:
            text = text_extracter(self.master.files_todo[0])
            self.extract_text.delete('1.0', 'end')
            self.extract_text.insert('1.0', text)
            # Add a space at the end to make sure the replace word function always works
            self.extract_text.insert('end', ' ')
        self.update_fileprogress()

    def update_fileprogress(self):
        num_files_done = len(self.master.files_done)
        num_files_todo = len(self.master.files_todo)
        self.filename_var.set(self.master.files_todo[0])
        self.filenumber_var.set(f'{num_files_done+1}/{num_files_todo+num_files_done}')

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
            x, y = self.winfo_pointerx(), self.winfo_pointery() + int(self.master.font_size / 2)
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
        self.extract_text.insert(index + ' wordstart -1c', word)

    def spellcheck(self, event=None):
        text = self.extract_text.get('1.0', 'end')
        words = text.split()
        spelling_errors = self.master.spell.unknown(words)

        # Find and highlight each spelling error
        index = '1.0'
        for word in spelling_errors:
            # TODO: Only finds the first occurance!
            index = self.extract_text.search(word, '1.0', 'end')
            if index == '':
                index = '1.0'
            self.extract_text.tag_add('misspelled', index, f'{index}+{len(word)}c')
