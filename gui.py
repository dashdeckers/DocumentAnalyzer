import tkinter as tk
import tkinter.ttk as ttk

from tkinter import (
    N, S, E, W, END,
)

root = tk.Tk()

def parse_pdf():
    print("Parsing PDF")
    put_text(transcription_window, "This would be the pdf text")

def put_text(text_widget, text):
    text_widget.delete("1.0", END)
    text_widget.insert("1.0", text)

def list_box_selected(event):
    global selected_quickedit
    sender = event.widget
    idx = sender.curselection()
    if idx:
        value = sender.get(idx)
        selected_quickedit = value
        print(f'selected: {value}')

def list_box_doubleclicked(event):
    sender = event.widget
    idx = sender.curselection()
    if idx:
        value = sender.get(idx)
        print(f'double clicked: {value}')

def add_quickedit():
    print("adding quickedit")

def remove_quickedit():
    global selected_quickedit
    print("removing quickedit")
    if selected_quickedit is None:
        print("selected quickedit is none")
        return
    quickedits.remove(selected_quickedit)
    selected_quickedit = None
    quickedit_window.delete(0, END)
    for element in quickedits:
        quickedit_window.insert(END, element)

tk.Label(root, text="Filename").grid(row=0, column=0, sticky=W)
tk.Entry(root, width=50).grid(row=0, column=1, columnspan=5)

transcription_window = tk.Text(root, width=50, height=20)
transcription_window.grid(row=1, column=0, columnspan=6, sticky=(N, W, E))
transcription_window.insert("1.0", "Press the 'Parse' button to get file contents")

selected_quickedit = None
quickedit_window = tk.Listbox(root, width=45)
quickedits = ['Quick-edit #1', 'Quick-edit #2', 'Quick-edit #3']
for element in quickedits:
    quickedit_window.insert(END, element)
quickedit_window.bind('<<ListboxSelect>>', list_box_selected)
quickedit_window.bind('<Double-1>', list_box_doubleclicked)
quickedit_window.grid(row=2, column=0, columnspan=3, rowspan=4, sticky=(S, W, E))

tk.Button(root, text="Parse", command=parse_pdf).grid(row=2, column=5)
tk.Button(root, text="Add Quick-edit", command=add_quickedit).grid(row=3, column=5)
tk.Button(root, text="Remove Quick-edit", command=remove_quickedit).grid(row=4, column=5)
tk.Button(root, text="Save").grid(row=5, column=5)

for colnum in range(root.grid_size()[0]):
    root.columnconfigure(colnum, weight=1)

for rownum in range(root.grid_size()[1]):
    root.rowconfigure(rownum, weight=1)

root.minsize(width=471, height=553)
root.maxsize(width=500, height=600)

root.title("Document Analysis")
root.mainloop()
