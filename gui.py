import tkinter as tk
import tkinter.ttk as ttk

from tkinter import (
	N, S, E, W,
)

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
feet = StringVar()
meters = StringVar()

feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind('<Return>', calculate)
'''