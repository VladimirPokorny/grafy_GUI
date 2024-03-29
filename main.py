import tkinter as tk
from tkinter import ttk, filedialog, RIGHT, X, Y, W, E, N, S, Label, StringVar, LabelFrame, OptionMenu, messagebox, VERTICAL
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from units import physical_quantity, data, number_columns
import natsort
import glob
from PyPDF2 import PdfFileReader, PdfFileMerger
from scipy.interpolate import make_interp_spline, BSpline
from numpy import sqrt


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
    FileList(natsort.natsorted(filePaths, reverse=False))
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
        tk.messagebox.showinfo(title="Info", message="Plot generation has been successfully completed")

    else:
        print("prázdná množina")
        tk.messagebox.showwarning(title="Warning", message="Add measured data in CSV")


def pdf_merger():
    pdfs = glob.glob("pdf_output/*.pdf")
    pdfs = natsort.natsorted(pdfs, reverse=False)
    print(pdfs)
    print('merging')

    merger = PdfFileMerger()

    for pdf in pdfs:  # iterate over the list of files
       merger.append(PdfFileReader(pdf), 'rb')

    merger.write("pdf_output/all_plots.pdf")
    merger.close()


def generate_plot():
    global files_to_open

    for file in files_to_open:
        table = pd.read_csv(file)

        rozsah1 = 3
        rozsah2 = len(pd.read_csv(file).loc[:, 'x-axis'])
        t = table.iloc[rozsah1:rozsah2, 0]
        t = t.astype(np.float64)
        t_new = np.linspace(t.min(), t.max(), 500)

        u1 = table.iloc[rozsah1:rozsah2, 1]
        u1 = u1.astype(np.float64)
        spl_u1 = make_interp_spline(t, u1, k=5)
        u1_new = spl_u1(t_new)

        u2 = table.iloc[rozsah1:rozsah2, 2]
        u2 = u2.astype(np.float64)
        spl_u2 = make_interp_spline(t, u2, k=5)
        u2_new = spl_u2(t_new)

        u3 = table.iloc[rozsah1:rozsah2, 3]
        u3 = u3.astype(np.float64)
        spl_u3 = make_interp_spline(t, u3, k=5)
        u3_new = spl_u3(t_new)

        plt.figure(figsize=(10, 10))
        name_of_file = str(os.path.basename(file))
        plt.title('Data ze souboru: %s \n' % name_of_file
                  + 'Ui_1_rms = %.3f V' % rms(u1[0:3 * 18940])
                  + '          Ui_1max = %.3f V' % max(u1)
                  + '          Ui_1min = %.3f V \n' % min(u1)
                  + 'Ui_2_rms = %.3f V' % rms(u2[0:3 * 18940])
                  + '          Ui_2max = %.3f V' % max(u2)
                  + '          Ui_2min = %.3f V \n' % min(u2)
                  + 'Ui_3_rms = %.3f V' % rms(u3[0:3 * 18940])
                  + '          Ui_3max = %.3f V' % max(u3)
                  + '          Ui_3min = %.3f V \n' % min(u3)
                 )
        plt.plot(t_new, u1_new, linewidth=2)
        plt.plot(t_new, u2_new, linewidth=2)
        plt.plot(t_new, u3_new, linewidth=2)

        plt.ylabel('Ui [V]')
        plt.xlabel('t [s]')

        if pdf.get() == 0 and preview.get() == 1:
            plt.show()
        else:
            pass

        if pdf.get() == 1:
            create_folder('pdf_output/')
            plt.rcParams['pdf.fonttype'] = 42
            file = os.path.basename((file).replace('.csv', ''))
            plt.savefig('pdf_output/' + file + '.pdf')
            pdf_merger()

            if preview.get() == 1:
                plt.show()
            else:
                pass


def rms(Quantity):
    return sqrt(sum(n * n for n in Quantity) / len(Quantity))


def create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# The window
root = tk.Tk()
root.title("List App")
root.geometry("500x400")

# root.geometry("700x600")
root.resizable(height=None, width=None)
root.minsize(500, 400)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)

input_frame = LabelFrame(root, text="input", padx=5, pady=5)
input_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=N + S + W + E)

input_frame.grid_rowconfigure(1, weight=1)
input_frame.grid_columnconfigure(0, weight=1)
input_frame.grid_columnconfigure(1, weight=1)
input_frame.grid_columnconfigure(2, weight=1)

# option_frame1 = LabelFrame(root, text="option", padx=5, pady=5)
# option_frame1.grid(row=0, column=1, padx=5, pady=5, sticky=N+S+W+E)
#
# option_frame2 = LabelFrame(root, text="option", padx=5, pady=5)
# option_frame2.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=N+S+W+E)

# option_frame.grid_rowconfigure(1, weight=1)
# option_frame.grid_columnconfigure(0, weight=1)
# option_frame.grid_columnconfigure(1, weight=1)
# option_frame.grid_columnconfigure(2, weight=1)

# The button to insert the item in the list
button = tk.Button(input_frame, text="Add Items", command=LoadAction)
button.grid(row=0, column=0, padx=5, pady=5, sticky=W + E)

# the button to delete everything
button_delete = tk.Button(input_frame, text="Delete All", command=delete)
button_delete.grid(row=0, column=2, padx=5, pady=5, sticky=W + E)

# The button to delete only the selected item in the list
button_delete_selected = tk.Button(input_frame, text="Delete Selected", command=call_delete)
button_delete_selected.grid(row=0, column=1, padx=5, pady=5, sticky=W + E)

label_files = Label(input_frame, text="Loaded files: ")
label_files.grid(row=1, column=0, columnspan=3, rowspan=1, sticky=W, padx=2, pady=(5, 0))

scrollbar = tk.Scrollbar(input_frame, orient=VERTICAL)
scrollbar.grid(row=2, column=0, columnspan=3, rowspan=1, sticky=N + S)


# The listbox
listbox = tk.Listbox(input_frame, selectmode='multiple', yscrollcommand=scrollbar.set)
listbox.grid(row=2, column=0, columnspan=3, rowspan=1, sticky=W + E + N + S, padx=2, pady=2)
listbox.config(yscrollcommand=scrollbar.set)


button_plot = tk.Button(root, text="Generate Plots", command=generate_plot_button)
button_plot.grid(row=2, column=1, padx=10, pady=10, sticky=W + E)

pdf = tk.IntVar()
checkbutton_plot_pdf = tk.Checkbutton(root, text="Generate Merged PDFs", variable=pdf, onvalue=1, offvalue=0,)
checkbutton_plot_pdf.grid(row=2, column=0, padx=10, pady=10, sticky=W + E)
checkbutton_plot_pdf.var = pdf

preview = tk.IntVar()
sample_checkbutton = tk.Checkbutton(root, text="View Preview", variable=preview, onvalue=1, offvalue=0,)
sample_checkbutton.grid(row=1, column=0, padx=10, pady=10, sticky=W + E)
sample_checkbutton.var = preview

root.mainloop()
