from . import blacklist, gooey
import csv
import os, os.path
import platform
from tkinter import filedialog as fd

global ope
ope = platform.system()

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

    data = readReport(file)
    writeHeader(data[0])

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

    with open('report.csv', 'a', newline = '') as writefile:
        spamwriter = csv.writer(
            writefile,
            delimiter = ',',
            quotechar = '|',
            quoting = csv.QUOTE_MINIMAL,
        )

        for row in data:
            list = [x for x in row]
            toners = []
            black = list[6]
            cyan = list[7]
            magenta = list[8]
            yellow = list[9]

            if IP in list[2]:
                list[6] = csvToner(black, value, toners)
                list[7] = csvToner(cyan, value, toners)
                list[8] = csvToner(magenta, value, toners)
                list[9] = csvToner(yellow, value, toners)

                if len(toners) > 0:
                    if blist:
                        checkedList = blacklist.checkBlacklist(list)
                        if len(checkedList) > 0:
                            row_count += 1
                            spamwriter.writerow(checkedList)
                        else:
                            continue
                    elif not blist:
                        row_count += 1
                        spamwriter.writerow(list)

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
    
def writeHeader(header: list):
    with open('report.csv', 'a', newline = '') as writefile:
        spamwriter = csv.writer(
            writefile,
            delimiter = ',',
            quotechar = '|',
            quoting = csv.QUOTE_MINIMAL,
        )

        spamwriter.writerow(header)