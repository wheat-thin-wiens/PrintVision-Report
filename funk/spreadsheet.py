import csv
import os, os.path
from tkinter import filedialog as fd, messagebox

def open_file(button, fileVar):
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
        button.config(state = 'normal' if fileVar != "No file selected" else 'disabled')
        return filename
    else:
        return

def which_csv(file, location, hValue, cValue):
    #os.chdir('/Users/ethanwiens/Downloads')
    os.chdir('C:/Users/Public')

    if os.path.isfile('report.csv'):
        os.remove('report.csv')
        open('report.csv', 'x')
        print('file created')

    if location == 'Hospital':
        csv_report(file, '10.200', hValue)
        csv_report(file, '10.205', hValue)
    elif location == 'Clinic':
        csv_report(file, '10.210', cValue)
    elif location == 'All':
        csv_report(file, '10.200', hValue)
        csv_report(file, '10.205', hValue)
        csv_report(file, '10.210', cValue)

    outLocation = fd.askdirectory(
        title = "Save new report",
        initialdir = "/"
    )
    saved = False
    while not saved:
        try:
            outLocation = fd.askdirectory(
            title = "Save new report",
            initialdir = "/"
        )
            
            if len(outLocation) > 0:
                os.replace('C:/Users/Public/report.csv', f"{outLocation}/report.csv")
            else:
                os.remove("C:/Users/Public/report.csv")
            saved = True
        except PermissionError:
            file_error = messagebox.showwarning("Unable to save", "If a previous report is still open, make sure you close it before running another report.")
            #htmlstatusVar.set('Run Report')
            continue
    
    view = messagebox.askyesno("Report Complete", "Would you like to view the report?")
    if view:
        os.system(f"start excel.exe {outLocation}/report.csv")

def csv_report(file, IP, value):
    with open('report.csv', 'a', newline = '') as csvfile:
        spamwriter = csv.writer(
            csvfile,
            delimiter = ',',
            quotechar = '|',
            quoting = csv.QUOTE_MINIMAL,
        )

    with open(file, newline = '') as csvfile:
        spamreader = csv.reader(csvfile, delimiter = ',', quotechar = '|')

        for row in spamreader:
            list = []
            list_copy = []

            for x in row:
                list.append(x)
                list_copy.append(x)

            if IP in list[2]:
                toner_list = []

                try:
                    toner_list = []
                    k = list[6].replace('"', '')
                    k = int(k.strip('%'))
                    if k <= value:
                        list[6] = f"{k}%"
                        toner_list.append(k)
                    else:
                        list[6] = ' '
                        continue

                    c = list[7].replace('"', '')
                    c = int(c.strip('%'))
                    if c <= value:
                        list[7] = f"{c}%"
                        toner_list.append(c)
                    else:
                        list[7] = ' '
                        continue

                    m = list[8].replace('"', '')
                    m = int(m.strip('%'))
                    if m <= value:
                        list[8] = f"{m}%"
                        toner_list.append(m)
                    else:
                        list[8] = ' '
                        continue

                    y = list[9].replace('"', '')
                    y = int(y.strip('%'))
                    if y <= value:
                        list[9] = f"{y}%"
                        toner_list.append(y)
                    else:
                        list[9] = ' '
                        continue
                except TypeError:
                    continue

                if len(toner_list) == 0:
                    continue
                
                with open('report.csv', 'a', newline = '') as csvfile:
                    spamwriter = csv.writer(
                        csvfile,
                        delimiter = ',',
                        quotechar = '|',
                        quoting = csv.QUOTE_MINIMAL,
                    )

                    spamwriter.writerow(list)
                    continue
