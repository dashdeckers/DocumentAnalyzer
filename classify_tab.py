import tkinter as tk
import tkinter.ttk as ttk
import os
from utility import get_context, text_folder

class ClassifyTab(tk.Frame):
    '''
    TODO: Fill this in.
    '''
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.max_button_cols = 4

        # Project data
        self.cat_names = None
        self.cat_buttons = None
        self.words_togo = list()
        self.text_tokens = list()
        self.text_files_done = list()
        self.previous_word_var = tk.StringVar(self, value='')
        self.current_word_var = tk.StringVar(self, value='')

        # GUI stuff
        self.word_frame = ttk.Frame(self)
        self.previous_word = ttk.Label(self.word_frame, textvar=self.previous_word_var)
        self.current_word = ttk.Label(self.word_frame, textvar=self.current_word_var)
        self.buttons_frame = ttk.Frame(self)

        # Packing
        self.previous_word.pack(side='top', fill='x', expand=1)
        self.current_word.pack(side='top', fill='x', expand=1)
        self.word_frame.pack(side='top', fill='both', expand=1)
        self.buttons_frame.pack(side='bottom', fill='both', expand=1)

    def refresh_classify(self):
        '''Sets the word labels to either be blank or to show
        the corresponding words. Also either creates the buttons
        for each category or destroys them if they exist,
        depending on whether a project is open.

        Called by:
        master.create_new_project()
        master.clear_current_project()
        master.open_project()
        '''
        self.words_togo = list()
        self.text_tokens = list()
        self.text_files_done = list()

        if self.get_next_text() == 'Working':
            self.next_word()

        if self.cat_buttons:
            for button in self.cat_buttons:
                button.destroy()
        self.create_cat_buttons()

    def add_word_to_cat(self, event, cat_num, cat_name):
        '''Add the current word to the corresponding category,
        depending on which button was pressed, and get the next word.

        Called by the user.
        '''
        context = self.current_word_var.get().split()
        word_index = int(len(context) / 2)
        self.master.categories[cat_name].append(context[word_index])
        self.next_word()

    def insert_next_context(self, context=None):
        '''Set self.previous_word to show the value of
        self.current_word and set self.current_word to show the context.
        If no context was given, set both to show nothing. Also
        highlight the main word of the context.

        **Args**:

        * context (list): The context to show.
        '''
        if not context:
            self.previous_word_var.set('')
            self.current_word_var.set('')
        else:
            self.previous_word_var.set(self.current_word_var.get())
            self.current_word_var.set(' '.join(context))

    def next_word(self):
        '''Get the next unclassified word and put it along with its
        context in self.current_word via self.insert_next_word().

        Called by add_word_to_cat() and refresh_classify().
        '''
        if self.master.project_currently_open():
            if self.words_togo:
                del self.words_togo[0]

            if not self.words_togo:
                status = self.get_next_text()
                if status == 'Done':
                    self.insert_next_context('--- No more words left! ---')
                    return
                if status == 'Empty':
                    self.insert_next_context()
                    return

            context = get_context(self.text_tokens, self.words_togo[0])
            self.insert_next_context(context)

    def get_next_text(self):
        '''Get the next text from text_folder containing a word not yet 
        present in the wordlists, store that tokenized text in
        self.text_tokens, then find all the uncategorized words
        in that text and store those in self.words_togo.

        Called by next_word().

        **Returns**:
        None if no project is open,
        'Empty' if there are no texts in the text_folder,
        'Working' if it found a text containing an unclassified word, and
        'Done' if it found a text but no unclassified words.
        '''
        if self.master.project_currently_open():
            files_directory = os.path.join('.', self.master.project_name, text_folder)
            files = [file for file in os.listdir(files_directory) if os.path.isfile(os.path.join(files_directory, file))]

            if not files:
                return 'Empty'

            for file in files:
                if file.endswith('.txt') and file not in self.text_files_done:
                    with open(os.path.join(files_directory, file), 'r') as text_file:
                        text_tokens = text_file.read().split()
                        for word in text_tokens:
                            if not self.is_in_wordlists(word):
                                self.text_tokens = text_tokens
                                self.words_togo = self.filter_tokens(text_tokens)
                                return 'Working'
                    self.text_files_done.append(file)
            return 'Done'

    def is_in_wordlists(self, word):
        '''Check if the word is already in one of the categories /
        wordlists.

        Called by get_next_text().

        **Args**:

        * word (str): The word to be searched for across categories.

        **Returns**:
        True if the word is in one of the categories.
        '''
        for catname in self.master.categories:
            if word in self.master.categories[catname]:
                return True
        return False

    def filter_tokens(self, tokens):
        '''Filters a tokenized text to find all the words that have not
        yet been categorized.

        Called by get_next_text().

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

    def create_cat_buttons(self):
        '''Create the buttons that add the current word to a specific
        category. It creates them dynamically and arranges them in
        as many columns as specified in max_button_cols.

        Called by refresh_classify().
        '''
        if self.master.project_currently_open():
            self.cat_names = list(self.master.categories.keys())
            self.cat_buttons = list()
            for i in range(self.master.n_cats):
                self.cat_buttons.append(ttk.Button(self.buttons_frame, text=self.cat_names[i] + f' ({i+1})', command=lambda event=0, b_num=i, b_name=self.cat_names[i]: self.add_word_to_cat(event, b_num, b_name)))
            for i in range(self.master.n_cats):
                self.cat_buttons[i].grid(row=int(i/self.max_button_cols), column=i%self.max_button_cols)
