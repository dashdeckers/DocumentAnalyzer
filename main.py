import tkinter as tk
import tkinter.ttk as ttk
import os
from tkinter import messagebox, filedialog
from extract_tab import ExtractTab
from classify_tab import ClassifyTab
from dataview_tab import DataviewTab
from popups import CreateProject
from utility import (
    create_spellchecker,
    file_folder,
    text_folder,
)

class DocumentClassifier(tk.Tk):
    '''
    TODO: Fill this in.
    '''
    def __init__(self):
        super().__init__()
        self.title('Document Classifier')
        self.geometry('800x800')
        self.notebook = ttk.Notebook(self)
        self.font_size = 12

        style = ttk.Style()
        style.configure('Example.TLabel', foreground='white', background='black')

        # Project data
        self.spell = create_spellchecker()
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
        self.menu_project.add_command(label='Create new project', command=self.show_new_project_popup, accelerator='Ctrl+N')
        self.menu_project.add_command(label='Open existing project', command=self.open_project, accelerator='Ctrl+O')
        self.menu_project.add_command(label='Synchronize current project', command=self.sync_project, accelerator='Ctrl+R')
        self.menu.add_cascade(label='Project', menu=self.menu_project)
        self.menu_edit = tk.Menu(self.menu, tearoff=0)
        self.menu_edit.add_command(label='Save & next document', command=self.extract.next_file, underline=1, accelerator='Ctrl+S')
        self.menu_edit.add_command(label='Redo current document', command=self.extract.reparse)
        self.menu_edit.add_command(label='Spellcheck', command=self.extract.spellcheck, underline=1, accelerator='Ctrl+P')
        self.menu.add_cascade(label='Edit', menu=self.menu_edit)

        # Packing
        self.notebook.add(self.extract, text='Extract Text')
        self.notebook.add(self.classify, text='Classify')
        self.notebook.add(self.dataview, text='View Data')
        self.notebook.pack(fill='both', expand=1)
        self.config(menu=self.menu)

        self.refresh_settings()

    def refresh_settings(self, event=None):
        '''Set both the status for each menu item as well as the
        correct keyboard bindings.

        Called every time the tab is switched and upon initialization.
        '''
        self.set_bindings()
        self.update_menu()

    def update_menu(self):
        '''Set the state of the menu items depending on whether a project
        is currently open or not.

        Only called by refresh_settings().
        '''
        if not self.project_currently_open():
            self.menu_project.entryconfig(2, state='disabled')
            for i in range(3):
                self.menu_edit.entryconfig(i, state='disabled')
        else:
            for i in range(3):
                self.menu_project.entryconfig(i, state='normal')
            if self.files_todo:
                for i in range(3):
                    self.menu_edit.entryconfig(i, state='normal')
            else:
                for i in range(3):
                    self.menu_edit.entryconfig(i, state='disabled')

    def set_bindings(self):
        '''Set the appropriate keyboard bindings depending on which tab the
        user is currently viewing.

        Only called by refresh_settings().

        TODO: Double check classify bindings + the check after filling in the functionality for the add_word function
        TODO: Put all keyboard bindings here, from all tabs to have a better overview
        '''
        self.notebook.bind('<<NotebookTabChanged>>', self.refresh_settings)
        self.notebook.bind('<Control-n>', self.show_new_project_popup)
        self.notebook.bind('<Control-o>', self.open_project)
        self.notebook.bind('<Control-r>', self.sync_project)

        self.extract.extract_text.bind('<ButtonRelease-1>', self.extract.show_corrections)
        self.extract.extract_text.bind('<Escape>', self.extract.hide_corrections)
        self.extract.extract_text.bind('<FocusOut>', self.extract.hide_corrections)
        self.extract.extract_text.bind('<Control-p>', self.extract.spellcheck)
        self.extract.extract_text.bind('<Control-s>', self.extract.next_file)
        self.extract.extract_text.bind('<Control-o>', self.open_project)
        self.extract.extract_text.bind('<Control-r>', self.sync_project)

        if self.n_cats and self.classify.cat_names:
            if self.notebook.tab(self.notebook.select(), 'text') == 'Classify':
                for i in range(self.n_cats):
                    self.bind(str(i+1), lambda event=0, b_num=i, b_name=self.classify.cat_names[i]: self.classify.add_word_to_cat(event, b_num, b_name))
            else:
                for i in range(self.n_cats):
                    self.unbind(str(i+1))

    def show_new_project_popup(self):
        '''Asks for user confirmation before clearing the current project
        and creating a new one via popup windows.

        Called by the user.

        TODO: Ask for confirmation
        '''
        if True:
            self.clear_current_project()
            CreateProject(self)

    def create_new_project(self):
        '''Creates a new project from internal data from user input obtained
        from popup windows.

        Called by the SetCategoryNames popup, which is called by the
        CreateProject popup.

        TODO: Make sure to write the full language name, and not the shortcut.
        '''
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

        self.refresh_settings()
        self.spell = create_spellchecker(self.language)
        self.title(self.project_name)
        self.classify.refresh_classify()
        self.dataview.refresh_dataview()
        self.extract.refresh_extract()

    def clear_current_project(self):
        '''Purges all internal project data.

        Called by open_project() and by show_new_project_popup().

        TODO: Make sure this purges the data from each tab as well
        '''
        self.title('Document Classifier')
        self.spell = create_spellchecker()
        self.files_todo = list()
        self.files_done = list()
        self.categories = dict()
        self.project_name = None
        self.language = None
        self.n_cats = None

        self.extract.filename_var.set('')
        self.extract.filenumber_var.set('')

        self.classify.cat_names = None
        self.classify.cat_buttons = None
        self.classify.previous_word_var.set('')
        self.classify.current_word_var.set('')
        self.classify.next_word_var.set('')

        self.dataview.selected_data_view.set('File History')
        self.dataview.data_view_selector['values'] = ['File History']
        self.dataview.data_view_selector.current(0)

        self.classify.refresh_classify()
        self.dataview.refresh_dataview()
        self.extract.refresh_extract()

    def parse_project_info_file(self, folder):
        '''Parses a project_info.txt file and incorporates the contained
        information.

        Only called by open_project().

        **Args**:

        * folder (str): The path to the project folder.

        **Returns**:
        True if no problems were encountered.
        '''
        try:
            # Read data
            with open(os.path.join(folder, 'project_info.txt'), 'r') as file:
                lines = [line.split() for line in file.read().splitlines()]

            # Make sure the main data has the valid format and parse it
            assert lines[0][0] == 'Project_name:', 'First line must start with "Project_name:"'
            assert lines[1][0] == 'Number_of_categories:', 'Second line must start with "Number_of_categories:"'
            assert lines[2][0] == 'Project_language:', 'Third line must start with "Project_language:"'
            assert not lines[3], 'Fourth line must be emmpty'
            assert lines[0][1] == os.path.split(folder)[-1], 'Folder name must be equal to the project name'
            self.n_cats = int(lines[1][1])
            self.project_name = lines[0][1]
            self.language = lines[2][1]

            # Make sure the category data has the valid format
            assert len(lines) == 4 + self.n_cats, 'Number_of_categories not consistent with number of lines describing category names'
            for cat in range(4, 4 + self.n_cats):
                self.categories[lines[cat][1]] = list()
            return True

        except ValueError:
            messagebox.showerror('Project info file error', f'Invalid "Number_of_categories" value in project info file. Must be an integer!')
            return False

        except AssertionError as e:
            messagebox.showerror('Project info file error', f'Problem with the project info file structure: {e}.')
            return False

        except FileNotFoundError as e:
            messagebox.showerror('Project info file error', f'The project info file (project_info.txt) is missing. Is this a valid project folder?')
            return False

    def open_project(self, event=None):
        '''Open a project folder selected by the user.

        Called by the user.

        TODO: Test if unsaved progress exists, notify the user.
        '''
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.clear_current_project()

        if self.parse_project_info_file(folder):
            self.sync_project()
            self.refresh_settings()
            self.spell = create_spellchecker(self.language)
            self.title(self.project_name)
            self.classify.refresh_classify()
            self.dataview.refresh_dataview()
            self.extract.refresh_extract()
        else:
            self.clear_current_project()

    def sync_project(self, event=None):
        '''Synchronize the project by synchronizing wordlists, filehistory
        and category wordlists.

        Called by the user and by open_project().
        '''
        if self.project_currently_open():
            self.sync_wordlists()
            self.sync_filehistory()
            self.sync_files()

    def sync_wordlists(self):
        '''Synchronizes the wordlists such that the category files contain
        the combined elements of the internal wordlists (self.categories) 
        and the category files, not allowing duplicates.

        Only called by sync_project().
        '''
        try:
            for catname in list(self.categories.keys()):
                with open(os.path.join('.', self.project_name, catname + '.txt'), 'r') as file:
                    catfile_contents = file.read().splitlines()
                    combined = self.categories[catname] + catfile_contents
                    no_duplicates = list()
                    for word in combined:
                        if word not in no_duplicates:
                            no_duplicates.append(word)

                with open(os.path.join('.', self.project_name, catname + '.txt'), 'w') as file:
                    for word in no_duplicates:
                        file.write(word + '\n')

                self.categories[catname] = no_duplicates

        except FileNotFoundError as e:
            messagebox.showerror('Category file error', f'A category file is missing: {e}.')

    def sync_filehistory(self):
        '''Adds the filenames present in self.files_done, and not already 
        present in filehistory.txt, to filehistory.txt.

        Only called by sync_project().
        '''
        try:
            with open(os.path.join('.', self.project_name, 'filehistory.txt'), 'r') as file:
                filehistory = file.read().splitlines()
                new_filehistory = filehistory + [file for file in self.files_done if file not in filehistory]

            with open(os.path.join('.', self.project_name, 'filehistory.txt'), 'w') as file:
                for filename in new_filehistory:
                    file.write(filename + '\n')

            self.files_done = new_filehistory

        except FileNotFoundError as e:
            messagebox.showerror('Filehistory file error', f'The file history file is missing: {e}.')

    def sync_files(self):
        '''Synchronises the files in the project folder (file_folder),
        and filehistory.txt with the internal lists self.files_done and 
        self.files_todo. The list of files present in the folder and NOT 
        listed in filehistory.txt will replace the self.files_todo list. 
        The list of files present in the folder and listed in
        filehistory.txt will replace the self.files_done list.

        Any entries in filehistory.txt that are not present in the file
        folder will be shown to the user. Any files in the file folder
        with an invalid extension will be shown to the user.

        Only called by sync_project().
        '''
        try:
            valid_extension = ('.pdf', '.txt', '.doc')
            files_directory = os.path.join('.', self.project_name, file_folder)

            files = [file for file in os.listdir(files_directory) if os.path.isfile(os.path.join(files_directory, file))]
            valid_files = list()
            invalid_files = list()
            for file in files:
                if file.endswith(valid_extension):
                    valid_files.append(file)
                else:
                    invalid_files.append(file)

            with open(os.path.join('.', self.project_name, 'filehistory.txt'), 'r') as file:
                filehistory = file.read().splitlines()

            self.files_done = [file for file in valid_files if file in filehistory]
            self.files_todo = [file for file in valid_files if file not in filehistory]

            filehistory_inconsistencies = [file for file in filehistory if file not in self.files_done]
            if filehistory_inconsistencies:
                messagebox.showerror('Filehistory error', f'There are files listed in filehistory that are not in the files folder: {[f for f in filehistory_inconsistencies]}.')
            if invalid_files:
                messagebox.showerror('Invalid extension', f'File must be either pdf, txt or doc. Skipping: {[f for f in invalid_files]}.')

            self.extract.refresh_extract()

        except FileNotFoundError as e:
            messagebox.showerror('Filehistory file error', f'The file history file is missing: {e}.')

    def project_currently_open(self):
        '''Checks if a project is currently open.

        Called by update_menu() and by sync_project().

        **Returns**:
        True if there is a project open.
        '''
        return self.project_name and self.n_cats and self.language

if __name__ == '__main__':
    App = DocumentClassifier()
    App.mainloop()
