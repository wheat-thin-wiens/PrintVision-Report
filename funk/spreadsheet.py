from . import blacklist, gooey, files
import csv
import os, os.path
from tkinter import filedialog as fd

def open_file(location, hValue: int, cValue: int, blist: bool, fileVar):
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
            which_csv(file, location, hValue, cValue, blist)
        else:
            continue

def which_csv(file, location, hValue, cValue, blist):
    initDir = files.createFile()

    data = readReport(file)
    files.writeLine(data[0])

    if location == 'Hospital':
        csv_report(data, '10.200', hValue, blist)
        csv_report(data, '10.205', hValue, blist)
    elif location == 'Clinic':
        csv_report(data, '10.210', cValue, blist)
    elif location == 'All':
        csv_report(data, '10.200', hValue, blist)
        csv_report(data, '10.205', hValue, blist)
        csv_report(data, '10.210', cValue, blist)

    gooey.saveDialog(initDir)

def csv_report(data: list, IP: str, value: int, blist: bool):
    row_count = 0

    for row in data:
        line = [x for x in row]
        toners = []
        black = line[6]
        cyan = line[7]
        magenta = line[8]
        yellow = line[9]

        if IP in line[2]:
            line[6] = csvToner(black, value, toners)
            line[7] = csvToner(cyan, value, toners)
            line[8] = csvToner(magenta, value, toners)
            line[9] = csvToner(yellow, value, toners)
        else:
            continue
        
        if len(toners) > 0:
            row_count = files.readLine(line, row_count, blist)
        else:
            continue

    match IP:
        case "10.200":    
            print(f'Hospital: {row_count}')
        case "10.205":
            print(f'CSC: {row_count}')
        case "10.210":
            print(f"Clinics: {row_count}")           

def csvToner(toner: str, value: int, tonerList: list):
    toner = toner.replace('"', '').strip("%")

    try:
        if int(toner) <= value:
            tonerList.append(toner)
            return f"{toner}%"
        else:
            return ""

    except TypeError:
        return ' '
    except ValueError:
        return ' '

def readReport(file):
    with open(file, newline = '') as readfile:
        spamreader = csv.reader(
            readfile,
            delimiter = ',',
            quotechar = '|'
        )

        data = [x for x in spamreader]
        return data
    