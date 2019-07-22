import tkinter as tk
import tkinter.ttk as ttk

from DocumentAnalyzer.utility import (
    strings,
    WrappingLabel,
)

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
        self.data_view_selector = ttk.Combobox(self, state='readonly',
                                               textvar=self.selected_data_view)
        self.data_view_selector['values'] = [self.selected_data_view.get()]
        self.data_view_selector.current(0)
        self.data_view_selector.bind('<<ComboboxSelected>>',
                                     self.data_view_selection_change)

        self.data_view = tk.Text(self, wrap='word')
        self.data_view.tag_configure('center', justify='center')
        self.data_view.insert('1.0', '\n'.join(self.master.files_done))
        self.data_view.tag_add('center', '1.0', 'end')
        self.data_view.configure(state='disabled')
        self.scrollbar = tk.Scrollbar(self, orient='vertical')
        self.data_view.configure(yscrollcommand=self.scrollbar.set)

        self.data_info = WrappingLabel(self, text=strings['filehist_infotext'])
        self.data_info.configure(anchor='center')

        # Packing
        self.data_view_selector.pack(side='top')
        self.scrollbar.pack(side='right', fill='y')
        self.data_view.pack(side='top', fill='both', expand=1)
        self.data_info.pack(side='bottom', fill='both', expand=1)

    def refresh_dataview(self):
        '''Set the possible values of the drop down menu to the 'File History'
        and the category names, and set the current selection to 'File History'.
        '''
        possible_values = ['File History'] + list(self.master.categories.keys())
        self.data_view_selector['values'] = possible_values
        self.data_view_selector.current(0)
        self.data_view_selection_change()

    def data_view_selection_change(self, event=None):
        '''Sets the text field to the contents of the currently selected
        dropdown menu item.
        '''
        self.data_view_selector.selection_clear()
        if self.selected_data_view.get() == 'File History':
            self.data_info['text'] = strings['filehist_infotext']
            self.data_view.configure(state='normal')
            self.data_view.delete('1.0', 'end')
            self.data_view.insert('1.0', '\n'.join(self.master.files_done))
            self.data_view.tag_add('center', '1.0', 'end')
            self.data_view.configure(state='disabled')
        else:
            catname = self.selected_data_view.get()
            text = '\n'.join(self.master.categories[catname])

            self.data_info['text'] = strings['cat_infotext']
            self.data_view.configure(state='normal')
            self.data_view.delete('1.0', 'end')
            self.data_view.insert('1.0', text)
            self.data_view.tag_add('center', '1.0', 'end')
            self.data_view.configure(state='disabled')
