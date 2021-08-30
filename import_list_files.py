import tkinter as tk
from tkinter import ttk, filedialog, RIGHT, X, Y, W, E, N, S, Label, StringVar, LabelFrame, OptionMenu, messagebox, VERTICAL
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from units import physical_quantity
import natsort

def LoadAction():
    filetypes = (
        ('ALL files', '*.*'),
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

def unit_choose():
    if quantity_unit_column1.get() == "t - time":
        quantity_unit_column1.config(value=unit_time)
        quantity_unit_column1.current(0)
    if quantity_unit_column1.get() == "I - current":
        quantity_unit_column1.config(value=unit_current)
        quantity_unit_column1.current(0)
    if quantity_unit_column1.get() == "U - voltage":
        quantity_unit_column1.config(value=unit_voltage)
        quantity_unit_column1.current(0)
    if quantity_unit_column1.get() == "M - torque":
        quantity_unit_column1.config(value=unit_torque)
        quantity_unit_column1.current(0)
    if quantity_unit_column1.get() == "n - speed":
        quantity_unit_column1.config(value=unit_speed)
        quantity_unit_column1.current(0)
    print("test")

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
        #print(table)

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

        plt.figure(figsize=(5, 5))
        plt.title('Data ze souboru: ' + os.path.basename((file).replace('.csv', '')))
        plt.plot(t, i1)
        plt.plot(t, i2)
        plt.plot(t, i3)
        plt.show()


    #     rozsah1 = 3
    #     rozsah2 = len(pd.read_csv(file).loc[:, 'x-axis'])
    #
    # graf_proudy_moment_otacky(tb_t, tb_i1, tb_i2, tb_M, tb_n, file, rozsah1, rozsah2):
    # table = pd.read_csv(file)
    #
    # t = table.iloc[rozsah1:rozsah2, tb_t]
    # t = t.astype(np.float)
    #
    # i1 = table.iloc[rozsah1:rozsah2, tb_i1]
    # i1 = i1.astype(np.float)
    #
    # if tb_i2 != -1:
    #     i2 = table.iloc[rozsah1:rozsah2, tb_i2]
    #     i2 = i2.astype(np.float)
    #     i3 = - i1 - i2
    #
    # M = table.iloc[rozsah1:rozsah2, tb_M]
    # M = M.astype(np.float)
    #
    # n = table.iloc[rozsah1:rozsah2, tb_n]
    # n = n.astype(np.float)
    #
    # plt.figure(figsize=(15, 15))
    #
    # plt.subplot(2, 1, 1)
    # plt.title('Průběhy proudů, otáček a momentu \nData ze souboru: ' + os.path.basename((file).replace('.csv', '')))
    # plt.plot(t, i1, )
    # if tb_i2 != -1:
    #     plt.plot(t, i2, )
    #     plt.plot(t, i3, )
    # plt.grid(color='grey', linestyle='-', linewidth=0.1)
    # plt.ylabel('I [A]')
    #
    # color = 'tab:red'
    # ax1 = plt.subplot(2, 1, 2)
    # ax1.set_xlabel('t [s]')
    # ax1.set_ylabel('M [Nm]', color=color)
    # ax1.plot(t, M, color=color)
    # ax1.tick_params(axis='y', labelcolor=color)
    # plt.grid(color='grey', linestyle='-', linewidth=0.1)
    #
    # color = 'tab:blue'
    # ax2 = ax1.twinx()
    # ax2.set_ylabel('n [ot/min]', color=color)  # we already handled the x-label with ax1
    # ax2.plot(t, n * 50, color=color)
    # ax2.tick_params(axis='y', labelcolor=color)
    #
    # # plt.show()
    #
    # plt.rcParams['pdf.fonttype'] = 42
    # file = os.path.basename((file).replace('.csv', ''))
    # plt.savefig('pdf/' + file + '.pdf', bbox_inches='tight')
    # plt.close()
    # return 1


# The window
root = tk.Tk()
root.title("List App")
root.geometry("500x400")
root.resizable(height = None, width = None)
root.minsize(450, 350)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

input_frame = LabelFrame(root, text="input", padx=5, pady=5)
input_frame.grid(row=0, column=0, padx=5, pady=5)

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

label_files = Label(input_frame, text=u"Loaded files: ")
label_files.grid(row=1, column=0, columnspan=3, rowspan=1, sticky=W, padx=2, pady=(5,0))

scrollbar = tk.Scrollbar(input_frame, orient=VERTICAL)
scrollbar.grid(row=2, column=0, columnspan=3, rowspan=1, sticky=N+S)


# The listbox
listbox = tk.Listbox(input_frame, selectmode='multiple', yscrollcommand=scrollbar.set)
listbox.grid(row=2, column=0, columnspan=3, rowspan=1, sticky=W+E+N+S, padx=2, pady=2)
listbox.config(yscrollcommand = scrollbar.set)


button_plot = tk.Button(text="Generate Plots", command=generate_plot_button)
button_plot.grid(row=3, column=1, padx=10, pady=10, sticky=W+E)
#

# selected_size = tk.StringVar()
# sizes = (('Small', 'S'),
#          ('Medium', 'M'),
#          ('Large', 'L'),
#          ('Extra Large', 'XL'),
#          ('Extra Extra Large', 'XXL'))

# for i, val in enumerate(sizes):
#     r = ttk.Radiobutton(option_frame1, text=val[0], value=val[1], variable=selected_size)
#     r.grid(row=i, column=0, padx=0, pady=0, sticky=W+E)


for i in range(4):
    globals()[f"label_columns{i}"] = Label(option_frame1, text="column " + str(i + 1) + ":")
    globals()[f"label_columns{i}"].grid(row=i, column=0, columnspan=1, rowspan=1, sticky=W, padx=2, pady=2)

    globals()[f"value_column{i}"] = StringVar(option_frame1)
    globals()[f"value_column{i}"].set(physical_quantity[0])  # default value

    globals()[f"quantity_column{i}"] = OptionMenu(option_frame1, globals()[f"value_column{i}"], *physical_quantity)
    globals()[f"quantity_column{i}"].grid(row=i, column=1, padx=2, pady=2, sticky=W + E)
    globals()[f"quantity_column{i}"].bind("<<ComboboxSelected>>", unit_choose)

    globals()[f"quantity_unit_column{i}"] = ttk.Combobox(option_frame1, value=[" "])
    globals()[f"quantity_unit_column{i}"].current(0)
    globals()[f"quantity_unit_column{i}"].grid(row=i, column=2, padx=2, pady=2, sticky=W + E)



# my_combo = ttk.Combobox(root, value=sizes)
# my_combo.current(0)
# my_combo.pack(pady=20)
# # bind the combobox
# my_combo.bind("<<ComboboxSelected>>", pick_color)
#
# # Color Combo box
# color_combo = ttk.Combobox(root, value=[" "])
# color_combo.current(0)
# color_combo.pack(pady=20)



root.mainloop()










