import tkinter as tk
import tkinter.ttk as ttk

filehistory = ['file1', 'file2', 'file3']

cat_infotext = '''These are the words that belong to the corresponding categories.
If you want to edit them directly: Then save the project, close the
program and open the corresponding text file located within the
project folder. This text file can be edited to add multiple words
to the wordlist directly, but make sure you put only one word per
line'''

filehist_infotext = '''This is the list of filenames that have already been extracted,
that means the text has been retrieved from the file, possibly edited and corrected,
and then saved. These filenames will be excluded from the extract step. To re-do
a file that is on this list: Close the program, open the file history text file
located within the project folder, remove that filename from the list, and then
save the file.
'''

class DataviewTab(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self.selected_data_view = tk.StringVar(self, value='File History')
        self.data_view_selector = ttk.Combobox(self, state='readonly', textvar=self.selected_data_view)
        self.data_view_selector['values'] = [self.selected_data_view.get()]
        self.data_view_selector.current(0)
        self.data_view_selector.bind('<<ComboboxSelected>>', self.data_view_selection_change)
        self.data_view = ttk.Label(self, text='\n'.join(filehistory))
        self.data_view.configure(anchor='center')
        self.data_info = ttk.Label(self, text=filehist_infotext)
        self.data_info.configure(anchor='center')

        # Packing
        self.data_view_selector.pack(side='top')
        self.data_view.pack(side='top', fill='both', expand=1)
        self.data_info.pack(side='bottom', fill='both', expand=1)

    def data_view_selection_change(self, event=None):
        self.data_view_selector.selection_clear()
        if self.selected_data_view.get() == 'File History':
            self.data_info['text'] = filehist_infotext
            self.data_view['text'] = '\n'.join(filehistory)
        else:
            self.data_info['text'] = cat_infotext
            self.data_view['text'] = '\n'.join(self.master.categories[self.selected_data_view.get()])

    def refresh_dataview(self):
        self.data_view_selector['values'] = ['File History'] + list(self.master.categories.keys())
        self.data_view_selector.current(0)
        self.data_view_selection_change()