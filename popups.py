import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as msg
from utility import language_dict

class CreateProject(tk.Toplevel):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self.title('Create a new project')
        self.geometry('300x150')

        self.name_label = tk.Label(self, text='Project Name')
        self.name_entry = tk.Entry(self)
        self.lang_label = tk.Label(self, text='Project Language')
        self.lang_entry = tk.Entry(self)
        self.catnum_label = tk.Label(self, text='Number of Categories')
        self.catnum_entry = tk.Entry(self)

        self.create_button = tk.Button(self, text='Create Project', command=self.create_project)
        self.name_entry.focus()

        self.name_label.pack()
        self.name_entry.pack()
        self.lang_label.pack()
        self.lang_entry.pack()
        self.catnum_label.pack()
        self.catnum_entry.pack()
        self.create_button.pack()

    def create_project(self):
        if self.valid_name() and self.valid_language() and self.valid_n_cats():
            self.master.project_name = self.name_entry.get()
            self.master.language = self.lang_entry.get()
            self.master.n_cats = int(self.catnum_entry.get())
            print('Creating Project')
            SetCategoryNames(self.master)
            self.destroy()

    def valid_name(self):
        name = self.name_entry.get()
        if not all(char.isalpha() or char.isspace() for char in name):
            msg.showerror('Error', 'Project name must be alphabetical')
            return False
        return True

    def valid_language(self):
        lang = self.lang_entry.get()
        if not lang in language_dict:
            msg.showerror('Error', 'Invalid language')
            return False
        return True

    def valid_n_cats(self):
        try:
            n_cats = int(self.catnum_entry.get())
            return True
        except ValueError:
            msg.showerror('Error', 'Number of categories must be an integer')
            return False

class SetCategoryNames(tk.Toplevel):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self.title('Category names')

        self.labels = list()
        self.entries = list()
        for i in range(self.master.n_cats):
            self.labels.append(ttk.Label(self, text=f'Category {i} name'))
            self.entries.append(tk.Entry(self))

        for i in range(self.master.n_cats):
            self.labels[i].pack()
            self.entries[i].pack()

        create_button = tk.Button(self, text='Done', command=self.create_cats)
        create_button.pack()

        self.entries[0].focus()

    def create_cats(self):
        for i in range(self.master.n_cats):
            self.master.categories[self.entries[i].get()] = list()
        self.destroy()
        self.master.refresh_project()