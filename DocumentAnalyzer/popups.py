import tkinter as tk
import tkinter.ttk as ttk

from tkinter.font import Font
from tkinter import messagebox as msg

try:
    from DocumentAnalyzer.utility import (
        language_dict,
        strings,
    )
except ImportError as e:
    from utility import (
        language_dict,
        strings,
    )

class CreateProject(tk.Toplevel):
    '''
    Create a new project popup window.
    '''
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.title('Create a new project')
        self.geometry('300x250')

        # GUI stuff
        self.name_label = tk.Label(self, text='Project Name')
        self.name_entry = tk.Entry(self)
        self.lang_label = tk.Label(self, text='Project Language')

        languages = [l.title() for l in language_dict.keys() if len(l) > 2]
        self.lang_entry = tk.StringVar(self, languages[0])
        self.lang_dmenu = tk.OptionMenu(self,
                                        self.lang_entry,
                                        *languages)

        self.catnum_label = tk.Label(self, text='Number of Categories')
        self.catnum_entry = tk.Spinbox(self,
                                       from_=1,
                                       to=99,
                                       width=3,
                                       font=Font(family='Helvetica', size=11),
                                       state='readonly')

        self.create_button = tk.Button(self,
                                       text='Create Project',
                                       command=self.create_project)
        self.bind('<Return>', self.create_project)
        self.name_entry.focus()

        # Packing
        self.name_label.pack()
        self.name_entry.pack(pady=5)
        self.lang_label.pack()
        self.lang_dmenu.pack(pady=5)
        self.catnum_label.pack()
        self.catnum_entry.pack(pady=5)
        self.create_button.pack(pady=15)

    def create_project(self, event=None):
        '''Sets the project name, number of categories and language based
        on user input, and then creates the popup window to determine category
        names. If the language was given as the two letter shortcut, convert
        it to its full name.
        '''
        if self.valid_name() and self.valid_language() and self.valid_n_cats():
            lang = self.lang_entry.get()
            language = lang if len(lang) > 2 else language_dict[lang]

            self.master.project_name = self.name_entry.get()
            self.master.language = language
            self.master.n_cats = int(self.catnum_entry.get())
            self.destroy()
            SetCategoryNames(self.master)

    def valid_name(self):
        '''Checks that the project name is valid. A project name can only
        contain alphanumerical characters, spaces, hyphens or underscores.

        **Returns**:
        True if the name is valid.
        '''
        name = self.name_entry.get()
        if not all(char.isalnum() 
                    or char.isspace() 
                    or char in ['_', '-'] 
                    for char in name):
            msg.showerror('Invalid input error', strings['invalid_name'])
            return False
        return True

    def valid_language(self):
        '''Checks that the project language is valid. The language can only be
        one of a predefined set of languages (see language_dict in utility),
        either in form of the two letter shortcut or the full language name.

        **Returns**:
        True if the language is valid.
        '''
        lang = self.lang_entry.get()
        if not lang.lower() in language_dict:
            msg.showerror('Invalid input error', strings['invalid_language'])
            return False
        return True

    def valid_n_cats(self):
        '''Checks that the number of categories is valid. The number of
        categories must be an integer.

        **Returns**:
        True if the name is valid.
        '''
        try:
            n_cats = int(self.catnum_entry.get())
            return True

        except ValueError:
            msg.showerror('Invalid input error', strings['invalid_n_cats'])
            return False

class SetCategoryNames(tk.Toplevel):
    '''
    Set category names (create new project part 2) popup window.
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
        master.create_new_project() to create project folder from internal
        data.
        '''
        for i in range(self.master.n_cats):
            self.master.categories[self.entries[i].get()] = list()

        # Always make an extra discard and discuss categories
        self.master.categories['discard'] = list()
        self.master.categories['discuss'] = list()
        self.master.n_cats += 2

        self.destroy()
        self.master.create_new_project()

class FindDelete(tk.Toplevel):
    '''
    Find or delete a string from the text popup window.
    '''
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.title('Find or Delete')
        self.minsize(width=300, height=0)

        # GUI stuff
        self.entry = tk.Entry(self, text='Enter a word or phrase')
        self.btn_frame = tk.Frame(self)
        self.find_btn = tk.Button(self.btn_frame,
                                  text='Find',
                                  command=self.find)
        self.delete_btn = tk.Button(self.btn_frame,
                                    text='Delete',
                                    command=self.delete)
        self.bind('<Return>', self.find)
        self.entry.focus()

        # Packing
        self.entry.pack(side='top', fill='x', expand=1)
        self.find_btn.pack(side='left', fill='both', expand=1)
        self.delete_btn.pack(side='right', fill='both', expand=1)
        self.btn_frame.pack(side='bottom', fill='x', expand=1)

    def find(self, event=None):
        '''Wrapper to call the find function.
        '''
        string = self.entry.get()
        self.master.extract.find(string)
        self.entry.delete(0, 'end')

    def delete(self, event=None):
        '''Wrapper to call the delete function.
        '''
        string = self.entry.get()
        if msg.askokcancel('Delete', strings['delete_confirmation'](string)):
            self.master.extract.delete(string)
        self.entry.delete(0, 'end')
