import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
from extract_tab import ExtractTab
from classify_tab import ClassifyTab
from dataview_tab import DataviewTab
from popups import CreateProject, SetCategoryNames
from utility import create_spellchecker

class DocumentClassifier(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Document Classifier')
        self.geometry('800x1000')
        self.font_size = 12

        self.categories = dict()

        style = ttk.Style()
        style.configure('Example.TLabel', foreground='white', background='black')

        self.notebook = ttk.Notebook(self)
        self.spell = create_spellchecker()
        self.project_name = None
        self.language = None
        self.n_cats = None

        # Menu
        self.menu = tk.Menu(self)
        self.menu_projects = tk.Menu(self.menu, tearoff=0)
        self.menu_projects.add_command(label='Create new project', command=self.create_new_project)
        self.menu_projects.add_command(label='Open existing project', command=self.open_project)
        self.menu_projects.add_command(label='Save current project', command=self.save_project)
        self.menu_projects.add_command(label='Clear current project', command=self.clear_project)
        self.menu_projects.add_command(label='Import files to current project', command=self.import_files)
        self.menu.add_cascade(label='Project', menu=self.menu_projects)
        self.menu_edits = tk.Menu(self.menu, tearoff=0)
        self.menu_edits.add_command(label='Clear file history', command=self.clear_file_history)
        self.menu_edits.add_command(label='Clear word lists', command=self.clear_word_lists)
        self.menu_edits.add_command(label='Save text and next document', command=self.next_file)
        self.menu_edits.add_command(label='Discard text and extract again', command=self.reparse)
        self.menu.add_cascade(label='Edit', menu=self.menu_edits)

        # Tabs
        self.extract = ExtractTab(self)
        self.classify = ClassifyTab(self)
        self.dataview = DataviewTab(self)

        # Packing
        self.notebook.add(self.extract, text='Extract Text')
        self.notebook.add(self.classify, text='Classify')
        self.notebook.add(self.dataview, text='View Data')
        self.notebook.pack(fill='both', expand=1)
        self.notebook.bind('<<NotebookTabChanged>>', self.set_bindings)
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

    def set_bindings(self, event=None):
        if self.n_cats and self.classify.cat_names:
            if self.notebook.tab(self.notebook.select(), 'text') == 'Classify':
                for i in range(self.n_cats):
                    self.bind(str(i+1), lambda event=0, b_num=i, b_name=self.classify.cat_names[i]: self.classify.add_word_to_cat(event, b_num, b_name))
            else:
                for i in range(self.n_cats):
                    self.unbind(str(i+1))

    def create_new_project(self):
        CreateProject(self)
        # Create the folder structure
        # Make the info file
        # Show 'Import pdfs/files via menu' in text field
        print('Creating new project')

    def open_project(self):
        # Test if unsaved progress exists, notify the user
        # Pop up window to select a folder
        # Test whether it is a valid folder (return 'what is missing')
        #
        # Then set internal settings:
        # Set spellchecker to the correct language
        # Set the categories (dict?)
        # Retrieve a list of pdf filenames
        # Retrieve the file history list
        # Retrieve the project name (just to show in the title)
        # Set the current filename and filenumber, and show its text
        print('Opening project')

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
        folder = filedialog.askdirectory()
        print(folder)

        # Pop up to choose a folder with the files
        # Import (copy) all valid files into project folder
        # Update the list of filenames
        # Valid files are pdfs, text files and doc files
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
