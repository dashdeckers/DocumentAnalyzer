import tkinter as tk
import os

from pdftest import get_text

# TODO: 
# Progress bar (file X out of Y)
# Refresh filenames (user copies more into folder)
#   OR add files via GUI
# Menu bar instead of buttons?

# Current filename is always self.filenames[0]
# that means when going to next file, delete that entry

class PDFPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Get the filenames to be parsed
        self.filenames = self.get_filenames()

        # Create label to show current filename
        self.fn_label = tk.Label(self, 
                                 text="Filename: " + self.filenames[0])
        self.fn_label.grid(row=0, column=0, columnspan=6, sticky="ew")

        # Create the window in which the editable pdf text will appear
        self.create_transcription_window()

        # Create the list of quick-access edits to the text
        self.create_quickedit_window()

        # Create the parse pdf, remove/add quick edit and go back buttons
        self.create_buttons()

        # Configure rows and cols for resizing
        self.configure_grid()

    # Give all rows and cols equal weights so that they resize nicely
    # TODO: Not working correctly, resizing doesn't resize the widgets
    def configure_grid(self):
        print(self.grid_size())
        for row_num in range(self.grid_size()[1]):
            self.rowconfigure(row_num, weight=1)
        for col_num in range(self.grid_size()[0]):
            self.columnconfigure(col_num, weight=1)

    # Create the buttons
    def create_buttons(self):
        from startpage import StartPage
        # Parse the scanned pdf corresponding to current filename and display text
        parse_b = tk.Button(self, text="Parse",
                            width=10,
                            command=self.parse_pdf)
        parse_b.grid(row=2, column=5)
        # Save the text to a text file with the same filename in the right folder
        save_b = tk.Button(self, text="Save",
                           width=10,
                           command=self.save_text)
        save_b.grid(row=3, column=5)
        # Run the spell checker to highlight misspellt words
        spell_b = tk.Button(self, text="Spellcheck",
                            width=10,
                            command=self.spellcheck)
        spell_b.grid(row=4, column=5)
        # Go back to the start page
        back_b = tk.Button(self, text="Back",
                           width=10,
                           command=lambda: self.master.switch_frame(StartPage))
        back_b.grid(row=5, column=5)
        # Go to the next page
        next_b = tk.Button(self, text="Next Page",
                           width=10,
                           command=lambda:print("Nope"))
        next_b.grid(row=6, column=5)
        # Add a quick edit command to list
        add_b = tk.Button(self, text="Add Quick-edit",
                          width=15,
                          command=self.add_quickedit)
        add_b.grid(row=6, column=0)
        # Remove the selected quick edit command from list
        rem_b = tk.Button(self, text="Remove Quick-edit",
                          width=15,
                          command=self.remove_quickedit)
        rem_b.grid(row=6, column=1)

    # Create the quickedit listbox and fill with default edits
    def create_quickedit_window(self):
        self.selected_qe = None
        self.qe_window = tk.Listbox(self, width=45)
        # TODO: How to make these functional? Name corresponds to function?
        self.quickedits = ['Quick-edit #1', 'Quick-edit #2', 'Quick-edit #3']
        for element in self.quickedits:
            self.qe_window.insert("end", element)
        self.qe_window.bind('<<ListboxSelect>>', self.list_box_selected)
        self.qe_window.bind('<Double-1>', self.list_box_doubleclicked)
        self.qe_window.grid(row=2, column=0, columnspan=3, rowspan=4, sticky="sew")

    # Create the transcription window and fill with default text
    def create_transcription_window(self):
        default_text = "Press the 'Parse' button to get file contents"
        self.t_window = tk.Text(self, width=50, height=20)
        self.t_window.grid(row=1, column=0, columnspan=6, sticky="new")
        self.t_window.insert("1.0", default_text)
        self.t_window.tag_configure("misspelled", foreground="red", underline=True)
        # TODO: Get a proper, os independent spellcheck dict
        self._dict = open("/usr/share/dict/words").read().split("\n")

    # Underlines all words in the text box that are not in the dictionary
    def spellcheck(self):
        text = self.t_window.get("1.0", "end").split()
        index = "1.0"

        print(text)

        for word in text:
            index = self.t_window.search(word, index, "end")
            if word in self._dict:
                self.t_window.tag_remove("misspelled", index, f"{index}+{len(word)}c")
            else:
                self.t_window.tag_add("misspelled", index, f"{index}+{len(word)}c")

    # Get all the filenames from the scanned pdf folder and remove already parsed
    def get_filenames(self):
        return ["Testing"]

    # Parse the file we are currently at and return its text
    def parse_pdf(self):
        print("Parsing PDF")
        text = get_text('./Testing/PDF_Files/test_pdf.pdf')
        self.t_window.delete("1.0", "end")
        self.t_window.insert("1.0", text)

    # Save the parsed and edited text from the transcription window to file
    def save_text(self):
        try:
            project_name = self.master.metadata['project_name']
            filename = self.filenames[0]
            file_path = os.path.join('.', project_name, "Text_Files", filename + '.txt')
            with open(file_path, 'w') as file:
                file.write(self.t_window.get("1.0", "end"))
            print("Saving text")
        except FileNotFoundError as e:
            raise e

    # Handle selecting a quick edit
    def list_box_selected(self, event):
        sender = event.widget
        idx = sender.curselection()
        if idx:
            value = sender.get(idx)
            self.selected_qe = value
            print(f'selected: {value}')

    # Handle double clicking a quickedit
    def list_box_doubleclicked(self, event):
        sender = event.widget
        idx = sender.curselection()
        if idx:
            value = sender.get(idx)
            print(f'double clicked: {value}')

    # Add a quickedit
    def add_quickedit(self):
        print("adding quickedit")

    # Remove the selected quickedit
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
