import tkinter as tk
from tkinter import filedialog, RIGHT, Y, W, E, N, S, Label
import natsort
import os

def LoadAction():
    filetypes = (
        ('CSV files', '*.csv*'),
        ('text files', '*.txt')
    )

    files = filedialog.askopenfilename(
        multiple=True,
        title='Open a file',
        initialdir='',
        filetypes=filetypes)

    filePaths = []
    for file in files:
        f = os.path.basename(file)
        filePaths.append(f)
    FileList(natsort.natsorted(filePaths,reverse=False))
    global files_to_open
    files_to_open = list(files)
    print(files)
    print('files to open: \n ' + str(files_to_open))


def FileList(filePaths):
    for i in range(len(filePaths)):
        listbox.insert(tk.END, filePaths[i])

def clicked():
    listbox.insert(tk.END, content.get())

def delete():
    listbox.delete(0, tk.END)
    global files_to_open
    files_to_open = []

def delete_selected():
    listbox.delete(tk.ANCHOR)
    #del files_to_open[tk.ANCHOR]

def call_delete():
    selection = listbox.curselection()
    for i in reversed(selection):
        listbox.delete(i)
        del files_to_open[i]
        print(files_to_open)

# The window
root = tk.Tk()
root.title("List App")
root.geometry("400x400")

# The button to insert the item in the list
button = tk.Button(root, text="Add Items", command=LoadAction)
button.grid(row=0, column=0, sticky=W+E)

# the button to delete everything
button_delete = tk.Button(root, text="Delete All", command=delete)
button_delete.grid(row=0, column=2, sticky=W+E)

# The button to delete only the selected item in the list
button_delete_selected = tk.Button(text="Delete Selected", command=call_delete)
button_delete_selected.grid(row=0, column=1, sticky=W+E)

scrollbar = tk.Scrollbar(root, orient="vertical")
scrollbar.grid(row=2, column=0, columnspan=3, rowspan=1, sticky=N+S, padx=5, pady=5) #(side=RIGHT, fill=Y)
#root.configure(yscrollcommand=scrollbar.set)

# The listbox
listbox = tk.Listbox(root, yscrollcommand=scrollbar.set)
listbox.grid(row=2, column=0, columnspan=3, rowspan=1, sticky=W+E, padx=5, pady=5) #(padx=0,pady=10,fill=tk.BOTH,expand=True)
listbox.config(yscrollcommand = scrollbar.set)

label_files = Label(root, text=u"Loaded files: ")
label_files.grid(row=1, column=0, columnspan=3, rowspan=1, sticky=W, padx=5, pady=(10,0))

#root.grid_columnconfigure(1,weight=1)
root.mainloop()