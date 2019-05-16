import tkinter as tk
import tkinter.ttk as ttk

from tkinter import (
	N, S, E, W,
)

root = tk.Tk()

def parse_pdf():
	print("Parsing PDF")
	put_text(transcription_window, "This would be the pdf text")

def put_text(text_widget, text):
	text_widget.insert("1.0", text)

tk.Label(root, text="Filename").grid(row=0, column=0, sticky=W)
tk.Entry(root, width=50).grid(row=0, column=1, columnspan=5)

transcription_window = tk.Text(root, width=50, height=20)
transcription_window.grid(row=1, column=0, columnspan=6, sticky=(N, W, E))
transcription_window.insert("1.0", "Press the 'Parse' button to get file contents")

quickedit_window = tk.Text(root, height=10)
quickedit_window.grid(row=2, column=0, columnspan=3, rowspan=2, sticky=(S, W))
quickedit_window.insert("1.0", "Quick edits go here")

tk.Button(root, text="Parse", command=parse_pdf).grid(row=2, column=5)
tk.Button(root, text="Save").grid(row=3, column=5)

root.mainloop()

'''
class Parsing_Editing_Window(ttk.Frame):
	def __init__(self, parent, *args, **kwargs):
		ttk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		# with a padding of 12 all around, stick to each side of root window
		self['padding'] = 12
		self.grid(column=0, row=0, sticky=(N, W, E, S))
		self.parent.columnconfigure(0, weight=1)
		self.parent.rowconfigure(0, weight=1)

		# put textarea on the top and stick to each side of root except the bottom
		transcription_window = tk.Text(self, width=50, height=20)
		transcription_window.grid(column=0, row=0, sticky=(N, W, E))
		# set the default text, and configure to resize evenly
		transcription_window.insert("1.0", "Press the 'Parse' button to get file contents")
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)

root = tk.Tk()
root.title("Document Analyser")
Parsing_Editing_Window(root)
root.mainloop()
'''
