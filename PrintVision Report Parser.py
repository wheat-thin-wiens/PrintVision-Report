# PrintVision Report Parser by Ethan Wiens
import csv
import os
import os.path
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import ttk

root = tk.Tk()
root.geometry("500x325")
root.title("PrintVision Report")
#root.iconbitmap('printing.ico')

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

def report(location, IP, value):
    model = int(modelCol.get())
    ip = int(ipCol.get())
    asset = int(assetCol.get())
    room = int(roomCol.get())
    black = int(kCol.get())
    cyan = int(cCol.get())
    magenta = int(mCol.get())
    yellow = int(yCol.get())

    with open('report.csv', 'a', newline = '') as csvfile:
        spamwriter = csv.writer(
            csvfile,
            delimiter = ',',
            quotechar = '|',
            quoting = csv.QUOTE_MINIMAL,
        )

    with open(filename, newline = '') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for row in spamreader:
            if IP in row[ip]:
                toner_list = []

                k = row[black].replace('"', '')
                if '%' in k:
                    k = int(k.strip('%'))
                    if k <= value:
                        toner_list.append(f"Black: {k}")

                c = row[cyan].replace('"', '')
                if '%' in c:
                    c = int(c.strip('%'))
                    if c <= value:
                        toner_list.append(f"Cyan: {c}")

                m = row[magenta].replace('"', '')
                if '%' in m:
                    m = int(m.strip('%'))
                    if m <= value:
                        toner_list.append(f"Magenta: {m}")

                y = row[yellow].replace('"', '')
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

                    spamwriter.writerow([location, row[model], row[ip], row[asset], row[room], ' '.join(toner_list)])
                    continue

def run_report(location):
    #os.chdir('/Users/ethanwiens/Downloads')
    os.chdir('C:/Users/Public')

    if os.path.isfile('report.csv'):
        os.remove('report.csv')
        open('report.csv', 'x')
        print('file created')

    hValue = int(hsptlValue.get())
    cValue = int(clncValue.get())

    if location == 'Hospital':
        report('Main Campus', '10.200', hValue)
        report('Main Campus', '10.205', hValue)
    elif location == 'Clinic':
        report('Clinic', '10.210', cValue)
    elif location == 'All':
        report('Main Campus', '10.200', hValue)
        report('Main Campus', '10.205', hValue)
        report('Clinic', '10.210', cValue)

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

    view = messagebox.askyesno("Report Complete", "Would you like to view the report?")
    if view:
        os.system(f"start excel.exe {outLocation}/report.csv")

def notadumbass():
    if btnchck.get() == 1:
        global modelCol_entry, ipCol_entry, assetCol_entry, roomCol_entry, kCol_entry, cCol_entry, mCol_entry, yCol_entry
        modelCol_entry.config(state = 'normal')
        ipCol_entry.config(state = 'normal')
        assetCol_entry.config(state = 'normal')
        roomCol_entry.config(state = 'normal')
        kCol_entry.config(state = 'normal')
        cCol_entry.config(state = 'normal')
        mCol_entry.config(state = 'normal')
        yCol_entry.config(state = 'normal')
    else:
        modelCol_entry.config(state = 'disabled')
        ipCol_entry.config(state = 'disabled')
        assetCol_entry.config(state = 'disabled')
        roomCol_entry.config(state = 'disabled')
        kCol_entry.config(state = 'disabled')
        cCol_entry.config(state = 'disabled')
        mCol_entry.config(state = 'disabled')
        yCol_entry.config(state = 'disabled')

