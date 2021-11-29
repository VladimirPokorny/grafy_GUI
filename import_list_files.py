import tkinter as tk
from tkinter import ttk, filedialog, RIGHT, X, Y, W, E, N, S, Label, StringVar, LabelFrame, OptionMenu, messagebox, VERTICAL
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from units import physical_quantity, data, number_columns
import natsort

def LoadAction():
    filetypes = (
        #('ALL files', '*.*'),
        ('CSV files', '*.csv'),
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

def call_delete():
    selection = listbox.curselection()
    for i in reversed(selection):
        listbox.delete(i)
        del files_to_open[i]
        print(files_to_open)


def unit_choose(*args):
    global i
    quantity_units = data[globals()[f"value_column_a{i}"].get()]
    globals()[f"value_column_b{i}"].set(quantity_units[0])
    menu = globals()[f"quantity_column_b{i}"]['menu']
    menu.delete(0, 'end')
    for quantity_unit in quantity_units:
        menu.add_command(label=quantity_unit, command=lambda nation=quantity_unit: globals()[f"value_column_b{i}"].set(nation))

def generate_plot_button():
    global files_to_open
    if 'files_to_open' in globals() and len(files_to_open) != 0:
        print(files_to_open)
        generate_plot()

    else:
        print("prázdná množina")
        tk.messagebox.showwarning(title="Warning", message="Add measured data in CSV")

def generate_plot():
    global files_to_open

    for file in files_to_open:
        table = pd.read_csv(file)

        rozsah1 = 3
        rozsah2 = len(pd.read_csv(file).loc[:, 'x-axis'])
        t = table.iloc[rozsah1:rozsah2, 0]
        t = t.astype(np.float64)

        i1 = table.iloc[rozsah1:rozsah2, 1]
        i1 = i1.astype(np.float64)

        i2 = table.iloc[rozsah1:rozsah2, 2]
        i2 = i2.astype(np.float64)

        i3 = table.iloc[rozsah1:rozsah2, 3]
        i3 = i3.astype(np.float64)

        plt.figure(figsize=(10, 10))
        plt.title('Data ze souboru: ' + os.path.basename((file).replace('.csv', '')))
        plt.plot(t, i1)
        plt.plot(t, i2)
        plt.plot(t, i3)

        if pdf.get() == 0 and preview.get() == 1:
            plt.show()
        else:
            pass

        if pdf.get() == 1:
            plt.rcParams['pdf.fonttype'] = 42
            file = os.path.basename((file).replace('.csv', ''))
            plt.savefig('pdf/' + file + '.pdf')

            if preview.get() == 1:
                plt.show()
            else:
                pass



# The window
root = tk.Tk()
root.title("List App")
#root.geometry("500x400")
root.geometry("700x600")
root.resizable(height = None, width = None)
root.minsize(450, 350)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

input_frame = LabelFrame(root, text="input", padx=5, pady=5)
input_frame.grid(row=0, column=0, padx=5, pady=5, sticky=N+S+W+E)

input_frame.grid_rowconfigure(1, weight=1)
input_frame.grid_columnconfigure(0, weight=1)
input_frame.grid_columnconfigure(1, weight=1)
input_frame.grid_columnconfigure(2, weight=1)

option_frame1 = LabelFrame(root, text="option", padx=5, pady=5)
option_frame1.grid(row=0, column=1, padx=5, pady=5, sticky=N+S+W+E)

option_frame2 = LabelFrame(root, text="option", padx=5, pady=5)
option_frame2.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=N+S+W+E)

# option_frame.grid_rowconfigure(1, weight=1)
# option_frame.grid_columnconfigure(0, weight=1)
# option_frame.grid_columnconfigure(1, weight=1)
# option_frame.grid_columnconfigure(2, weight=1)

# The button to insert the item in the list
button = tk.Button(input_frame, text="Add Items", command=LoadAction)
button.grid(row=0, column=0, padx=5, pady=5, sticky=W+E)

# the button to delete everything
button_delete = tk.Button(input_frame, text="Delete All", command=delete)
button_delete.grid(row=0, column=2, padx=5, pady=5, sticky=W+E)

# The button to delete only the selected item in the list
button_delete_selected = tk.Button(input_frame, text="Delete Selected", command=call_delete)
button_delete_selected.grid(row=0, column=1, padx=5, pady=5, sticky=W+E)

