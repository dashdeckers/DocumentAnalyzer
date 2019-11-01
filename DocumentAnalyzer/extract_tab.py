import tkinter as tk
import tkinter.ttk as ttk

from os.path import join, splitext
from functools import partial

try:
    from DocumentAnalyzer.symspellpy.symspellpy import Verbosity
    from DocumentAnalyzer.utility import (
        CustomText,
        add_to_dict_file,
        text_extracter, 
        clean_text,
        file_folder,
        text_folder,
        strings,
    )
except ImportError as e:
    from symspellpy.symspellpy import Verbosity
    from utility import (
        CustomText,
        add_to_dict_file,
        text_extracter, 
        clean_text,
        file_folder,
        text_folder,
        strings,
    )

class ExtractTab(tk.Frame):
    '''
    This class contains the tab responsible for extracting and editing
    the text from PDF files.
    '''
    def __init__(self, master):
        super().__init__()
        self.master = master

        # Project data
        self.default_text = strings['default_text']
        self.filename_var = tk.StringVar(self, value='')
        self.filenumber_var = tk.StringVar(self, value='')

        # GUI stuff
        self.extract_filefield = ttk.Frame(self)
        self.extract_filename = ttk.Label(self.extract_filefield,
                                          textvar=self.filename_var,
                                          anchor='w')
        self.extract_filenumber = ttk.Label(self.extract_filefield,
                                            textvar=self.filenumber_var,
                                            anchor='e')
        self.extract_text = CustomText(self,
                                       font=(None, self.master.font_size),
                                       wrap='word',
                                       undo=True,
                                       autoseparators=False)
        self.scrollbar = tk.Scrollbar(self, orient='vertical')
        self.extract_text.configure(yscrollcommand=self.scrollbar.set)
        self.extract_text.tag_configure('misspelled',
                                        foreground='red',
                                        underline=True)
        self.extract_text.tag_configure('find',
                                        background='yellow')
        self.extract_text.insert('1.0', self.default_text)
        self.extract_text.configure(state='disabled')
        self.extract_text.focus_force()

        # Packing
        self.extract_filename.pack(side='left', fill='both')
        self.extract_filenumber.pack(side='right', fill='both')
        self.extract_filefield.pack(side='bottom', fill='both')
        self.scrollbar.pack(side='right', fill='y')
        self.extract_text.pack(side='top', fill='both', expand=1)

    def refresh_extract(self):
        '''Sets the text in the textfield to either the default text or to the
        text extracted from the first file in the self.master.files_todo list
        if that list is not empty and a project is currently open. If text was
        extracted, it runs a spellcheck on it. Also updates the fileprogress
        bar.
        '''
        self.hide_corrections()

        if self.master.project_currently_open() and self.master.files_todo:
            self.extract_text.configure(state='normal')
            # Don't do anything if we have already extracted the correct text.
            # We don't want to replace current spell-correction progress.
            if not self.filename_var.get() == self.master.files_todo[0]:
                path_to_text = join(self.master.folder,
                                    file_folder,
                                    self.master.files_todo[0])
                text = text_extracter(path_to_text)
                text = clean_text(text)
                self.extract_text.delete('1.0', 'end')
                self.extract_text.insert('1.0', text)
                # Add a space at the end to make sure the replace_word()
                # function always works.
                self.extract_text.insert('end', ' ')
                self.extract_text.edit_reset()
                self.spellcheck()
        else:
            self.extract_text.delete('1.0', 'end')
            self.extract_text.insert('1.0', self.default_text)
            self.extract_text.configure(state='disabled')
            self.extract_text.edit_reset()

        self.update_fileprogress()

    def update_fileprogress(self):
        '''Sets the current filename and the file progress on the fileprogress
        bar below the extract tab. If there is no project currently open,
        these values are blank.
        '''
        n_done = len(self.master.files_done)
        n_todo = len(self.master.files_todo)

        if self.master.project_currently_open():
            if self.master.files_todo:
                self.filename_var.set(self.master.files_todo[0])
                self.filenumber_var.set(f'{n_done + 1}/{n_todo + n_done}')
            else:
                self.filename_var.set('')
                self.filenumber_var.set(f'{n_done}/{n_todo + n_done}')
        else:
            self.filename_var.set('')
            self.filenumber_var.set('')

    def next_file(self, event=None):
        '''Saves the text currently in the text field in the text_folder of
        the project using the same filename, and then replace the text with
        the extracted text of the next file (or with the default text if there
        is no next file).
        '''
        if self.master.project_currently_open() and self.master.files_todo:
            text = self.extract_text.get('1.0', 'end')
            filename = splitext(self.filename_var.get())[0] + '.txt'
            path_to_text = join(self.master.folder,
                                text_folder,
                                filename)
            with open(path_to_text, 'w') as file:
                file.write(text)

            self.master.files_done.append(self.master.files_todo[0])
            del self.master.files_todo[0]

            self.master.sync_filehistory(self.master.folder)

        self.refresh_extract()
        return 'break'

    def reparse(self):
        '''Discard the text currently in the text field and replace it with
        the extracted text of the next file. The user is prompted for
        confirmation.
        '''
        self.filename_var.set('')
        self.refresh_extract()

    def get_corrections(self, word):
        '''Get a list of correction suggestions for the word.

        **Args**:

        * word (str): The misspelled word to get corrections for.

        **Returns**:
        A list of possible corrections, sorted by edit distance and
        term frequency.
        '''
        single_corrections = self.master.spell.lookup(word, Verbosity.ALL)
        single_corrections = [c.term for c in single_corrections]

        compound_corrections = self.master.spell.lookup_compound(word, 2)
        compound_corrections = [c.term for c in compound_corrections]

        candidates = single_corrections[:5] + compound_corrections[:5]
        return candidates

    def show_corrections(self, event=None):
        '''Show the list of corrections as a menu at the mouse position.
        '''
        # Make sure we don't have two menus open
        self.hide_corrections()

        # Get the word at the index
        index = self.extract_text.index('insert')
        try:
            word = self.extract_text.get(index + ' wordstart', index + ' wordend')
        except tk.TclError:
            word = ''

        # If the word is spelled incorrectly
        if word and len(word) > 1 and word not in self.master.spell._words:

            # Get the possible corrections and add them to the menu
            self.corrections_menu = tk.Menu(self, tearoff=0)
            corrections = self.get_corrections(word)
            for cword in corrections:
                callback = partial(self.replace_word, word=cword, index=index)
                self.corrections_menu.add_command(label=cword, command=callback)

            # Add the 'add to dict' option and put the menu where it belongs
            callback = partial(self.add_to_dict, word=word)
            self.corrections_menu.add_command(label='Add to dictionary', command=callback)
            x, y = self.winfo_pointerx(), self.winfo_pointery() + int(self.master.font_size / 2)
            self.corrections_menu.post(x, y)

    def hide_corrections(self, event=None):
        '''Hide the menu showing the list of corrections.
        '''
        try:
            self.corrections_menu.destroy()
        except AttributeError:
            pass

    def add_to_dict(self, word):
        '''Adds a word to the dictionary
        '''
        add_to_dict_file(word, self.master.folder)
        self.master.spell.create_dictionary_entry(word, 1)
        self.spellcheck()

    def replace_word(self, word, index):
        '''Replace the word at the index with the given word.

        **Args**:

        * word (str): The word to replace the other word.

        * index (str): The index at which the word can be found that
        should be replaced.
        '''
        self.extract_text.edit_separator()
        self.extract_text.delete(index + ' wordstart', index + ' wordend')
        self.extract_text.insert('insert', word)
        self.extract_text.edit_separator()

    def spellcheck(self, event=None):
        '''Highlight each word in the text field that is misspelled.
        '''
        if not self.master.files_todo or not self.master.spell:
            return 'break'

        self.extract_text.tag_remove('misspelled', '1.0', 'end')
        self.extract_text.tag_remove('find', '1.0', 'end')

        # Loop through each word in text
        index = '1.0'
        while index:
            # Get the starting index of the next word
            index = self.extract_text.search(r'\w+', index, 'end', regexp=1)
            if index:
                word = self.extract_text.get(index, index + ' wordend')
                word_end_index = f'{index}+{len(word)}c'
                # If the word is a spelling error, tag it
                if word not in self.master.spell._words:
                    self.extract_text.tag_add('misspelled', index, word_end_index)
                index = word_end_index

        return 'break'

    def on_space_press(self, event=None):
        '''Run the spellchecker and add an edit separator everytime the space
        bar is pressed.
        '''
        self.extract_text.edit_separator()
        self.after(10, self.spellcheck)

    def find(self, string, event=None):
        '''Highlights all occurrences of the string and centers the view around
        the first occurrence.
        '''
        pattern = '\\y' + string + '\\y'
        self.extract_text.tag_pattern(pattern, 'find', regexp=True)

        return 'break'

    def delete(self, string, event=None):
        '''Deletes all occurrences of the word or string in the text.
        '''
        self.extract_text.edit_separator()

        pattern = '\\y' + string + '\\y'
        self.extract_text.delete_pattern(pattern, regexp=True)

        self.spellcheck()
        return 'break'

    def undo(self, event=None):
        '''Undo the last edit using the built in method in the Text widget.
        '''
        try:
            self.extract_text.edit_undo()
            self.spellcheck()
        except tk.TclError:
            pass

        return 'break'

    def redo(self, event=None):
        '''Redo the last edit using the built in method in the Text widget.
        '''
        try:
            self.extract_text.edit_redo()
            self.spellcheck()
        except tk.TclError:
            pass

        return 'break'