def create_gui():
    # Tabbed UI
    tabs = ttk.Notebook(root)
    tabs.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'n')

    frame1 = ttk.Frame(tabs, width = 400, height = 280)
    frame2 = ttk.Frame(tabs, width = 400, height = 280)
    frame3 = ttk.Frame(tabs, width = 400, height = 280)
    frame1.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'n')
    frame2.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = 'n')
    frame3.grid(row = 0, column = 2, padx = 10, pady = 5, sticky = 'n')
    tabs.add(frame1, text = "Report")
    tabs.add(frame2, text = "Configure")
    tabs.add(frame3, text = 'Info')

    #canvas = tk.Canvas(frame2, width = 400, height = 280)
    #canvas.grid(row = 0, column = 0)
    #scrollbar = ttk.Scrollbar(frame2, orient = 'vertical', command = canvas.yview)
    #scrollbar.grid(row = 0, column = 2, rowspan = 10, sticky = 'e')
    #canvas.config(yscrollcommand=scrollbar.set, scrollregion=(0,0,100,100))
    #frame = tk.Frame(canvas, bg='white', width=200, height=100)
    #canvas.create_window(100, 500, window=frame)
    
    # Report Tab
    global fileVar, runBtn, statusVar, hsptlValue, clncValue, outVar

    fileVar = tk.StringVar(value = "No file selected")
    statusVar = tk.StringVar(value = "Ready")
    hsptlValue = tk.StringVar(value = '5')
    clncValue = tk.StringVar(value = '10')
    outVar = tk.StringVar(value = 'No destination selected')

    openBtn = tk.Button(frame1, text = "Open File", command = open_file)
    openBtn.grid(row = 5, column = 3, padx = 10, pady = 10, sticky = 'se')

    runBtn = tk.Button(frame1, text = "Run", state = 'disabled', command = lambda:run_report(location_dropdown.get()))
    runBtn.grid(row = 5, column = 4, padx = 10, pady = 10, sticky = 'se')

    inputFrame = tk.Frame(frame1)
    inputFrame['borderwidth'] = 2
    inputFrame['relief'] = 'groove'
    inputFrame.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10, sticky = 'nwe')

    location_dropdown = ttk.Combobox(
        inputFrame,
        state = "readonly",
        values = ['All', 'Hospital', 'Clinics'],
        width = 20,
    )
    location_dropdown.current(0)
    location_dropdown.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = 'nw')

    location_label = tk.Label(inputFrame, text = "Location:")
    location_label.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'nw')

    hsptlValue_entry = ttk.Entry(inputFrame, textvariable = hsptlValue, width = 23)
    hsptlValue_entry.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = 'nw')

    hsptlValue_label = tk.Label(inputFrame, text = "Hospital Value:")
    hsptlValue_label.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = 'nw')

    clncValue_entry = ttk.Entry(inputFrame, textvariable = clncValue, width = 23)
    clncValue_entry.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = 'nw')

    clncValue_label = tk.Label(inputFrame, text = "Clinic Value:")
    clncValue_label.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = 'nw')

    file_label = tk.Label(inputFrame, text = 'File Selected:')
    file_label.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = 'nw')

    fileVarlabel = tk.Label(inputFrame, textvariable = fileVar, width = 23, anchor = 'w')
    fileVarlabel.grid(row = 3, column = 1, padx = 10, pady = 10, sticky = 'nw')

    output_label = tk.Label(inputFrame, text = "Output Destination:")
    output_label.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = 'nw')

    destination_label = tk.Label(inputFrame, textvariable = outVar, width = 23, anchor = 'w')
    destination_label.grid(row = 4, column = 1, padx = 10, pady = 10, sticky = 'nw')

    stsLabel = tk.Label(frame1, textvariable = statusVar, anchor = 'w')
    stsLabel.grid(row = 5, column = 0, padx = 10, pady = 10, sticky = 'nw')

    #dumbbutton = tk.Button(root, text = 'dumb', command = printy)
    #dumbbutton.grid(row = 4, column = 1, padx = 10, pady = 5, sticky = 'nw')

    # Config Tab
    global modelCol, ipCol, assetCol, roomCol, kCol, cCol, mCol, yCol
    global modelCol_entry, ipCol_entry, assetCol_entry, roomCol_entry, kCol_entry, cCol_entry, mCol_entry, yCol_entry
    global btnchck

    modelCol = tk.StringVar(value = 0)
    ipCol = tk.StringVar(value = 2)
    assetCol = tk.StringVar(value = 3)
    roomCol = tk.StringVar(value = 4)
    kCol = tk.StringVar(value = 6)
    cCol = tk.StringVar(value = 7)
    mCol = tk.StringVar(value = 8)
    yCol = tk.StringVar(value = 9)

    btnchck = tk.IntVar()

    modelCol_label = tk.Label(frame2, text = "Model Column:")
    modelCol_label.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'nw')
    modelCol_entry = ttk.Entry(frame2, textvariable = modelCol, width = 20, state = 'disabled')
    modelCol_entry.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = 'nw')

    ipCol_label = tk.Label(frame2, text = "IP Column:")
    ipCol_label.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'nw')
    ipCol_entry = ttk.Entry(frame2, textvariable = ipCol, width = 20, state = 'disabled')
    ipCol_entry.grid(row = 1, column = 1, padx = 10, pady = 5, sticky = 'nw')

    assetCol_label = tk.Label(frame2, text = "Asset Column:")
    assetCol_label.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = 'nw')
    assetCol_entry = ttk.Entry(frame2, textvariable = assetCol, width = 20, state = 'disabled')
    assetCol_entry.grid(row = 2, column = 1, padx = 10, pady = 5, sticky = 'nw')

    roomCol_label = tk.Label(frame2, text = "Room Column:")
    roomCol_label.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'nw')
    roomCol_entry = ttk.Entry(frame2, textvariable = roomCol, width = 20, state = 'disabled')
    roomCol_entry.grid(row = 3, column = 1, padx = 10, pady = 5, sticky = 'nw')

    kCol_label = tk.Label(frame2, text = "Black Column:")
    kCol_label.grid(row = 4, column = 0, padx = 10, pady = 5, sticky = 'nw')
    kCol_entry = ttk.Entry(frame2, textvariable = kCol, width = 20, state = 'disabled')
    kCol_entry.grid(row = 4, column = 1, padx = 10, pady = 5, sticky = 'nw')

    cCol_label = tk.Label(frame2, text = 'Cyan Column:')
    cCol_label.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = 'nw')
    cCol_entry = ttk.Entry(frame2, textvariable = cCol, width = 20, state = 'disabled')
    cCol_entry.grid(row = 5, column = 1, padx = 10, pady = 5, sticky = 'nw')

    mCol_label = tk.Label(frame2, text = 'Magenta Column:')
    mCol_label.grid(row = 6, column = 0, padx = 10, pady = 5, sticky = 'nw')
    mCol_entry = ttk.Entry(frame2, textvariable = mCol, width = 20, state = 'disabled')
    mCol_entry.grid(row = 6, column = 1, padx = 10, pady = 5, sticky = 'nw')

    yCol_label = tk.Label(frame2, text = "Yellow Column:")
    yCol_label.grid(row = 7, column = 0, padx = 10, pady = 5, sticky = 'nw')
    yCol_entry = ttk.Entry(frame2, textvariable = yCol, width = 20, state = 'disabled')
    yCol_entry.grid(row = 7, column = 1, padx = 10, pady = 5, sticky = 'nw')

    dumbass_check = tk.Checkbutton(frame2, text = "I know what I'm doing", variable = btnchck, onvalue = 1, offvalue = 0, command = notadumbass)
    dumbass_check.grid(row = 8, column = 0, padx = 10, pady = 5, sticky = 'nw')

    # Info Tab
    info_text = tk.Label(frame3, text = 'Intended for use with PrintVision toner reports.')
    info_text.grid(row = 0, column = 0)
    copyright = tk.Label(frame3, text = '© 2024 - Ethan Wiens - All Rights Reserved', anchor = 'w')
    copyright.grid(row = 1, column = 0)

    root.columnconfigure([0, 1], weight = 1)
    #root.rowconfigure([1, 0], weight = 1)

if __name__ == '__main__':
    create_gui()
    root.mainloop()
