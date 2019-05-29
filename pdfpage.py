import tkinter as tk

class PDFPage(tk.Frame):
    def __init__(self, master):
        from startpage import StartPage
        tk.Frame.__init__(self, master)

        default_text = "Press the 'Parse' button to get file contents"
        filename = self.get_filename()

        # Show filename
        tk.Label(self, text=filename).grid(row=0, column=0, columnspan=6, sticky="ew")

        # Create the transcription text window and insert the default text
        self.t_window = tk.Text(self, width=50, height=20)
        self.t_window.grid(row=1, column=0, columnspan=6, sticky="new")
        self.t_window.insert("1.0", default_text)

        # Create the quickedit listbox and fill with default edits
        self.selected_qe = None
        self.qe_window = tk.Listbox(self, width=45)
        # TODO: How to make these functional? Name corresponds to function?
        self.quickedits = ['Quick-edit #1', 'Quick-edit #2', 'Quick-edit #3']
        for element in self.quickedits:
            self.qe_window.insert("end", element)
        self.qe_window.bind('<<ListboxSelect>>', self.list_box_selected)
        self.qe_window.bind('<Double-1>', self.list_box_doubleclicked)
        self.qe_window.grid(row=2, column=0, columnspan=3, rowspan=4, sticky="sew")

        # Create the buttons
        tk.Button(self, text="Parse",
                  command=self.parse_pdf).grid(row=2, column=5)
        tk.Button(self, text="Add Quick-edit",
                  command=self.add_quickedit).grid(row=3, column=5)
        tk.Button(self, text="Remove Quick-edit",
                  command=self.remove_quickedit).grid(row=4, column=5)
        tk.Button(self, text="Save",
                  command=self.save_text).grid(row=5, column=5)
        tk.Button(self, text="Back",
                  command=lambda: master.switch_frame(StartPage)).grid(row=5, column=5)

    def get_filename(self):
        return "Filename: Testing"

    def parse_pdf(self):
        print("Parsing PDF")
        text = "This would be the pdf text"
        self.t_window.delete("1.0", "end")
        self.t_window.insert("1.0", text)

    def save_text(self):
        print("Saving text")

    def list_box_selected(self, event):
        sender = event.widget
        idx = sender.curselection()
        if idx:
            value = sender.get(idx)
            self.selected_qe = value
            print(f'selected: {value}')

    def list_box_doubleclicked(self, event):
        sender = event.widget
        idx = sender.curselection()
        if idx:
            value = sender.get(idx)
            print(f'double clicked: {value}')

    def add_quickedit(self):
        print("adding quickedit")

    def remove_quickedit(self):
        print("removing quickedit")
        if self.selected_qe is None:
            print("selected quickedit is none")
            return
        self.quickedits.remove(self.selected_qe)
        self.selected_qe = None
        self.qe_window.delete(0, "end")
        for element in self.quickedits:
            self.qe_window.insert("end", element)
