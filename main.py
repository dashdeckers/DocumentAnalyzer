import tkinter as tk
import tkinter.ttk as ttk
import os
from tkinter import messagebox, filedialog
from extract_tab import ExtractTab
from classify_tab import ClassifyTab
from dataview_tab import DataviewTab
from popups import CreateProject, SetCategoryNames
from utility import (
    create_spellchecker,
    file_folder,
    text_folder,
)

class DocumentClassifier(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Document Classifier')
        self.geometry('800x800')
        self.notebook = ttk.Notebook(self)
        self.spell = create_spellchecker()
        self.font_size = 12

        style = ttk.Style()
        style.configure('Example.TLabel', foreground='white', background='black')

        # Project data
        self.files_todo = list()
        self.files_done = list()
        self.categories = dict()
        self.project_name = None
        self.language = None
        self.n_cats = None

        # Tabs
        self.extract = ExtractTab(self)
        self.classify = ClassifyTab(self)
        self.dataview = DataviewTab(self)

        # Menu
        self.menu = tk.Menu(self)
        self.menu_project = tk.Menu(self.menu, tearoff=0)
        self.menu_project.add_command(label='Create new project', command=lambda slf=self: CreateProject(slf))
        self.menu_project.add_command(label='Open existing project', command=self.open_project)
        self.menu_project.add_command(label='Save current project', command=self.save_project)
        self.menu_project.add_command(label='Clear current project', command=self.clear_project)
        self.menu_project.add_command(label='Import files to current project', command=self.import_files)
        self.menu.add_cascade(label='Project', menu=self.menu_project)
        self.menu_edit = tk.Menu(self.menu, tearoff=0)
        self.menu_edit.add_command(label='Clear file history', command=self.clear_file_history)
        self.menu_edit.add_command(label='Clear word lists', command=self.clear_word_lists)
        self.menu_edit.add_command(label='Save text and next document', command=self.next_file)
        self.menu_edit.add_command(label='Discard text and extract again', command=self.reparse)
        self.menu_edit.add_command(label='Spellcheck', command=self.extract.spellcheck)
        self.menu.add_cascade(label='Edit', menu=self.menu_edit)

        # Packing
        self.notebook.add(self.extract, text='Extract Text')
        self.notebook.add(self.classify, text='Classify')
        self.notebook.add(self.dataview, text='View Data')
        self.notebook.pack(fill='both', expand=1)
        self.notebook.bind('<<NotebookTabChanged>>', self.refresh_settings)
        self.config(menu=self.menu)

    def refresh_project(self):
        if self.language:
            self.spell = create_spellchecker(self.language)
        else:
            self.spell = create_spellchecker()

        if self.project_name:
            self.title(self.project_name)
        else:
            self.title('Document Classifier')

        self.classify.refresh_classify()
        self.dataview.refresh_dataview()
        self.extract.refresh_extract()

    def refresh_settings(self, event=None):
        self.set_bindings()
        self.update_menu()

    def update_menu(self):
        if not all((self.project_name, self.language, self.n_cats)):
            for i in range(2, 5):
                self.menu_project.entryconfig(i, state='disabled')
            for i in range(5):
                self.menu_edit.entryconfig(i, state='disabled')
        else:
            for i in range(5):
                self.menu_project.entryconfig(i, state='normal')
            for i in range(2):
                self.menu_edit.entryconfig(i, state='normal')
            if self.files_todo:
                for i in range(2, 5):
                    self.menu_edit.entryconfig(i, state='normal')
            else:
                for i in range(2, 5):
                    self.menu_edit.entryconfig(i, state='disabled')

    def set_bindings(self):
        # TODO: Double check this (+ the check) after filling in the functionality for that function
        if self.n_cats and self.classify.cat_names:
            if self.notebook.tab(self.notebook.select(), 'text') == 'Classify':
                for i in range(self.n_cats):
                    self.bind(str(i+1), lambda event=0, b_num=i, b_name=self.classify.cat_names[i]: self.classify.add_word_to_cat(event, b_num, b_name))
            else:
                for i in range(self.n_cats):
                    self.unbind(str(i+1))

    def create_new_project(self):
        # Create folders
        os.mkdir(os.path.join('.', self.project_name))
        os.mkdir(os.path.join('.', self.project_name, file_folder))
        os.mkdir(os.path.join('.', self.project_name, text_folder))
        # Create project info file
        with open(os.path.join('.', self.project_name, 'project_info.txt'), 'w') as file:
            file.write(
                f'Project_name: {self.project_name}\n'
                f'Number_of_categories: {self.n_cats}\n'
                f'Project_language: {self.language}\n'
                '\n'
            )
            for catnum, catname in enumerate(list(self.categories.keys())):
                file.write(f'Category_{catnum}_name: {catname}\n')
                # Create the category / wordlist files
                with open(os.path.join('.', self.project_name, f'{catname}.txt'), 'w') as catfile:
                    pass
        # Create file history file
        with open(os.path.join('.', self.project_name, 'filehistory.txt'), 'w') as file:
            pass

    def parse_project_info_file(self, folder):
        try:
            # Read data
            with open(os.path.join('.', folder, 'project_info.txt'), 'r') as file:
                lines = [line.split() for line in file.read().splitlines()]

            # Make sure the main data has the valid format and parse it
            assert lines[0][0] == 'Project_name:', 'Name problem'
            assert lines[1][0] == 'Number_of_categories:', 'Catnum problem'
            assert lines[2][0] == 'Project_language:', 'Language problem'
            assert not lines[3]
            self.n_cats = int(lines[1][1])
            self.project_name = lines[0][1]
            self.language = lines[2][1]

            # Make sure the category data has the valid format
            assert len(lines) == 4 + self.n_cats, 'Catnames problem'
            for cat in range(4, 4 + self.n_cats):
                self.categories[lines[cat][1]] = list()
            return True

        except (ValueError, AssertionError, FileNotFoundError) as e:
            print('ERROR:', e)
            return False

    def open_project(self):
        # TODO: Test if unsaved progress exists, notify the user
        folder = filedialog.askdirectory()

        try:
            # Parse project info file
            assert self.parse_project_info_file(folder), 'Invalid project_info file'

            # Update the spellchecker language
            self.spell = create_spellchecker(self.language)

            # Update category wordlists
            for catname in list(self.categories.keys()):
                with open(os.path.join('.', folder, f'{catname}.txt'), 'r') as file:
                    wordlist = file.read().splitlines()
                self.categories[catname] = wordlist

            # Update list of filenames from document folder
            filenames = os.listdir(os.path.join('.', folder, file_folder))

            # Update the file history
            with open(os.path.join('.', folder, 'filehistory.txt'), 'r') as file:
                done_filenames = file.read().splitlines()
            self.files_done = done_filenames
            self.files_todo = list(set(filenames) - set(done_filenames))

            # Update internal stuff
            self.extract.update_fileprogress()
            self.refresh_project()

        except (AssertionError, FileNotFoundError) as e:
            print('ERROR:', e)
            messagebox.showerror('Problem loading project', 'Something went wrong loading the project, please make sure the structure is valid')

    def save_project(self):
        # Save wordlists, file history, current text
        print('Saving project')

    def clear_project(self):
        # Remind user what he is doing (make sure)
        # Delete: 
        # All saved text files
        # Wordlists
        # File history
        # Results
        print('Clearing project')

    def import_files(self):
        # TODO: Change this to just import files from the pdf folder of the current project
        valid_extension = ('.pdf', '.txt', '.doc')

        files = filedialog.askopenfilenames()

        for file in files:
            if file.endswith(valid_extension):
                self.files_todo.append(file)
            else:
                messagebox.showerror('Invalid extension', f'File must be either pdf, txt or doc. Skipping {file}.')

        self.extract.refresh_extract()

        # Import (copy) all valid files into project folder
        print('Importing files')

    def clear_word_lists(self):
        # Remind user what he is doing (make sure)
        print('Clearing word lists')

    def clear_file_history(self):
        # Remind user what he is doing (make sure)
        print('Clearing file history')

    def next_file(self):
        # Save the text with the same filename in text folder
        # Extract text from next file
        print('Saving and parsing the next file')

    def reparse(self):
        # Remind user what he is doing (make sure)
        # Extract text from the current file and replace the current text
        print('Discarding text and parsing the file again')


if __name__ == '__main__':
    App = DocumentClassifier()
    App.mainloop()