label_files = Label(input_frame, text="Loaded files: ")
label_files.grid(row=1, column=0, columnspan=3, rowspan=1, sticky=W, padx=2, pady=(5,0))

scrollbar = tk.Scrollbar(input_frame, orient=VERTICAL)
scrollbar.grid(row=2, column=0, columnspan=3, rowspan=1, sticky=N+S)


# The listbox
listbox = tk.Listbox(input_frame, selectmode='multiple', yscrollcommand=scrollbar.set)
listbox.grid(row=2, column=0, columnspan=3, rowspan=1, sticky=W+E+N+S, padx=2, pady=2)
listbox.config(yscrollcommand = scrollbar.set)


button_plot = tk.Button(root, text="Generate Plots", command=generate_plot_button)
button_plot.grid(row=4, column=1, padx=10, pady=10, sticky=W+E)

pdf = tk.IntVar()
checkbutton_plot_pdf = tk.Checkbutton(root, text="Generate Merged PDFs", variable=pdf, onvalue=1, offvalue=0,)
checkbutton_plot_pdf.grid(row=4, column=0, padx=10, pady=10, sticky=W+E)
checkbutton_plot_pdf.var = pdf

preview = tk.IntVar()
sample_checkbutton = tk.Checkbutton(root, text="View Preview", variable=preview, onvalue=1, offvalue=0,)
sample_checkbutton.grid(row=3, column=0, padx=10, pady=10, sticky=W+E)
sample_checkbutton.var = preview

###################################################################
value_column_time = StringVar(option_frame1)
value_column_time.set('number column')  # default value

label_column_time = Label(option_frame1, text="Time column:")
label_column_time.grid(row=0, column=0, columnspan=1, rowspan=1, sticky=W, padx=2, pady=2)

quantity_column_time = OptionMenu(option_frame1, value_column_time, *number_columns)
quantity_column_time.grid(row=0, column=1, padx=2, pady=2, sticky=W + E)

##
value_column_current1 = StringVar(option_frame1)
value_column_current1.set('number column')  # default value

label_column_current1 = Label(option_frame1, text="Current phase 1:")
label_column_current1.grid(row=1, column=0, columnspan=1, rowspan=1, sticky=W, padx=2, pady=2)

quantity_column_current1 = OptionMenu(option_frame1, value_column_current1, *number_columns)
quantity_column_current1.grid(row=1, column=1, padx=2, pady=2, sticky=W + E)

##
value_column_current2 = StringVar(option_frame1)
value_column_current2.set('number column')  # default value

label_column_current2 = Label(option_frame1, text="Current phase 2:")
label_column_current2.grid(row=2, column=0, columnspan=1, rowspan=1, sticky=W, padx=2, pady=2)

quantity_column_current2 = OptionMenu(option_frame1, value_column_current2, *number_columns)
quantity_column_current2.grid(row=2, column=1, padx=2, pady=2, sticky=W + E)

##
value_column_voltage1 = StringVar(option_frame1)
value_column_voltage1.set('number column')  # default value

label_column_voltage1 = Label(option_frame1, text="Voltage phase 1:")
label_column_voltage1.grid(row=3, column=0, columnspan=1, rowspan=1, sticky=W, padx=2, pady=2)

quantity_column_voltage1 = OptionMenu(option_frame1, value_column_voltage1, *number_columns)
quantity_column_voltage1.grid(row=3, column=1, padx=2, pady=2, sticky=W + E)


for i in range(4):
    globals()[f"label_columns{i}"] = Label(option_frame2, text="column " + str(i + 1) + ":")
    globals()[f"label_columns{i}"].grid(row=i, column=0, columnspan=1, rowspan=1, sticky=W, padx=2, pady=2)

    globals()[f"value_column_a{i}"] = StringVar()
    globals()[f"value_column_b{i}"] = StringVar()
    globals()[f"value_column_a{i}"].trace('w', unit_choose)

    globals()[f"quantity_column_a{i}"] = OptionMenu(option_frame2, globals()[f"value_column_a{i}"], *data.keys())
    globals()[f"quantity_column_b{i}"] = OptionMenu(option_frame2, globals()[f"value_column_b{i}"], '')
    #globals()[f"value_column_a{i}"].set(data(0))

    globals()[f"quantity_column_a{i}"].grid(row=i, column=1, padx=2, pady=2, sticky=W + E)
    globals()[f"quantity_column_b{i}"].grid(row=i, column=2, padx=2, pady=2, sticky=W + E)


root.mainloop()










