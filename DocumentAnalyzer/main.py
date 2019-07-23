import tkinter as tk
import tkinter.ttk as ttk

from os import listdir, mkdir
from os.path import join, isfile, split
from tkinter import messagebox as msg
from tkinter import filedialog
from time import time

try:
    from DocumentAnalyzer.extract_tab import ExtractTab
    from DocumentAnalyzer.classify_tab import ClassifyTab
    from DocumentAnalyzer.results_tab import ResultsTab
    from DocumentAnalyzer.dataview_tab import DataviewTab
    from DocumentAnalyzer.popups import CreateProject
    from DocumentAnalyzer.utility import (
        create_spellchecker,
        file_folder,
        text_folder,
        strings,
    )
except ImportError as e:
    from extract_tab import ExtractTab
    from classify_tab import ClassifyTab
    from results_tab import ResultsTab
    from dataview_tab import DataviewTab
    from popups import CreateProject
    from utility import (
        create_spellchecker,
        file_folder,
        text_folder,
        strings,
    )


class DocumentAnalyzer(tk.Tk):
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
        style.configure('WORD.TLabel',
                        foreground='red')

        # Project data
        self.spell = None
        self.files_todo = list()
        self.files_done = list()
        self.categories = dict()
        self.project_name = None
        self.language = None
        self.n_cats = None

        # Tabs
        self.extract = ExtractTab(self)
        self.classify = ClassifyTab(self)
        self.results = ResultsTab(self)
        self.dataview = DataviewTab(self)

        # Menu
        self.menu = tk.Menu(self)
        self.menu_project = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Project', menu=self.menu_project)
        self.menu_edit = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Edit', menu=self.menu_edit)

        self.menu_project.add_command(label='Create new project',
                                      command=self.show_new_project_popup,
                                      accelerator='Ctrl+N')
        self.menu_project.add_command(label='Open existing project',
                                      command=self.open_project,
                                      accelerator='Ctrl+O')
        self.menu_project.add_command(label='Synchronize current project',
                                      command=self.sync_project,
                                      accelerator='Ctrl+R')
        self.menu_edit.add_command(label='Save & next document',
                                   command=self.extract.next_file,
                                   accelerator='Ctrl+S')
        self.menu_edit.add_command(label='Redo current document',
                                   command=self.extract.reparse)
        self.menu_edit.add_command(label='Spellcheck',
                                   command=self.extract.spellcheck,
                                   accelerator='Ctrl+P')

        # Packing
        self.notebook.add(self.extract, text='Extract Text')
        self.notebook.add(self.classify, text='Classify')
        self.notebook.add(self.results, text='Results')
        self.notebook.add(self.dataview, text='View Data')
        self.notebook.pack(fill='both', expand=1)
        self.config(menu=self.menu)

        self.refresh_settings()

    def refresh_settings(self, event=None):
        '''Set both the status for each menu item as well as the
        correct keyboard bindings and refresh the current tab.
        '''
        self.set_bindings()
        self.update_menu()

        current_tab = self.notebook.tab(self.notebook.select(), 'text')
        if current_tab == 'Extract Text':
            self.extract.refresh_extract()
        if current_tab == 'Classify':
            self.classify.refresh_classify()
        if current_tab == 'Results':
            self.results.refresh_results()
        if current_tab == 'View Data':
            self.dataview.refresh_dataview()

    def update_menu(self):
        '''Set the state of the menu items depending on whether a project
        is currently open or not.
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
        '''
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.notebook.bind('<<NotebookTabChanged>>', self.refresh_settings)
        self.notebook.bind('<Control-n>', self.show_new_project_popup)
        self.notebook.bind('<Control-o>', self.open_project)
        self.notebook.bind('<Control-r>', self.sync_project)

        self.extract.extract_text.bind('<Control-p>', self.extract.spellcheck)
        self.extract.extract_text.bind('<Control-s>', self.extract.next_file)
        self.extract.extract_text.bind('<Control-o>', self.open_project)
        self.extract.extract_text.bind('<Control-r>', self.sync_project)
        self.extract.extract_text.bind('<ButtonRelease-1>',
                                       self.extract.show_corrections)
        self.extract.extract_text.bind('<Escape>',
                                       self.extract.hide_corrections)
        self.extract.extract_text.bind('<FocusOut>',
                                       self.extract.hide_corrections)

        if self.notebook.tab(self.notebook.select(), 'text') == 'Classify':
            for i, catname in enumerate(list(self.categories.keys())):
                func = lambda _, c=catname: self.classify.add_word(_, c)
                self.bind(str(i+1), func)
        else:
            for i in range(len(self.categories)):
                self.unbind(str(i+1))

    def on_close(self):
        '''Ask the user for confirmation before quitting the program,
        if a project is open.
        '''
        if not self.project_currently_open():
            self.destroy()
        elif msg.askokcancel('Quit', strings['save_reminder']('Quit')):
            self.destroy()

    def show_new_project_popup(self):
        '''Asks for user confirmation before clearing the current project
        and creating a new one via popup windows.
        '''
        if not self.project_currently_open():
            self.clear_current_project()
            CreateProject(self)
        elif msg.askokcancel('New project',
                             strings['save_reminder']('create a project')):
            self.clear_current_project()
            CreateProject(self)

    def create_new_project(self):
        '''Creates a new project from internal data from user input obtained
        from popup windows.
        '''
        mkdir(join('.', self.project_name))
        mkdir(join('.', self.project_name, file_folder))
        mkdir(join('.', self.project_name, text_folder))
        
        # Create project info file
        project_info_path = join('.', self.project_name, 'project_info.txt')
        with open(project_info_path, 'w') as file:
            file.write(
                f'Project_name: {self.project_name}\n'
                f'Number_of_categories: {self.n_cats}\n'
                f'Project_language: {self.language}\n'
                '\n'
            )
            for catnum, catname in enumerate(list(self.categories.keys())):
                file.write(f'Category_{catnum+1}_name: {catname}\n')

                # Create the category / wordlist files
                catfile_path = join('.', self.project_name, f'{catname}.txt')
                with open(catfile_path, 'w') as catfile:
                    pass

        # Create file history file
        filehistory_path = join('.', self.project_name, 'filehistory.txt')
        with open(filehistory_path, 'w') as file:
            pass

        self.refresh_settings()
        t0 = time()
        self.spell = create_spellchecker(self.language)
        print(f'Loaded the spellchecker in {time()-t0}')
        self.title(self.project_name)
        self.classify.refresh_classify()
        self.dataview.refresh_dataview()
        self.extract.refresh_extract()

    def clear_current_project(self):
        '''Purges all internal project data.
        '''
        self.title('Document Classifier')
        self.spell = None
        self.files_todo = list()
        self.files_done = list()
        self.categories = dict()
        self.project_name = None
        self.language = None
        self.n_cats = None

        self.extract.filename_var.set('')
        self.extract.filenumber_var.set('')

        self.classify.destroy_cat_buttons()
        self.classify.cat_buttons = None
        self.classify.text_files_done = list()
        self.classify.text_tokens = list()
        self.classify.words_togo = list()
        self.classify.insert_next_context()

        self.results.res_labels = None
        self.results.res_values = dict()

        self.dataview.selected_data_view.set('File History')
        self.dataview.data_view_selector['values'] = ['File History']
        self.dataview.data_view_selector.current(0)

        self.classify.refresh_classify()
        self.dataview.refresh_dataview()
        self.extract.refresh_extract()

    def parse_project_info_file(self, folder):
        '''Parses a project_info.txt file and incorporates the contained
        information.

        **Args**:

        * folder (str): The path to the project folder.

        **Returns**:
        True if no problems were encountered.
        '''
        try:
            # Read data
            with open(join(folder, 'project_info.txt'), 'r') as file:
                lines = [line.split() for line in file.read().splitlines()]

            # Make sure the main data has the valid format and parse it
            assert lines[0][0] == 'Project_name:', strings['p_name_err']
            assert lines[1][0] == 'Number_of_categories:', strings['n_cat_err']
            assert lines[2][0] == 'Project_language:', strings['p_lang_err']
            assert not lines[3], strings['blank_line_err']
            assert lines[0][1] == split(folder)[-1], strings['folder_name_err']

            self.n_cats = int(lines[1][1])
            self.project_name = lines[0][1]
            self.language = lines[2][1]

            # Make sure the category data has the valid format and parse it
            assert len(lines) == 4 + self.n_cats, strings['n_cat_lines_err']

            for cat in range(4, 4 + self.n_cats):
                self.categories[lines[cat][1]] = list()
            return True

        except ValueError:
            msg.showerror('Project info file error',
                strings['n_cats_value_err'])
            return False

        except AssertionError as e:
            msg.showerror('Project info file error',
                strings['assertion_err'](e))
            return False

        except FileNotFoundError as e:
            msg.showerror('Project info file error',
                strings['project_file_missing'])
            return False

    def open_project(self, event=None):
        '''Open a project folder selected by the user.
        '''
        if self.project_currently_open() and not \
                msg.askokcancel('Switch project',
                                strings['save_reminder']('switch projects')):
            return

        folder = filedialog.askdirectory()
        if not folder:
            return

        self.clear_current_project()

        if self.parse_project_info_file(folder):
            t0 = time()
            self.spell = create_spellchecker(self.language)
            print(f'Loaded the spellchecker in {time()-t0}')
            self.sync_project()
            self.title(self.project_name)
            self.classify.refresh_classify()
            self.dataview.refresh_dataview()
            self.extract.refresh_extract()
            self.refresh_settings()
        else:
            self.clear_current_project()

    def sync_project(self, event=None):
        '''Synchronize the project by synchronizing wordlists, filehistory
        and category wordlists.
        '''
        if self.project_currently_open():
            self.sync_wordlists()
            self.sync_filehistory()
            self.sync_files()

    def sync_wordlists(self):
        '''Synchronizes the wordlists such that the category files contain
        the combined elements of the internal wordlists (self.categories) 
        and the category files, not allowing duplicates.
        '''
        try:
            for catname in list(self.categories.keys()):
                catfile_path = join('.', self.project_name, catname + '.txt')

                with open(catfile_path, 'r') as file:
                    catfile_contents = file.read().splitlines()
                    combined = self.categories[catname] + catfile_contents
                    no_duplicates = list()
                    for word in combined:
                        if word not in no_duplicates:
                            no_duplicates.append(word)

                with open(catfile_path, 'w') as file:
                    for word in no_duplicates:
                        file.write(word + '\n')

                self.categories[catname] = no_duplicates

        except FileNotFoundError as e:
            msg.showerror('Category file error', 
                strings['cat_file_missing'](e))

        except BrokenPipeError as e:
            msg.showerror('Unknown Error',
                strings['broken_pipe_err'])

    def sync_filehistory(self):
        '''Adds the filenames present in self.files_done, and not already 
        present in filehistory.txt, to filehistory.txt.
        '''
        try:
            filehistory_path = join('.', self.project_name, 'filehistory.txt')

            with open(filehistory_path, 'r') as file:
                fh = file.read().splitlines()
                new_fh = fh + [f for f in self.files_done if f not in fh]

            with open(filehistory_path, 'w') as file:
                for filename in new_fh:
                    file.write(filename + '\n')

            self.files_done = new_fh

        except FileNotFoundError as e:
            msg.showerror('Filehistory file error',
                strings['filehistory_missing'](e))

    def sync_files(self):
        '''Synchronises the files in the project folder (file_folder)
        and filehistory.txt with the internal lists self.files_done and 
        self.files_todo. The list of files present in the folder and NOT 
        listed in filehistory.txt will replace the self.files_todo list. 
        The list of files present in the folder and listed in
        filehistory.txt will replace the self.files_done list.

        Any entries in filehistory.txt that are not present in the file
        folder will be shown to the user. Any files in the file folder
        with an invalid extension will be shown to the user.
        '''
        try:
            valid_extension = ('.pdf', '.txt', '.doc')
            f_dir = join('.', self.project_name, file_folder)

            files = [f for f in listdir(f_dir) if isfile(join(f_dir, f))]
            valid_files = list()
            invalid_files = list()
            for file in files:
                if file.endswith(valid_extension):
                    valid_files.append(file)
                else:
                    invalid_files.append(file)

            filehistory_path = join('.', self.project_name, 'filehistory.txt')
            with open(filehistory_path, 'r') as file:
                filehistory = file.read().splitlines()

            self.files_done = [f for f in valid_files if f in filehistory]
            self.files_todo = [f for f in valid_files if f not in filehistory]

            inconsistencies = [f for f in filehistory 
                                    if f not in self.files_done]
            if inconsistencies:
                msg.showerror('Filehistory error',
                    strings['filehist_inconsistency'](inconsistencies))
            if invalid_files:
                msg.showerror('Invalid extension',
                    strings['invalid_extension'](invalid_files))

            self.extract.refresh_extract()

        except FileNotFoundError as e:
            msg.showerror('Filehistory file error',
                strings['filehistory_missing'](e))

    def project_currently_open(self):
        '''Checks if a project is currently open.

        **Returns**:
        True if there is a project open.
        '''
        return self.project_name and self.n_cats and self.language

def main():
    App = DocumentAnalyzer()
    App.mainloop()

if __name__ == '__main__':
    main()