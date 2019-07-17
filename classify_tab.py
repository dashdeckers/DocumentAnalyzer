import tkinter as tk
import tkinter.ttk as ttk

max_button_cols = 4

class ClassifyTab(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.cat_names = None
        self.cat_buttons = None

        self.classify_label = ttk.Label(self, text='Whaaaat', style='Example.TLabel')
        self.buttons_frame = ttk.Frame(self)

        # Packing
        self.classify_label.pack(side='top', fill='both', expand=1)
        self.buttons_frame.pack(side='bottom', fill='both', expand=1)

    def add_word_to_cat(self, event, cat_num, cat_name):
        #self.master.categories[cat_name].append(word)
        print(cat_num, cat_name)

    def create_cat_buttons(self):
        self.cat_names = list(self.master.categories.keys())
        self.cat_buttons = list()
        for i in range(self.master.n_cats):
            self.cat_buttons.append(ttk.Button(self.buttons_frame, text=self.cat_names[i] + f' ({i+1})', command=lambda event=0, b_num=i, b_name=self.cat_names[i]: self.add_word_to_cat(event, b_num, b_name)))
        for i in range(self.master.n_cats):
            self.cat_buttons[i].grid(row=int(i/max_button_cols), column=i%max_button_cols)

    def refresh_classify(self):
        if self.cat_buttons:
            for button in self.cat_buttons:
                button.destroy()
        self.create_cat_buttons()