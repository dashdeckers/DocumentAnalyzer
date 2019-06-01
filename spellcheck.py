import tkinter as tk
import tkinter.font as tkFont

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        ## Toolbar
        self.toolbar = tk.Frame()

        ## Main part of the GUI
        # I'll use a frame to contain the widget and 
        # scrollbar; it looks a little nicer that way...
        text_frame = tk.Frame(borderwidth=1, relief="sunken")
        self.text = tk.Text(wrap="word", background="white", 
                            borderwidth=0, highlightthickness=0)
        self.vsb = tk.Scrollbar(orient="vertical", borderwidth=1,
                                command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(in_=text_frame,side="right", fill="y", expand=False)
        self.text.pack(in_=text_frame, side="left", fill="both", expand=True)
        self.toolbar.pack(side="top", fill="x")
        text_frame.pack(side="bottom", fill="both", expand=True)

        # Define misspellt tag
        self.text.tag_configure("misspelled", foreground="red", underline=True)

        # Call spellcheck when space is pressed
        self.text.bind("<space>", self.Spellcheck)

        # Spell checking dictionary, needs to be changed for sure
        self._words=open("/usr/share/dict/words").read().split("\n")

    def Spellcheck(self, event):
        '''Spellcheck the word preceeding the insertion point'''
        index = self.text.search(r'\s', "insert", backwards=True, regexp=True)
        if index == "":
            index ="1.0"
        else:
            index = self.text.index("%s+1c" % index)
        word = self.text.get(index, "insert")
        if word in self._words:
            self.text.tag_remove("misspelled", index, "%s+%dc" % (index, len(word)))
        else:
            self.text.tag_add("misspelled", index, "%s+%dc" % (index, len(word)))

if __name__ == "__main__":
    app=App()
    app.mainloop()