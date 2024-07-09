import csv
import os.path
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk

root = tk.Tk()
root.geometry("700x500")
root.title("Toner Report Scanner")

def open_file():
    filename = fd.askopenfilename(
        title = "Open a file",
        initialdir = '/Downloads',
        filetypes = (
            ('CSV Files', '*.csv'),
            #('All Files', '*.*'),
        )
    )

    fileVar.set(f"{os.path.basename(filename)}")
    runBtn.config(state = 'normal' if fileVar != "No file selected" else 'disabled')

def hospital_report():
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
                    if k <= 5:
                        toner_list.append(f"Black: {k}")

                c = row[7].replace('"', '')
                if '%' in c:
                    c = int(c.strip('%'))
                    if c <= 5:
                        toner_list.append(f"Cyan: {c}")

                m = row[8].replace('"', '')
                if '%' in m:
                    m = int(m.strip('%'))
                    if m <= 5:
                        toner_list.append(f"Magenta: {m}")

                y = row[9].replace('"', '')
                if '%' in y:
                    y = int(y.strip('%'))
                    if y <= 5:
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
                    if k <= 5:
                        toner_list.append(f"Black: {k}")

                c = row[7].replace('"', '')
                if '%' in c:
                    c = int(c.strip('%'))
                    if c <= 5:
                        toner_list.append(f"Cyan: {c}")

                m = row[8].replace('"', '')
                if '%' in m:
                    m = int(m.strip('%'))
                    if m <= 5:
                        toner_list.append(f"Magenta: {m}")

                y = row[9].replace('"', '')
                if '%' in y:
                    y = int(y.strip('%'))
                    if y <= 5:
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
                    if k <= 10:
                        toner_list.append(f"Black: {k}")

                c = row[7].replace('"', '')
                if '%' in c:
                    c = int(c.strip('%'))
                    if c <= 10:
                        toner_list.append(f"Cyan: {c}")

                m = row[8].replace('"', '')
                if '%' in m:
                    m = int(m.strip('%'))
                    if m <= 10:
                        toner_list.append(f"Magenta: {m}")

                y = row[9].replace('"', '')
                if '%' in y:
                    y = int(y.strip('%'))
                    if y <= 10:
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
    os.chdir('/Users/ethanwiens/Downloads')
    #os.chdir('/Downloads')

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

    statusVar.set("Report complete.")

def create_gui():
    global filename, fileVar, runBtn, statusVar, valueVar

    fileVar = tk.StringVar(value = "No file selected")
    statusVar = tk.StringVar(value = "Ready")
    valueVar = tk.StringVar(value = '0')

    # Open Button
    openBtn = tk.Button(text = "Open File", command = open_file)
    openBtn.grid(row = 3, column = 2, padx = 10, pady = 10, sticky = 'se')

    # Run Button
    runBtn = tk.Button(text = "Run", state = 'disabled', command = lambda:run_report(location_dropdown.get()))
    runBtn.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = 'se')

    # Location Select
    location_dropdown = ttk.Combobox(
        state = "readonly",
        values = ['', 'Hospital', 'Clinics', 'All'],
        width = 20,
    )
    location_dropdown.current(0)
    location_dropdown.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = 'nw')

    location_label = tk.Label(root, text = "Location")
    location_label.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'nw')

    # Value Select
    value_entry = ttk.Entry(root, textvariable = valueVar, width = 20)
    value_entry.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = 'nw')

    value_label = tk.Label(root, text = "Value")
    value_label.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = 'nw')

    # File name label
    file_label = tk.Label(root, text = 'File Selected:')
    file_label.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = 'nw')

    # Status label


    # File Preview


    root.columnconfigure([0, 1], weight = 1)
    root.rowconfigure(1, weight = 1)

if __name__ == '__main__':
    create_gui()
    root.mainloop()
