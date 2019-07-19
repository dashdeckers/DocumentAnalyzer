import tkinter as tk
import tkinter.ttk as ttk
from utility import get_context

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
        self.previous_word_var = tk.StringVar(self, value='')
        self.current_word_var = tk.StringVar(self, value='')
        self.next_word_var = tk.StringVar(self, value='')

        # GUI stuff
        self.word_frame = ttk.Frame(self)
        self.previous_word = ttk.Label(self.word_frame, textvar=self.previous_word_var)
        self.current_word = ttk.Label(self.word_frame, textvar=self.current_word_var)
        self.next_word = ttk.Label(self.word_frame, textvar=self.next_word_var)
        self.buttons_frame = ttk.Frame(self)

        # Packing
        self.previous_word.pack(side='top', fill='x', expand=1)
        self.current_word.pack(side='top', fill='x', expand=1)
        self.next_word.pack(side='top', fill='x', expand=1)
        self.word_frame.pack(side='top', fill='both', expand=1)
        self.buttons_frame.pack(side='bottom', fill='both', expand=1)

    def refresh_classify(self):
        '''Sets the word labels to either be blank or to show
        the corresponding words. Also either creates the buttons
        for each category or destroys them if they exist,
        depending on whether a project is open.
        '''
        self.previous_word_var.set('previous')
        self.current_word_var.set('current')
        self.next_word_var.set('next')
        if self.cat_buttons:
            for button in self.cat_buttons:
                button.destroy()
        self.create_cat_buttons()

    def add_word_to_cat(self, event, cat_num, cat_name):
        '''Add the current word to the corresponding category,
        and get the next word.
        '''
        print(cat_num, cat_name)

    def next_word(self):
        '''Show the next word that is not yet in a wordlist and
        it's context and put it in next_word, moving the next_word
        to current_word, the current_word to previous_word and
        removing the previous_word. If the text has no new word,
        get the next text. If there is no next word, leave the
        next_word blank.
        '''
        pass

    def get_next_text(self):
        '''Get the next text from text_folder containing a word
        not yet present in the wordlists.

        ? Keep track somehow so you don't have to parse through
        ? everything all the time (like self.files_done)

        ? keep self.text and self.done_texts variables

        **Returns**:
        The text file as a string
        '''
        pass

    def is_in_wordlists(self, word):
        '''Check if the word is already in one of the categories /
        wordlists.

        **Returns**:
        True if the word is in one of the categories.
        '''
        for catname in self.master.categories:
            if word in self.master.categories[catname]:
                return True
        return False

    def create_cat_buttons(self):
        '''Create the buttons that add the current word to a specific
        category. It creates them dynamically and arranges them in
        as many columns as specified in max_button_cols.
        '''
        if self.master.project_currently_open():
            self.cat_names = list(self.master.categories.keys())
            self.cat_buttons = list()
            for i in range(self.master.n_cats):
                self.cat_buttons.append(ttk.Button(self.buttons_frame, text=self.cat_names[i] + f' ({i+1})', command=lambda event=0, b_num=i, b_name=self.cat_names[i]: self.add_word_to_cat(event, b_num, b_name)))
            for i in range(self.master.n_cats):
                self.cat_buttons[i].grid(row=int(i/self.max_button_cols), column=i%self.max_button_cols)
