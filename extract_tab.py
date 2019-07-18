import tkinter as tk
import tkinter.ttk as ttk
import os
from functools import partial
from utility import (
    text_extracter, 
    clean_text,
    file_folder,
)
import time

class ExtractTab(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.default_text = 'Open or create a project and then import files via the menu to get started '

        self.filename_var = tk.StringVar(self, value='')
        self.filenumber_var = tk.StringVar(self, value='')
        self.extract_filefield = ttk.Frame(self)
        self.extract_filename = ttk.Label(self.extract_filefield, textvar=self.filename_var, anchor='w')
        self.extract_filenumber = ttk.Label(self.extract_filefield, textvar=self.filenumber_var, anchor='e')
        self.extract_text = tk.Text(self, font=(None, self.master.font_size), wrap='word')
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
        self.hide_corrections()
        # Check the file list and put the extracted text of the first file if there are files
        if self.master.files_todo:
            text = text_extracter(os.path.join('.', self.master.project_name, file_folder, self.master.files_todo[0]))
            text = clean_text(text)
            self.extract_text.delete('1.0', 'end')
            self.extract_text.insert('1.0', text)
            # Add a space at the end to make sure the replace word function always works
            self.extract_text.insert('end', ' ')
            self.update_fileprogress()
            self.spellcheck()

    def update_fileprogress(self):
        num_files_done = len(self.master.files_done)
        num_files_todo = len(self.master.files_todo)
        self.filename_var.set(self.master.files_todo[0])
        self.filenumber_var.set(f'{num_files_done+1}/{num_files_todo+num_files_done}')

    def get_corrections(self, word):
        t0 = time.time()
        # TODO: This needs to be filtered to show suggestions ranked based on distance
        candidates = list(self.master.spell.candidates(word))
        print(f'Candidates after {time.time()-t0}')
        best_guess = self.master.spell.correction(word)
        candidates.remove(best_guess)
        print(f'Best guess after {time.time()-t0}')
        if len(candidates) > 5:
            return [best_guess] + candidates[:5]
        else:
            return [best_guess] + candidates

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
            self.extract_text.focus()
        except AttributeError:
            pass

    def focus_corrections_menu(self, event=None):
        try:
            self.corrections_menu.focus()
            self.corrections_menu.entryconfig(0, state='active')
        except tk.TclError:
            pass

    def replace_word(self, word, index):
        self.extract_text.delete(index + ' wordstart', index + ' wordend')
        self.extract_text.insert('insert', word)

    def spellcheck(self, event=None):
        # Loop through each word in text
        index = '1.0'
        while index:
            index = self.extract_text.search(r'\w+', index, 'end', regexp=1)
            if index:
                word = self.extract_text.get(index, index + ' wordend')
                word_end_index = f'{index}+{len(word)}c'
                # If the word is a spelling error, tag it
                if self.master.spell.unknown([word]):
                    self.extract_text.tag_add('misspelled', index, word_end_index)
                index = word_end_index