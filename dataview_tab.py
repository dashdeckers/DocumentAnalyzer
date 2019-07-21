import tkinter as tk
import tkinter.ttk as ttk

from utility import cat_infotext, filehist_infotext

class DataviewTab(tk.Frame):
    '''
    TODO: Fill this in.
    '''
    def __init__(self, master):
        super().__init__()
        self.master = master

        # Project data
        self.selected_data_view = tk.StringVar(self, value='File History')

        # GUI stuff
        self.data_view_selector = ttk.Combobox(self, state='readonly', textvar=self.selected_data_view)
        self.data_view_selector['values'] = [self.selected_data_view.get()]
        self.data_view_selector.current(0)
        self.data_view_selector.bind('<<ComboboxSelected>>', self.data_view_selection_change)
        self.data_view = ttk.Label(self, text='\n'.join(self.master.files_done))
        self.data_view.configure(anchor='center')
        self.data_info = ttk.Label(self, text=filehist_infotext)
        self.data_info.configure(anchor='center')

        # Packing
        self.data_view_selector.pack(side='top')
        self.data_view.pack(side='top', fill='both', expand=1)
        self.data_info.pack(side='bottom', fill='both', expand=1)

    def refresh_dataview(self):
        self.data_view_selector['values'] = ['File History'] + list(self.master.categories.keys())
        self.data_view_selector.current(0)
        self.data_view_selection_change()

    def data_view_selection_change(self, event=None):
        self.data_view_selector.selection_clear()
        if self.selected_data_view.get() == 'File History':
            self.data_info['text'] = filehist_infotext
            self.data_view['text'] = '\n'.join(self.master.files_done)
        else:
            self.data_info['text'] = cat_infotext
            self.data_view['text'] = '\n'.join(self.master.categories[self.selected_data_view.get()])
