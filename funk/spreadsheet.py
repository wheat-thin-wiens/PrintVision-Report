from . import blacklist
import csv
import os, os.path
import platform
from tkinter import filedialog as fd, messagebox

global ope
ope = platform.system()

def open_file(location, hValue, cValue, blist):
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
            which_csv(file, location, hValue, cValue, blist)
        else:
            continue

def which_csv(file, location, hValue, cValue, blist):
    #os.chdir('/Users/ethanwiens/Downloads')
    os.chdir('C:/Users/Public')

    if os.path.isfile('report.csv'):
        os.remove('report.csv')
        open('report.csv', 'x')
        print('file created')

    if location == 'Hospital':
        csv_report(file, '10.200', hValue, blist)
        csv_report(file, '10.205', hValue, blist)
    elif location == 'Clinic':
        csv_report(file, '10.210', cValue, blist)
    elif location == 'All':
        csv_report(file, '10.200', hValue, blist)
        csv_report(file, '10.205', hValue, blist)
        csv_report(file, '10.210', cValue, blist)

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
            break
        except PermissionError:
            messagebox.showwarning("Unable to save", "If a previous report is still open, make sure you close it before running another report.")
            continue
    
    view = messagebox.askyesno("Report Complete", "Would you like to view the report?")
    if view:
        os.system(f"start excel.exe {outLocation}/report.csv")

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

                    try:
                        black = list[6].replace('"', '')
                        black = black.strip('%')
                        black = int(black)
                        if black <= value:
                            list[6] = f'{black}%'
                            toners.append(black)
                        else:
                            list[6] = ' '
                            
                    except TypeError:
                        # print('black type error')
                        pass
                    except ValueError:
                        # print('black value error')
                        pass

                    try:
                        cyan = list[7].replace('"', '')
                        cyan = int(cyan.strip('%'))
                        if cyan <= value:
                            list[7] = f'{cyan}%'
                            toners.append(cyan)
                        else:
                            list[7] = ' '
                            
                    except TypeError:
                        # print('cyan type error')
                        pass
                    except ValueError:
                        # print('cyan value error')
                        pass

                    try:
                        magenta = list[8].replace('"', '')
                        magenta = int(magenta.strip('%'))
                        if magenta <= value:
                            list[8] = f'{magenta}%'
                            toners.append(magenta)
                        else:
                            list[8] = ' '
                            
                    except TypeError:
                        # print('magenta type error')
                        pass
                    except ValueError:
                        # print('magenta value error')
                        pass

                    try:
                        yellow = list[9].replace('"', '')
                        yellow = int(yellow.strip('%'))
                        if yellow <= value:
                            list[9] = f'{yellow}%'
                            toners.append(yellow)
                        else:
                            list[9] = ' '
                    except TypeError:
                        # print('yellow type error')
                        pass
                    except ValueError:
                        # print('yellow value error')
                        pass

                    if len(toners) > 0:
                        if blist:
                            checkedList = blacklist.csvCheckBlacklist(list)
                            if len(checkedList) > 0:
                                row_count += 1
                                print(f'\rRows Added: ({row_count})', end = '')
                                spamwriter.writerow(checkedList)
                            else:
                                continue
                        elif not blist:
                            row_count += 1
                            print(f'\rRows Added: ({row_count})', end = '')
                            spamwriter.writerow(list)

                else:
                    continue