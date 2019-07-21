import tkinter as tk
import tkinter.ttk as ttk

from tkinter import messagebox as msg
from utility import language_dict

class CreateProject(tk.Toplevel):
    '''
    TODO: Fill this in.
    '''
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.title('Create a new project')
        self.geometry('300x200')

        # GUI stuff
        self.name_label = tk.Label(self, text='Project Name')
        self.name_entry = tk.Entry(self)
        self.lang_label = tk.Label(self, text='Project Language')
        self.lang_entry = tk.Entry(self)
        self.catnum_label = tk.Label(self, text='Number of Categories')
        self.catnum_entry = tk.Entry(self)

        self.create_button = tk.Button(self, text='Create Project', command=self.create_project)
        self.bind('<Return>', self.create_project)
        self.name_entry.focus()

        # Packing
        self.name_label.pack()
        self.name_entry.pack()
        self.lang_label.pack()
        self.lang_entry.pack()
        self.catnum_label.pack()
        self.catnum_entry.pack()
        self.create_button.pack()

    def create_project(self, event=None):
        '''Sets the project name, number of categories and language based
        on user input, and then creates the popup window to determine category
        names.
        '''
        if self.valid_name() and self.valid_language() and self.valid_n_cats():
            self.master.project_name = self.name_entry.get()
            self.master.language = self.lang_entry.get()
            self.master.n_cats = int(self.catnum_entry.get())
            self.destroy()
            SetCategoryNames(self.master)

    def valid_name(self):
        '''Checks that the project name is valid. A project name can only contain
        alphanumerical characters, spaces, hyphens or underscores.

        **Returns**:
        True if the name is valid.
        '''
        name = self.name_entry.get()
        if not all(char.isalnum() or char.isspace() or char in ['_', '-'] for char in name):
            msg.showerror('Invalid input error', 'Project name must be alphabetical, or with spaces, underscores or hyphens')
            return False
        return True

    def valid_language(self):
        '''Checks that the project language is valid. The language can only be one
        of a predefined set of languages (see language_dict in utility), either in
        form of the two letter shortcut or the full language name.

        **Returns**:
        True if the language is valid.
        '''
        lang = self.lang_entry.get()
        if not lang.lower() in language_dict:
            msg.showerror('Invalid input error', 'Invalid language')
            return False
        return True

    def valid_n_cats(self):
        '''Checks that the number of categories is valid. The number of categories
        must be an integer.

        **Returns**:
        True if the name is valid.
        '''
        try:
            n_cats = int(self.catnum_entry.get())
            return True

        except ValueError:
            msg.showerror('Invalid input error', 'Number of categories must be an integer')
            return False

class SetCategoryNames(tk.Toplevel):
    '''
    TODO: Fill this in.
    '''
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.title('Category names')
        self.minsize(width=300, height=0)

        # GUI stuff
        self.labels = list()
        self.entries = list()
        for i in range(self.master.n_cats):
            self.labels.append(ttk.Label(self, text=f'Category {i+1} name'))
            self.entries.append(tk.Entry(self))

        create_button = tk.Button(self, text='Done', command=self.create_cats)
        self.bind('<Return>', self.create_cats)
        self.entries[0].focus()

        # Packing
        for i in range(self.master.n_cats):
            self.labels[i].pack()
            self.entries[i].pack()
        create_button.pack()

    def create_cats(self, event=None):
        '''Sets the categories based on the user input, then calls
        master.create_new_project() to create project folder from internal data.
        '''
        for i in range(self.master.n_cats):
            self.master.categories[self.entries[i].get()] = list()
        self.destroy()
        self.master.create_new_project()
