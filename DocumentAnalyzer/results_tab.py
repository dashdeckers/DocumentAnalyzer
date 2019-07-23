import tkinter as tk
import tkinter.ttk as ttk

try:
    from DocumentAnalyzer.utility import (
        max_button_cols,
    )
except ImportError as e:
    from utility import (
        max_button_cols,
    )

class ResultsTab(tk.Frame):
	def __init__(self, master):
		super().__init__()
		self.master = master

		# Go through the text files just like in classify.
		# For each word, increment a count in one or more
		# of the categories (in a new dict?)

		# Bindings, purge data, docstrings

		# Project data
		self.res_labels = None
		self.res_values = dict()

		# GUI stuff
		self.label_frame = ttk.Frame(self)

		# Packing
		self.label_frame.pack(side='top', fill='both', expand=1)

	def refresh_results(self):
		self.calculate_results()
		self.destroy_labels()
		self.create_labels()

	def calculate_results(self):
		pass

	def destroy_labels(self):
		if self.res_labels:
			for label in self.res_labels:
				label.destroy()

	def create_labels(self):
		if self.master.project_currently_open():
			self.res_labels = list()

			for catname in list(self.master.categories.keys()):
				self.res_labels.append(ttk.Label(self.label_frame,
												 text=f'{catname}: ?'))

			for i, label in enumerate(self.res_labels):
				label.grid(row=int(i / max_button_cols),
						   column=i % max_button_cols)