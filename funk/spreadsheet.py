from . import blacklist
import csv
import os, os.path
import platform
import tkinter as tk
from tkinter import filedialog as fd, messagebox

global ope
ope = platform.system()

def open_file(location, hValue, cValue, blist, fileVar, outVar):
    file_chosen = False

    while not file_chosen:
        file = fd.askopenfilename(
            title = "Open file",
            initialdir = '/',
            filetypes = (
                ('CSV Files', '*.csv'),
                #('All Files', '*.*'),
            )
        )

        if len(file) > 0:
            file_chosen = True
            fileVar.set(os.path.basename(file))
            which_csv(file, location, hValue, cValue, blist, outVar)
        else:
            continue

def which_csv(file, location, hValue, cValue, blist, outVar):
    match ope:
        case "Windows":
            initDir = "C:/Users/Public"
            os.chdir(initDir)
        case "Darwin":
            initDir = "/Users/ethanwiens/dev/PrintVision-Report"
            os.chdir(initDir)
        case "Linux":
            initDir = "/Users/ethanwiens/dev/PrintVision-Report"
            os.chdir(initDir)

    if os.path.isfile('report.csv'):
        os.remove('report.csv')
        open('report.csv', 'x')
        print('file created')

    if location == 'Hospital':
        print('Hospital Results:')
        csv_report(file, '10.200', hValue, blist)
        print('CSC Results:')
        csv_report(file, '10.205', hValue, blist)
    elif location == 'Clinic':
        print('Clinic Results:')
        csv_report(file, '10.210', cValue, blist)
    elif location == 'All':
        print('Hospital Results:')
        csv_report(file, '10.200', hValue, blist)
        print('CSC Results:')
        csv_report(file, '10.205', hValue, blist)
        print('Clinic Results:')
        csv_report(file, '10.210', cValue, blist)

    saved = False
    while not saved:
        try:
            outLocation = fd.askdirectory(
            title = "Save new report",
            initialdir = "/"
        )
            
            if len(outLocation) > 0:
                os.replace(f"{initDir}/report.csv", f"{outLocation}/report.csv")  #type: ignore
                outVar.set(outLocation)
            else:
                os.remove(f"{initDir}/report.csv")  #type: ignore
            saved = True
            break
        except PermissionError:
            messagebox.showwarning("Unable to save", "If a previous report is still open, make sure you close it before running another report.")
            continue
    
    view = messagebox.askyesno("Report Complete", "Would you like to view the report?")
    if view:
        os.system(f"start excel.exe {outLocation}/report.csv")  #type: ignore



def csv_report(file, IP, value, blist):
    row_count = 0

    with open('report.csv', 'a', newline = '') as writefile:
        spamwriter = csv.writer(
            writefile,
            delimiter = ',',
            quotechar = '|',
            quoting = csv.QUOTE_MINIMAL,
        )

        with open(file, newline = '') as readfile:
            spamreader = csv.reader(readfile, delimiter = ',', quotechar = '|')

            '''
            K = row[6]
            C = row[7]
            M = row[8]
            Y = row[9]
            '''

            for row in spamreader:
                list = []

                for x in row:
                    list.append(x)

                if IP in list[2]:
                    toners = []

                    black = csvToner(list[6], value, toners)
                    cyan = csvToner(list[7], value, toners)
                    magenta = csvToner(list[8], value, toners)
                    yellow = csvToner(list[9], value, toners)

                    if len(toners) > 0:
                        if blist:
                            checkedList = blacklist.checkBlacklist(list)
                            if len(checkedList) > 0:
                                row_count += 1
                                # print(f'\rRows Added: ({row_count})', end = '')
                                spamwriter.writerow(checkedList)
                            else:
                                continue
                        elif not blist:
                            row_count += 1
                            # print(f'\rRows Added: ({row_count})', end = '')
                            spamwriter.writerow(list)

                else:
                    continue
        
    print(f'Rows added: {row_count}')

def csvToner(toner: str, value: int, tonerList: list):
    toner = toner.replace('"', '').strip("%")

    try:
        if int(toner) <= value:
            tonerList.append(toner)
            return f"{toner}%"
        else:
            return ""

    except TypeError:
        return
    except ValueError:
        return
