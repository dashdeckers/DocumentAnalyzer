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

        # GUI stuff
        self.pc_frame = ttk.Frame(self)
        self.cc_frame = ttk.Frame(self)

        self.pc_words = list()
        self.pc_labels = list()
        self.cc_words = list()
        self.cc_labels = list()
        for i in range(5):
            self.pc_words.append(tk.StringVar(self.pc_frame, value=''))
            self.cc_words.append(tk.StringVar(self.cc_frame, value=''))
        for i in range(5):
            self.pc_labels.append(ttk.Label(self.pc_frame, textvar=self.pc_words[i]))
            self.cc_labels.append(ttk.Label(self.cc_frame, textvar=self.cc_words[i]))

        self.pc_labels[2].configure(style='WORD.TLabel')
        self.cc_labels[2].configure(style='WORD.TLabel')

        self.buttons_frame = ttk.Frame(self)

        # Packing
        for i in range(5):
            self.pc_labels[i].pack(side='left', expand=1)
        self.pc_frame.pack(side='top', fill='x', expand=1)

        for i in range(5):
            self.cc_labels[i].pack(side='left', expand=1)
        self.cc_frame.pack(side='top', fill='x', expand=1)

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

    def add_word_to_cat(self, event, catnum, catname):
        '''Add the current word to the corresponding category,
        depending on which button was pressed, and get the next word.

        Called by the user.
        '''
        self.master.categories[catname].append(self.cc_words[2].get())
        print(self.master.categories)
        self.next_word()

    def insert_next_context(self, word=None, context=None):
        '''Set self.previous_word to show the value of
        self.current_word and set self.current_word to show the context.
        If no context was given, set both to show nothing.

        **Args**:

        * word (str): The main word
        * context (list of lists): The left and right context to show,
        each containing up to two words.
        '''
        if not context and not word:
            for i in range(5):
                self.pc_words[i].set('')
                self.cc_words[i].set('')

        else:
            for i in range(5):
                self.pc_words[i].set(self.cc_words[i].get())

            if len(context[0]) == 2:
                self.cc_words[0].set(context[0][0])
                self.cc_words[1].set(context[0][1])

            if len(context[0]) == 1:
                self.cc_words[0].set('')
                self.cc_words[1].set(context[0][0])

            if len(context[0]) == 0:
                self.cc_words[0].set('')
                self.cc_words[1].set('')

            self.cc_words[2].set(word)

            for i in [0,1]:
                try:
                    self.cc_words[3+i].set(context[1][i])
                except IndexError as e:
                    self.cc_words[3+i].set('')
                    pass


    def next_word(self, first=False):
        '''Get the next unclassified word and put it along with its
        context in self.current_word via self.insert_next_word().

        Called by add_word_to_cat() and refresh_classify().

        **Args**:

        * first (bool): Indicates that this is the first time the
        function is called
        '''
        if self.master.project_currently_open():

            if not self.words_togo:
                status = self.get_next_text()
                if status == 'Done':
                    self.insert_next_context('--- No more words left! ---')
                    return
                if status == 'Empty':
                    self.insert_next_context()
                    return

            if self.words_togo:
                self.words_togo = self.filter_tokens(self.words_togo)
                context = get_context(self.text_tokens, self.words_togo[0])
                self.insert_next_context(self.words_togo[0], context)

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
