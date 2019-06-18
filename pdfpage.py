import tkinter as tk
import os

from parser import Parser

# TODO: 
# highlighting of the line we are on
# optimize
# next file functionality

class PDFPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.initialize_parser()

        self.create_header_row()
        self.create_text_area()
        self.spellcheck()

        self.create_edit_row()
        self.create_button_row()
        self.next_error()

    def initialize_parser(self):
        self.p = Parser()
        self.p.extract_text()
        self.p.clean_text()
        self.errors = self.p.spellcheck()

    def reparse(self):
        self.initialize_parser()
        self.text.insert("1.0", " ".join(self.p.tokens))

    # Underlines all spelling mistakes in text
    def spellcheck(self):
        index = "1.0"
        for word in self.errors:
            index = self.text.search(word, "1.0", "end") # "1.0" --> index
            # if word in self.p.spell._word_frequency._dictionary.keys():
            #     self.text.tag_remove("misspelled", index, f"{index}+{len(word)}c")
            # else:
            self.text.tag_add("misspelled", index, f"{index}+{len(word)}c")

    def create_text_area(self):
        self.text = tk.Text(self, width=60, height=15, wrap="word")
        self.text.tag_configure("misspelled", foreground="red", underline=True)
        self.text.insert("1.0", " ".join(self.p.tokens))
        self.text.grid(row=1, column=0, columnspan=8, sticky="we")

        scroll = tk.Scrollbar(self)
        scroll.config(command=self.text.yview)
        self.text.config(yscrollcommand=scroll.set)
        scroll.grid(row=1, column=8, sticky="ns")

    def create_header_row(self):
        name = tk.Label(self, text="filename")
        name.grid(row=0, column=0, sticky="w")

        page = tk.Label(self, text="1/10")
        page.grid(row=0, column=7, sticky="e")

    def create_edit_row(self):
        self.word = tk.Text(self, width=13, height=1)
        self.word.grid(row=2, column=3, columnspan=2)

        self.context1 = tk.Label(self)
        self.context1.grid(row=2, column=0, columnspan=3)

        self.context2 = tk.Label(self)
        self.context2.grid(row=2, column=5, columnspan=3)

        self.options = ["None"]
        self.correction = tk.StringVar(self, "Pick an option")
        self.options_menu = tk.OptionMenu(self,
                                     self.correction,
                                     *self.options)
        self.correction.trace("w", self.apply_correction)
        self.options_menu.grid(row=3, column=3, columnspan=2)
        self.options_menu.config(width=13)

    def next_error(self):
        if not self.errors:
            self.word.delete("1.0", "end")
            self.context1['text'] = ""
            self.context2['text'] = ""
            self.correction.set("Done!")
            self.options_menu['menu'].delete(0, 'end')

        else:
            self.err = self.errors.pop()
            self.cont = self.p.show_context(self.err)

            self.word.delete("1.0", "end")
            self.word.insert("1.0", self.cont[3])
            self.context1['text'] = self.cont[:3]
            self.context2['text'] = self.cont[4:]

            self.options = list(self.p.show_corrections(self.err))
            if len(self.options) > 5:
                self.options = self.options[:5]
            self.correction.set("Pick an option")

            menu = self.options_menu['menu']
            menu.delete(0, 'end')
            for op in self.options:
                menu.add_command(label=op,
                                 command=tk._setit(self.correction, op))

    def apply_correction(self, *args):
        self.p.correct_word(self.err, self.correction.get())
        self.text.delete("1.0", "end")
        self.text.insert("1.0", " ".join(self.p.tokens))
        self.spellcheck()
        self.next_error()

    def create_button_row(self):
        from startpage import StartPage

        b1 = tk.Button(self, text="Discard & Reparse", width=13,
                       command=lambda: self.reparse())
        b1.grid(row=4, column=0, columnspan=2)

        b2 = tk.Button(self, text="Save & Next", width=13)
        b2.grid(row=4, column=2, columnspan=2)

        b3 = tk.Button(self, text="Previous Page", width=13,
                       command=lambda: self.master.switch_frame(StartPage))
        b3.grid(row=4, column=4, columnspan=2)

        b4 = tk.Button(self, text="Next Page", width=13,
                       command=lambda: print("Nope"))
        b4.grid(row=4, column=6, columnspan=2)


class _PDFPage(tk.Frame):
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
