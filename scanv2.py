# PrintVision Report by Ethan Wiens
import csv
import os
import os.path
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import ttk

root = tk.Tk()
root.geometry("400x280")
root.title("PrintVision Report")
root.iconbitmap('printing.ico')

def open_file():
    global filename
    filename = fd.askopenfilename(
        title = "Open file",
        initialdir = '/',
        filetypes = (
            ('CSV Files', '*.csv'),
            #('All Files', '*.*'),
        )
    )

    if len(filename) > 0:
        fileVar.set(f"{os.path.basename(filename)}")
        runBtn.config(state = 'normal' if fileVar != "No file selected" else 'disabled')
    else:
        return

def hospital_report():
    value = int(hsptlValue.get())

    with open('report.csv', 'w', newline = '') as csvfile:
        spamwriter = csv.writer(
            csvfile,
            delimiter = ',',
            quotechar = '|',
            quoting = csv.QUOTE_MINIMAL,
        )

    with open(filename, newline = '') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for row in spamreader:
            if '10.200' in row[2]:
                toner_list = []

                k = row[6].replace('"', '')
                if '%' in k:
                    k = int(k.strip('%'))
                    if k <= value:
                        toner_list.append(f"Black: {k}")

                c = row[7].replace('"', '')
                if '%' in c:
                    c = int(c.strip('%'))
                    if c <= value:
                        toner_list.append(f"Cyan: {c}")

                m = row[8].replace('"', '')
                if '%' in m:
                    m = int(m.strip('%'))
                    if m <= value:
                        toner_list.append(f"Magenta: {m}")

                y = row[9].replace('"', '')
                if '%' in y:
                    y = int(y.strip('%'))
                    if y <= value:
                        toner_list.append(f"Yellow: {y}")

                if len(toner_list) < 1:
                    continue

                with open('report.csv', 'a', newline = '') as csvfile:
                    spamwriter = csv.writer(
                        csvfile,
                        delimiter = ',',
                        quotechar = '|',
                        quoting = csv.QUOTE_MINIMAL,
                    )

                    spamwriter.writerow(['Main Campus', row[0], row[2], row[3], row[4], toner_list])
                    continue

            elif '10.205' in row[2]:
                toner_list = []

                k = row[6].replace('"', '')
                if '%' in k:
                    k = int(k.strip('%'))
                    if k <= value:
                        toner_list.append(f"Black: {k}")

                c = row[7].replace('"', '')
                if '%' in c:
                    c = int(c.strip('%'))
                    if c <= value:
                        toner_list.append(f"Cyan: {c}")

                m = row[8].replace('"', '')
                if '%' in m:
                    m = int(m.strip('%'))
                    if m <= value:
                        toner_list.append(f"Magenta: {m}")

                y = row[9].replace('"', '')
                if '%' in y:
                    y = int(y.strip('%'))
                    if y <= value:
                        toner_list.append(f"Yellow: {y}")

                if len(toner_list) < 1:
                    continue

                with open('report.csv', 'a', newline = '') as csvfile:
                    spamwriter = csv.writer(
                        csvfile,
                        delimiter = ',',
                        quotechar = '|',
                        quoting = csv.QUOTE_MINIMAL,
                    )

                    spamwriter.writerow(['Main Campus', row[0], row[2], row[3], row[4], toner_list])
                    continue

def clinic_report():
    value = int(clncValue.get())

    with open('report.csv', 'w', newline = '') as csvfile:
        spamwriter = csv.writer(
            csvfile,
            delimiter = ',',
            quotechar = '|',
            quoting = csv.QUOTE_MINIMAL,
        )

    with open(filename, newline = '') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for row in spamreader:
            if '10.210' in row[2]:
                toner_list = []

                k = row[6].replace('"', '')
                if '%' in k:
                    k = int(k.strip('%'))
                    if k <= value:
                        toner_list.append(f"Black: {k}")

                c = row[7].replace('"', '')
                if '%' in c:
                    c = int(c.strip('%'))
                    if c <= value:
                        toner_list.append(f"Cyan: {c}")

                m = row[8].replace('"', '')
                if '%' in m:
                    m = int(m.strip('%'))
                    if m <= value:
                        toner_list.append(f"Magenta: {m}")

                y = row[9].replace('"', '')
                if '%' in y:
                    y = int(y.strip('%'))
                    if y <= value:
                        toner_list.append(f"Yellow: {y}")

                if len(toner_list) < 1:
                    continue

                with open('report.csv', 'a', newline = '') as csvfile:
                    spamwriter = csv.writer(
                        csvfile,
                        delimiter = ',',
                        quotechar = '|',
                        quoting = csv.QUOTE_MINIMAL,
                    )

                    spamwriter.writerow(['Clinic', row[0], row[2], row[3], row[4], toner_list])
                    continue

