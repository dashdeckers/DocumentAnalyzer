from tkinter import ttk
from tkinter import messagebox
from functools import partial
from spellchecker import SpellChecker
import tkinter as tk

# TODO:

# Pop up message on close (unsaved progress)

# Make sure you can only access the right menu items in the right tab with
# print(self.notebook.tab(self.notebook.select(), 'text'))
# print(self.notebook.index(self.notebook.select()))




# Open an existing project:

# Resumes where you left off with the next file that has not been extracted yet
# (for that, look at file history)

# To start again, clear file history and it starts again at the beginning, but if
# it finds an existing text file it shows that instead of reparsing

# For more fine tuned control over which files to re-do and skip, edit the file
# history file



# Create a new project:

# Creates a folder following user specifications
# User adds one or more folders full of pdfs via the menu
# Follow the flow

class Notebook(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Here's a title")
		self.geometry('800x1000')
		self.font_size = 12

		style = ttk.Style()
		style.configure('Example.TLabel', foreground='white', background='black')

		self.notebook = ttk.Notebook(self)
		self.spell = SpellChecker()

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

		# Extract text tab
		self.filename_var = tk.StringVar(self, 'filename')
		self.filenumber_var = tk.StringVar(self, '1/10') # should maybe be blank?
		self.extract = ttk.Frame(self.notebook)
		self.extract_filefield = ttk.Frame(self.extract)
		self.extract_filename = ttk.Label(self.extract_filefield, textvar=self.filename_var, anchor='w')
		self.extract_filenumber = ttk.Label(self.extract_filefield, textvar=self.filenumber_var, anchor='e')
		self.extract_text = tk.Text(self.extract, bg='white', fg='black', font=(None, self.font_size))
		self.scrollbar = tk.Scrollbar(self.extract, orient='vertical')
		self.extract_text.configure(yscrollcommand=self.scrollbar.set)
		self.extract_text.insert('1.0', 'Import files via the menu to get started')
		self.extract_text.bind('<ButtonRelease-1>', self.show_corrections)
		self.extract_text.focus_force()

		# Classify tab
		self.classify = ttk.Frame(self.notebook)
		self.classify_label = ttk.Label(self.classify, text='Whaaaat', style='Example.TLabel')

		# Packing
		self.extract_filename.pack(side='left', fill='both')
		self.extract_filenumber.pack(side='right', fill='both')
		self.extract_filefield.pack(side='bottom', fill='both')
		self.scrollbar.pack(side='right', fill='y')
		self.extract_text.pack(side='top', fill='both', expand=1)

		self.classify_label.pack(side='top', fill='both', expand=1)

		self.notebook.add(self.extract, text='Extract Text')
		self.notebook.add(self.classify, text='Classify')
		self.notebook.pack(fill='both', expand=1)
		self.config(menu=self.menu)

	def get_correction_menu_coords(self):
		bbox = self.extract_text.bbox('insert')
		menu_x = bbox[0] + self.winfo_x() + self.extract_text.winfo_x()
		menu_y = bbox[1] + self.winfo_y() + self.extract_text.winfo_y() + self.font_size
		return (menu_x, menu_y)

	def get_corrections(self, word):
		# TODO: This needs to be filtered to show suggestions ranked based on distance
		candidates = list(self.spell.candidates(word))
		if len(candidates) > 10:
			return candidates[:10]
		else:
			return candidates

	def show_corrections(self, event=None):
		# Get the word at the index
		index = self.extract_text.index('insert')
		try:
			word = self.extract_text.get(index + ' wordstart', index + ' wordend')
		except tk.TclError:
			word = ''

		# If the word is spelled incorrectly
		if word and len(word) > 1 and self.spell.unknown([word]):
			# Make sure we don't have two menus open
			self.hide_corrections()
			self.corrections_menu = tk.Menu(self, tearoff=0)

			# Get the possible corrections and add them to the menu
			corrections = self.get_corrections(word)
			for word in corrections:
				callback = partial(self.replace_word, word=word, index=index)
				self.corrections_menu.add_command(label=word, command=callback)

			# Put the menu where it belongs and bind the relevant keys
			x, y = self.get_correction_menu_coords()
			self.corrections_menu.post(x, y)
			self.corrections_menu.bind('<Escape>', self.hide_corrections)
			self.extract_text.bind('<Down>', self.focus_corrections_menu)

	def hide_corrections(self):
		try:
			self.corrections_menu.destroy()
			self.extract_text.unbind('<Down>')
			self.extract_text.focus_force()
		except AttributeError:
			pass

	def focus_corrections_menu(self, event=None):
		# TODO: Highlight selection, enter binding, check if down works
		try:
			self.corrections_menu.focus_force()
			self.corrections_menu.entryconfig(0, state='active')
		except tk.TclError:
			pass

	def replace_word(self, word, index):
		# TODO: Somehow find the actual index of wordstart to properly replace
		self.extract_text.delete(index + ' wordstart', index + ' wordend')
		self.extract_text.insert(index + ' wordstart', word)


	def create_new_project(self):
		# Pop up window to retrieve following information:
		# Language
		# Number of categories (+ names)
		# Project name
		#
		# Then, 
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
	App = Notebook()
	App.mainloop()








'''
# OLD SPELLCHECK BAR

		self.context_rvar = tk.StringVar(self, 'Context right') # all this can be replaced by a menu with corrections that pops up upon clicking the error
		self.context_lvar = tk.StringVar(self, 'Context left')
		self.correction_var = tk.StringVar(self, 'spelng mitsake')
		self.spellcheck_field = ttk.Frame(self.extract)
		self.spellcheck_cl = ttk.Label(self.spellcheck_field, textvar=self.context_lvar)	
		self.spellcheck_cr = ttk.Label(self.spellcheck_field, textvar=self.context_rvar)
		self.spellcheck_word = ttk.Label(self.spellcheck_field, textvar=self.correction_var)

		...

		self.spellcheck_field.pack(side='bottom', fill='both', pady=10) 
		self.spellcheck_cl.pack(side='left', fill='y')
		self.spellcheck_cr.pack(side='right', fill='y')
		self.spellcheck_word.pack(fill='y') # could put these in frames to center the labels within?




'''