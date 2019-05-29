
'''
for colnum in range(root.grid_size()[0]):
    root.columnconfigure(colnum, weight=1)

for rownum in range(root.grid_size()[1]):
    root.rowconfigure(rownum, weight=1)

folders = [o for o in os.listdir() if os.path.isdir(o)]

'''


import tkinter as tk

class DocumentAnalyser(tk.Tk):
    def __init__(self):
        from startpage import StartPage
        tk.Tk.__init__(self)
        self.minsize(width=530, height=550)
        self.maxsize(width=600, height=700)
        self.title("Document Analysis")
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

app = DocumentAnalyser()
app.mainloop()
