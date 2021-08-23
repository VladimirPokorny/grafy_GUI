import tkinter as tk
from tkinter import filedialog, Text
from tkinter.messagebox import showinfo
import natsort
import os

def UploadAction():
    filetypes = (
        ('All files', '*.*'),
        ('text files', '*.txt')
    )

    files = filedialog.askopenfilename(
        multiple=True,
        title='Open a file',
        initialdir='',
        filetypes=filetypes)


    showinfo(
        title='Selected File',
        message=files
    )

    filePaths = []
    for file in files:
        f = os.path.basename((file).replace('.*', ''))
        f = os.path.splitext(f)[0]
        filePaths.append(f)
    FileList(natsort.natsorted(filePaths,reverse=True))


def FileList(filePaths):
    text = Text(root, height=8)
    text.pack()
    text.insert('1.0', 'Načtené soubory: \n\n')
    for i in range(len(filePaths)):
        text.insert('3.0', filePaths[i] + '\n')


root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(True, True)
root.geometry('400x400')

button = tk.Button(
    root,
    text='Open',
    command=UploadAction
)
button.pack()

# The entry to input the items
content = tk.StringVar()
entry = tk.Entry(root, textvariable=content)
entry.pack()

# The button to insert the item in the list
button = tk.Button(root, text="Add Item", command=clicked)
button.pack()

# the button to delete everything
button_delete = tk.Button(text="Delete", command=delete)
button_delete.pack()

# The button to delete only the selected item in the list
button_delete_selected = tk.Button(text="Delete Selected", command=delete_selected)
button_delete_selected.pack()

# The listbox
listbox = tk.Listbox(root)
listbox.pack()

root.mainloop()

# for name in files(dir):
#     listbox.insert('end', name)


root.mainloop()

