import tkinter as tk
import tkinter.ttk as ttk

from os import listdir
from os.path import join, isfile

try:
    from DocumentAnalyzer.utility import (
        get_context,
        text_folder,
        max_button_cols,
    )
except ImportError as e:
    from utility import (
        get_context,
        text_folder,
        max_button_cols,
    )

class ClassifyTab(tk.Frame):
    '''
    TODO: Fill this in.
    '''
    def __init__(self, master):
        super().__init__()
        self.master = master

        # Project data
        self.cat_buttons = None
        self.words_togo = list()
        self.text_tokens = list()
        self.text_files_done = list()

        # GUI stuff
        self.c_frame = ttk.Frame(self)
        self.c_words = list()
        self.c_labels = list()
        for i in range(5):
            self.c_words.append(tk.StringVar(self.c_frame, value=''))
            self.c_labels.append(ttk.Label(self.c_frame,
                                            textvar=self.c_words[-1]))
        self.c_labels[2].configure(style='WORD.TLabel')
        self.buttons_frame = ttk.Frame(self)

        # Packing
        for i in range(5):
            self.c_labels[i].pack(side='left', expand=1)
        self.c_frame.pack(side='top', fill='x', expand=1)
        self.buttons_frame.pack(side='bottom', fill='both', expand=1)

    def refresh_classify(self):
        '''Sets the word labels to either be blank or to show the
        corresponding words. Also either creates the buttons for each
        category or destroys them if they exist, depending on whether a
        project is open.
        '''
        self.words_togo = list()
        self.text_tokens = list()
        self.text_files_done = list()

        if self.get_next_text() == 'Working':
            self.next_word()

        self.destroy_cat_buttons()
        self.create_cat_buttons()

    def add_word(self, event, catname):
        '''Add the current word to the corresponding category,
        depending on which button was pressed, and get the next word.
        '''
        word = self.c_words[2].get()
        if not word == 'Finished!':
            self.master.categories[catname].append(word)
        self.next_word()

    def insert_next_context(self, word=None, context=None):
        '''Set the previous word labels to show the values of the current
        word labels and set the current word labels to show the current
        context. If no context was given, set both to show nothing. If
        the user has classified all words, show only 'Finished!'.

        **Args**:

        * word (str): The main word

        * context (list of lists): The left and right context to show,
        each containing up to two words.
        '''
        if word == 'Finished!' and not context:
            for i in range(5):
                self.c_words[i].set('')
            self.c_words[2].set(word)
            return

        if not context and not word:
            for i in range(5):
                self.c_words[i].set('')

        else:
            # Left context
            if len(context[0]) == 2:
                self.c_words[0].set(context[0][0])
                self.c_words[1].set(context[0][1])

            if len(context[0]) == 1:
                self.c_words[0].set('')
                self.c_words[1].set(context[0][0])

            if len(context[0]) == 0:
                self.c_words[0].set('')
                self.c_words[1].set('')

            # Word
            self.c_words[2].set(word)

            # Right context
            for i in [0,1]:
                try:
                    self.c_words[3+i].set(context[1][i])
                except IndexError as e:
                    self.c_words[3+i].set('')
                    pass


    def next_word(self):
        '''Get the next unclassified word and put it along with its
        context in self.current_word via self.insert_next_word().
        '''
        if self.master.project_currently_open():

            self.words_togo = self.filter(self.words_togo)

            if not self.words_togo:
                status = self.get_next_text()
                if status == 'Done':
                    self.insert_next_context('Finished!')
                    return
                if status == 'Empty':
                    self.insert_next_context()
                    return

            if self.words_togo:
                context = get_context(self.text_tokens, self.words_togo[0])
                self.insert_next_context(self.words_togo[0], context)

    def get_next_text(self):
        '''Get the next text from text_folder containing a word not yet 
        present in the wordlists, store that tokenized text in
        self.text_tokens, then find all the uncategorized words
        in that text and store those in self.words_togo.

        **Returns**:
        None if no project is open,
        'Empty' if there are no texts in the text_folder,
        'Working' if it found a text containing an unclassified word, and
        'Done' if it found a text but no unclassified words.
        '''
        if self.master.project_currently_open():
            f_dir = join('.', self.master.project_name, text_folder)
            files = [f for f in listdir(f_dir) if isfile(join(f_dir, f))]

            if not files:
                return 'Empty'

            for file in files:
                if file.endswith('.txt') and file not in self.text_files_done:
                    with open(join(f_dir, file), 'r') as text_file:
                        text_tokens = text_file.read().split()
                        for word in text_tokens:
                            if not self.is_in_wordlists(word):
                                self.text_tokens = text_tokens
                                self.words_togo = self.filter(text_tokens)
                                return 'Working'
                    self.text_files_done.append(file)
            return 'Done'

    def is_in_wordlists(self, word):
        '''Check if the word is already in one of the categories /
        wordlists.

        **Args**:

        * word (str): The word to be searched for across categories.

        **Returns**:
        True if the word is in one of the categories.
        '''
        for catname in self.master.categories:
            if word in self.master.categories[catname]:
                return True
        return False

    def filter(self, tokens):
        '''Filters a tokenized text to remove all the words that have
        already been categorized.

        **Args**:

        * tokens (list): The tokenized text.

        **Returns**:
        The filtered list of tokens.
        '''
        words_togo = list()
        for word in tokens:
            if not self.is_in_wordlists(word):
                words_togo.append(word)
        return words_togo

    def destroy_cat_buttons(self):
        '''Destroy the buttons that add the current word to a specific
        category.'''
        if self.cat_buttons:
            for button in self.cat_buttons:
                button.destroy()

    def create_cat_buttons(self):
        '''Create the buttons that add the current word to a specific
        category. It creates them dynamically and arranges them in as
        many columns as specified in max_button_cols.
        '''
        if self.master.project_currently_open():
            self.cat_buttons = list()

            for i, catname in enumerate(self.master.categories):
                func = lambda c=catname: self.add_word(None, c)
                self.cat_buttons.append(ttk.Button(self.buttons_frame,
                                                   text=f'{catname} ({i+1})',
                                                   command=func))

            for i, button in enumerate(self.cat_buttons):
                button.grid(row=int(i / max_button_cols),
                            column=i % max_button_cols)