def run_report(location):
    #os.chdir('/Users/ethanwiens/Downloads')
    os.chdir('C:/Users/Public')

    if os.path.isfile('report.csv'):
        os.remove('report.csv')
        open('report.csv', 'x')

    if location == 'Hospital':
        hospital_report()
    elif location == 'Clinic':
        clinic_report()
    elif location == 'All':
        hospital_report()
        clinic_report()

    time.sleep(1)
    statusVar.set("Report complete.")

    outLocation = fd.askdirectory(
        title = "Save new report",
        initialdir = "/"
    )

    if len(outLocation) > 0:
        outVar.set(f"{outLocation}")
        os.replace('C:/Users/Public/report.csv', f"{outLocation}/report.csv")
    else:
        os.remove("C:/Users/Public/report.csv")

    #messagebox.askyesno("Report Complete", "Would you like to view the report?")

def create_gui():
    global fileVar, runBtn, statusVar, hsptlValue, clncValue, outVar

    fileVar = tk.StringVar(value = "No file selected")
    statusVar = tk.StringVar(value = "Ready")
    hsptlValue = tk.StringVar(value = '5')
    clncValue = tk.StringVar(value = '10')
    outVar = tk.StringVar(value = 'No destination selected')

    # Open Button
    openBtn = tk.Button(root, text = "Open File", command = open_file)
    openBtn.grid(row = 5, column = 1, padx = 10, pady = 10, sticky = 'se')

    # Run Button
    runBtn = tk.Button(root, text = "Run", state = 'disabled', command = lambda:run_report(location_dropdown.get()))
    runBtn.grid(row = 5, column = 2, padx = 10, pady = 10, sticky = 'se')

    # Input Frame
    inputFrame = tk.Frame(root)
    inputFrame['borderwidth'] = 5
    inputFrame['relief'] = 'groove'
    inputFrame.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10, sticky = 'nwe')

    # Location Select
    location_dropdown = ttk.Combobox(
        inputFrame,
        state = "readonly",
        values = ['', 'Hospital', 'Clinics', 'All'],
        width = 20,
    )
    location_dropdown.current(0)
    location_dropdown.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = 'nw')

    location_label = tk.Label(inputFrame, text = "Location:")
    location_label.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'nw')

    # Value Select
    hsptlValue_entry = ttk.Entry(inputFrame, textvariable = hsptlValue, width = 23)
    hsptlValue_entry.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = 'nw')

    hsptlValue_label = tk.Label(inputFrame, text = "Hospital Value:")
    hsptlValue_label.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = 'nw')

    clncValue_entry = ttk.Entry(inputFrame, textvariable = clncValue, width = 23)
    clncValue_entry.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = 'nw')

    clncValue_label = tk.Label(inputFrame, text = "Clinic Value:")
    clncValue_label.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = 'nw')

    # File name label
    file_label = tk.Label(inputFrame, text = 'File Selected:')
    file_label.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = 'nw')

    fileVarlabel = tk.Label(inputFrame, textvariable = fileVar)
    fileVarlabel.grid(row = 3, column = 1, padx = 10, pady =10, sticky = 'nw')

    # Output Label
    output_label = tk.Label(inputFrame, text = "Output Destination:")
    output_label.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = 'nw')

    destination_label = tk.Label(inputFrame, textvariable = outVar)
    destination_label.grid(row = 4, column = 1, padx = 10, pady = 10, sticky = 'nw')

    # Status label
    stsLabel = tk.Label(root, textvariable = statusVar)
    stsLabel.grid(row = 5, column = 0, padx = 10, pady = 10, sticky = 'nw')

    #dumbbutton = tk.Button(root, text = 'dumb', command = printy)
    #dumbbutton.grid(row = 4, column = 1, padx = 10, pady =10, sticky = 'nw')

    root.columnconfigure([0, 1], weight = 1)
    #root.rowconfigure([1, 0], weight = 1)

if __name__ == '__main__':
    create_gui()
    root.mainloop()
