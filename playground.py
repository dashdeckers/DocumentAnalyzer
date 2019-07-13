from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

class Notebook(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Here's a title")
		self.geometry("800x1000")

		style = ttk.Style()
		style.configure('Example.TLabel', foreground='white', background='black')

		self.notebook = ttk.Notebook(self)

		self.menu = tk.Menu(self)
		self.menu_projects = tk.Menu(self.menu, tearoff=0)
		self.menu_projects.add_command(label="Create new project", command=self.create_new_project)
		self.menu_projects.add_command(label="Switch projects", command=self.switch_projects)
		self.menu.add_cascade(label="Project", menu=self.menu_projects)
		self.menu_edits = tk.Menu(self.menu, tearoff=0)
		self.menu_edits.add_command(label="Clear file history", command=self.clear_file_history)
		self.menu_edits.add_command(label="Clear word lists", command=self.clear_word_lists)
		self.menu.add_cascade(label="Edit", menu=self.menu_edits)

		self.extract = ttk.Frame(self.notebook)
		self.extract_filefield = ttk.Frame(self.extract)
		self.extract_filename = ttk.Label(self.extract_filefield, text="filename", anchor=tk.W)
		self.extract_filenumber = ttk.Label(self.extract_filefield, text="1/10", anchor=tk.E)
		self.extract_textfield = tk.Text(self.extract)

		self.classify = ttk.Frame(self.notebook)
		self.classify_label = ttk.Label(self.classify, text="Whaaaat", style="Example.TLabel")

		# Packing
		self.extract_filefield.pack(side=tk.BOTTOM, fill=tk.BOTH)
		self.extract_filename.pack(side=tk.LEFT, fill=tk.BOTH)
		self.extract_filenumber.pack(side=tk.RIGHT, fill=tk.BOTH)
		self.extract_textfield.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

		self.classify_label.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
		self.notebook.add(self.extract, text="Extract Text")
		self.notebook.add(self.classify, text="Classify")
		self.notebook.pack(fill=tk.BOTH, expand=1)
		self.config(menu=self.menu)

	def create_new_project(self):
		print("Creating new project...")

	def switch_projects(self):
		print("Switching projects")

	def clear_word_lists(self):
		print("Clearing word lists")

	def clear_file_history(self):
		print("Clearing file history")


if __name__ == '__main__':
	App = Notebook()
	App.mainloop()