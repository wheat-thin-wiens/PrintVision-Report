import json
import os, os.path
import platform
from . import blacklist, spreadsheet, web
import tkinter as tk
from tkinter import ttk

global ope
ope = platform.system()

def create_gui(window, appVer):
# Tabbed UI
    tabs = ttk.Notebook(window)
    tabs.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'n')

    ## HTML Tab
    global username, password, htmlstatusVar, html_hsptlValue, html_clncValue, html_location_dropdown, useBlacklist
    
    htmlstatusVar = tk.StringVar(value = "Run Report")
    html_hsptlValue = tk.StringVar(value = '5')
    html_clncValue = tk.StringVar(value = '10')
    useBlacklist = tk.BooleanVar()
    
    try:
        if ope == "Windows":
            os.chdir('C:/Users/Public')

        with open('printvision.json') as file:
            data = json.load(file)
            username = tk.StringVar(value = data.get('Username'))
            password = tk.StringVar(value = data.get('Password'))
    except ValueError:
        print('Credentials not saved')
        username = tk.StringVar(value = '')
        password = tk.StringVar(value = '')
    except FileNotFoundError:
        print('File not found')
        username = tk.StringVar(value = '')
        password = tk.StringVar(value = '')

    frame1 = ttk.Frame(tabs, width = 400, height = 280)
    frame1.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'n')
    tabs.add(frame1, text = 'HTML')

    topframe = ttk.LabelFrame(frame1, text = "Login")
    topframe.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'new')

    sep = ttk.Separator(frame1, orient = 'horizontal')
    sep.grid(row = 1, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'nsew')

    botframe = ttk.LabelFrame(frame1, text = 'Report')
    botframe.grid(row = 2, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'new')

    user_lbl = tk.Label(topframe, text = "User Name:                      ")
    user_lbl.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'nw')
    user_entry = ttk.Entry(topframe, textvariable = username, width = 23, state = 'normal')
    user_entry.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = 'nw')

    pass_lbl = tk.Label(topframe, text = 'Password:')
    pass_lbl.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'nw')
    pass_entry = ttk.Entry(topframe, textvariable = password, width = 23, show = '*')
    pass_entry.grid(row = 1, column = 1, padx = 10, pady = 5, sticky = 'nw')

    html_location_dropdown = ttk.Combobox(
        botframe, 
        state = 'readonly', 
        values = ['All', 'Hospital', 'Clinics'],
        width = 20,
    )

    html_location_dropdown.current(0)
    html_location_dropdown.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = 'nw')
    location_label = tk.Label(botframe, text = 'Location:')
    location_label.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'nw')

    hsptl_entry = ttk.Entry(botframe, textvariable = html_hsptlValue, width = 23)
    hsptl_entry.grid(row = 1, column = 1, padx = 10, pady = 5, sticky = 'nw')
    hsptl_label = tk.Label(botframe, text = 'Hospital Value:                ')
    hsptl_label.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'nw')

    clnc_entry = ttk.Entry(botframe, textvariable = html_clncValue, width = 23)
    clnc_entry.grid(row = 2, column = 1, padx = 10, pady = 5, sticky = 'nw')
    clnc_label = tk.Label(botframe, text = 'Clinic Value:')
    clnc_label.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = 'nw')

    report_btn = ttk.Button(
        frame1,
        textvariable = htmlstatusVar,
        command = lambda:web.login(
            username.get(),
            password.get(),
            int(hsptl_entry.get()),
            int(clnc_entry.get()),
            html_location_dropdown.get(),
            useBlacklist.get()
        ),
        width = 15
    )
    report_btn.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'nw')

    blcklstCheck = tk.Checkbutton(frame1, text = "Use Blacklist", variable = useBlacklist, onvalue = True, offvalue = False)
    blcklstCheck.grid(row = 3, column = 1, padx = 10, pady = 5, sticky = 'nw')

    #save_btn = ttk.Button(topframe, text= 'Save', command = lambda:web.save(username.get(), password.get()), width = 15)
    #save_btn.grid(row = 2, column = 1, padx = 10, pady = 5, sticky = 'e')

    
    ## CSV Tab
    frame2 = ttk.Frame(tabs, width = 400, height = 280)
    frame2.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = 'n')
    tabs.add(frame2, text = "CSV")

    global fileVar, runBtn, outVar, statusVar, hsptlValue, clncValue, csvuseBlacklist

    fileVar = tk.StringVar(value = "No file selected")
    statusVar = tk.StringVar(value = "Ready")
    hsptlValue = tk.StringVar(value = '5')
    clncValue = tk.StringVar(value = '10')
    outVar = tk.StringVar(value = 'No destination selected')
    csvuseBlacklist = tk.BooleanVar()

    fileFrame = ttk.LabelFrame(frame2, text = "File")
    fileFrame['borderwidth'] = 2
    fileFrame['relief'] = 'groove'
    fileFrame.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'nwe')

    csv_sep = ttk.Separator(frame2, orient = 'horizontal')
    csv_sep.grid(row = 1, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'nsew')

    inputFrame = ttk.LabelFrame(frame2, text = "Settings")
    inputFrame['borderwidth'] = 2
    inputFrame['relief'] = 'groove'
    inputFrame.grid(row = 2, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'nwe')

    location_dropdown = ttk.Combobox(
        inputFrame,
        state = "readonly",
        values = ['All', 'Hospital', 'Clinics'],
        width = 20,
    )

    location_dropdown.current(0)
    location_dropdown.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = 'nw')

    location_label = tk.Label(inputFrame, text = "Location:")
    location_label.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'nw')

    hsptlValue_entry = ttk.Entry(inputFrame, textvariable = hsptlValue, width = 23)
    hsptlValue_entry.grid(row = 1, column = 1, padx = 10, pady = 5, sticky = 'nw')

    hsptlValue_label = tk.Label(inputFrame, text = "Hospital Value:                ")
    hsptlValue_label.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'nw')

    clncValue_entry = ttk.Entry(inputFrame, textvariable = clncValue, width = 23)
    clncValue_entry.grid(row = 2, column = 1, padx = 10, pady = 5, sticky = 'nw')

    clncValue_label = tk.Label(inputFrame, text = "Clinic Value:")
    clncValue_label.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = 'nw')

    file_label = tk.Label(fileFrame, text = 'File Selected:')
    file_label.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'nw')

    fileVarlabel = tk.Label(fileFrame, textvariable = fileVar, width = 23, anchor = 'w')
    fileVarlabel.grid(row = 3, column = 1, padx = 10, pady = 5, sticky = 'e')

    output_label = tk.Label(fileFrame, text = "Output Destination:")
    output_label.grid(row = 4, column = 0, padx = 10, pady = 5, sticky = 'e')

    destination_label = tk.Label(fileFrame, textvariable = outVar, width = 23, anchor = 'w')
    destination_label.grid(row = 4, column = 1, padx = 10, pady = 5, sticky = 'nw')
    
    openrunBtn = ttk.Button(
        frame2, 
        text = "Open and Run",
        width = 15,
        command = lambda:spreadsheet.open_file(
            location_dropdown.get(),
            int(hsptlValue_entry.get()),
            int(clncValue_entry.get()),
            csvuseBlacklist.get(),
            fileVar,
            outVar
        )
    )
    openrunBtn.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = 'w')

    csvblcklstCheck = tk.Checkbutton(frame2, text = "Use Blacklist", variable = csvuseBlacklist, onvalue = True, offvalue = False)
    csvblcklstCheck.grid(row = 5, column = 1, padx = 10, pady = 5, sticky = 'nw')

    #window.columnconfigure([0, 1], weight = 1)
    #root.rowconfigure([1, 0], weight = 1)

    ## Blacklist Tab
    frame3 = ttk.Frame(tabs, width = 400, height = 280)
    frame3.grid(row = 0, column = 2, padx = 10, pady = 5, sticky = 'n')
    tabs.add(frame3, text = "Blacklist")

    global blackVar
    
    try:
        os.chdir('C:/Users/Public')
        with open('printvision.json') as file:
            data = json.load(file)
            theList = data.get('Blacklist')
            blackVar = tk.StringVar(value = ', '.join(theList))
    except ValueError:
        # JSON is present but contents are empty
        print("Blacklist not saved.")
        blackVar = tk.StringVar(value = '')
    except FileNotFoundError:
        blackVar = tk.StringVar(value = '')
    except TypeError:
        # JSON is present but blacklist not present, json.load() returns None, which is not iterable
        print('Blacklist not saved')
        blackVar = tk.StringVar(value = '')

    editFrame = ttk.LabelFrame(frame3, text = 'Edit')
    editFrame.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'nw')
    blackEntry = ttk.Entry(editFrame, textvariable = blackVar, width = 48)
    blackEntry.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'nw')
    saveBtn = ttk.Button(editFrame, text = 'Save', width = 15, command = lambda:blacklist.saveList(blackVar.get()))
    saveBtn.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'nw')

    # editFrame = ttk.LabelFrame(frame3, text = "Edit")
    # editFrame.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'n')
    # blackText = ttk.Entry(editFrame, width = 48)
    # blackText.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 5, sticky = 'n')
    # addBtn = ttk.Button(editFrame, text = 'Add', width = 15, )
    # addBtn.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'nw')
    # removeBtn = ttk.Button(editFrame, text = 'Remove', width = 15, )
    # removeBtn.grid(row = 1, column = 1, padx = 10, pady = 5, sticky = 'nw')

    # listFrame = ttk.LabelFrame(frame3, text = 'List')
    # listFrame.grid(row = 1, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'nw')
    # listText = ttk.Label(listFrame, textvariable = blackVar, width = 25)
    # listText.grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 5, sticky = 'nw')
    # saveBtn = ttk.Button(listFrame, text = "Save", width = 15, )
    # saveBtn.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'nw')

    ## Info Tab
    frame4 = ttk.Frame(tabs, width = 400, height = 280)
    frame4.grid(row = 0, column = 4, padx = 10, pady = 5, sticky = 'n')
    tabs.add(frame4, text = 'Info')

    verLabel = tk.Label(frame4, text = f"Version {appVer}")
    verLabel.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'nw')

    copyLabel = tk.Label(frame4, text = "Copyright 2024 Ethan Wiens")
    copyLabel.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'nw')