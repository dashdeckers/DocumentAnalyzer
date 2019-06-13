import tkinter as tk

class DocumentAnalyser(tk.Tk):
    def __init__(self):
        from startpage import StartPage
        tk.Tk.__init__(self)
        # Basic configs
        self.minsize(width=530, height=350)
        self.maxsize(width=800, height=1000)
        self.title("Document Analysis")
        # Persistent data
        self.metadata = {
            'language' : None,
            'n_categories' : None,
            'project_name' : None,
        }
        # Switch frame to the start page
        self._frame = None
        self.switch_frame(StartPage)

    # Function to switch between pages
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

app = DocumentAnalyser()
app.mainloop()
