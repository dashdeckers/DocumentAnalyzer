import tkinter as tk
import tkinter.ttk as ttk

from os import listdir
from os.path import join, isfile

try:
    from DocumentAnalyzer.utility import (
        max_button_cols,
        text_folder,
    )
except ImportError as e:
    from utility import (
        max_button_cols,
        text_folder,
    )

class ResultsTab(tk.Frame):
    '''
    TODO: Fill this in.
    '''
    def __init__(self, master):
        super().__init__()
        self.master = master

        # Project data
        self.res_labels = None
        self.res_values = dict()

        # GUI stuff
        self.label_frame = ttk.Frame(self)

        # Packing
        self.label_frame.pack(side='top', fill='both', expand=1)

    def refresh_results(self):
        '''Calculate the results and show them using labels.
        '''
        self.calculate_results()
        self.destroy_labels()
        self.create_labels()

    def calculate_results(self):
        '''Calculate the frequencies: For each word in the text files, increment
        the count for each category that contains that word. Store the results
        in self.res_values.
        '''
        if self.master.project_currently_open():
            self.res_values = dict.fromkeys(list(self.master.categories.keys()))
            for key in self.res_values:
                self.res_values[key] = 0

            f_dir = join('.', self.master.project_name, text_folder)
            files = [f for f in listdir(f_dir) if isfile(join(f_dir, f))
                                                and f.endswith('.txt')]

            if not files:
                return

            for file in files:
                with open(join(f_dir, file), 'r') as text_file:
                    text_tokens = text_file.read().split()
                    for word in text_tokens:
                        for catname in self.master.categories:
                            if word in self.master.categories[catname]:
                                self.res_values[catname] += 1

    def destroy_labels(self):
        '''Destroy the labels containing the results for each category.
        '''
        if self.res_labels:
            for label in self.res_labels:
                label.destroy()

    def create_labels(self):
        '''Create the labels containing the results for each category.
        '''
        if self.master.project_currently_open():
            self.res_labels = list()

            self.res_labels.append(tk.Label(self.label_frame,
                                            text='Category: Count'))

            for catname in list(self.master.categories.keys()):
                labeltext = f'{catname}: {self.res_values[catname]}'
                self.res_labels.append(tk.Label(self.label_frame,
                                                text=labeltext))

            for label in self.res_labels:
                label.pack(side='top', fill='x', expand=1)
