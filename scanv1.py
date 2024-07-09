import csv
import os.path
import tkinter as tk
from tkinter import CENTER, StringVar
from tkinter import filedialog as fd

# Window
root = tk.Tk()
root.geometry("300x300")
root.title("CSV Report")
root.iconbitmap()

global textVar
textVar = StringVar()
textVar.set("Ready.")

# Open File
def file_open():
    global filename
    filename = fd.askopenfilename(
        title = 'Open a file',
        initialdir = '/Downloads',
        filetypes = (
            ("CSV Files", "*.csv"),
            ("All Files", "*.*"),
        )
    )

    textVar.set(f"File selected: {os.path.basename(filename)}")

# Run Report
def run_report():
    os.chdir('/Users/ethanwiens/Downloads')
    #os.chdir('/Downloads')

    if os.path.isfile('report.csv'):
        os.remove('report.csv')
        open('report.csv', 'x')

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

            elif '10.210' in row[2]:
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

    textVar.set("Report complete.")

# Button Frame
btnFrame = tk.Frame(
    root,
    height = 100
).place(
    relx = 0.5,
    rely = 0.5,
    anchor = CENTER
)

# Open File Button
fileBtn = tk.Button(
    btnFrame,
    text = "Open",
    width = 5,
    command = file_open,
    cursor = 'gumby',
).grid(
    row = 0,
    column = 0,
    sticky = tk.N,
    pady = 10
)

# Run Report Button
runBtn = tk.Button(
    btnFrame,
    text = "Run",
    width = 5,
    command = run_report,
    cursor = 'gumby'
).grid(
    row = 1,
    column = 0,
    sticky = tk.N,
    pady = 10
)

# Status Label
statusLabel = tk.Label(
    root,
    textvariable = textVar,
    wraplength = 200,
    justify = 'left'
).grid(
    row = 0,
    column = 1,
    sticky = tk.E,
    pady = 10
)

root.mainloop()
