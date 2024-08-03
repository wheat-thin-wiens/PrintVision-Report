import spreadsheet
import tkinter as tk
from tkinter import filedialog as fd, messagebox, ttk
import web

global credsPresent

try:
    import creds
    credsPresent = True
except ImportError:
    credsPresent = False
    pass

def create_gui(window):
# Tabbed UI
    tabs = ttk.Notebook(window)
    tabs.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'n')

    frame1 = ttk.Frame(tabs, width = 400, height = 280)
    frame2 = ttk.Frame(tabs, width = 400, height = 280)
    frame3 = ttk.Frame(tabs, width = 400, height = 280)
    frame1.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = 'n')
    frame2.grid(row = 0, column = 2, padx = 10, pady = 5, sticky = 'n')
    frame3.grid(row = 0, column = 3, padx = 10, pady = 5, sticky = 'n')
    tabs.add(frame1, text = "CSV")
    tabs.add(frame2, text = "Configure")
    tabs.add(frame3, text = 'Info')
    
    ## HTML Tab
    global username, password, htmlstatusVar, html_hsptlValue, html_clncValue, html_location_dropdown

    htmlstatusVar = tk.StringVar(value = "Run Report")
    html_hsptlValue = tk.StringVar(value = '5')
    html_clncValue = tk.StringVar(value = '10')
    
    if credsPresent:
        username = tk.StringVar(value = creds.username)
        password = tk.StringVar(value = creds.password)
    else:
        username = tk.StringVar(value = '')
        password = tk.StringVar(value = '')

    frame4 = ttk.Frame(tabs, width = 400, height = 280)
    frame4.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'n')
    tabs.add(frame4, text = 'HTML')

    topframe = ttk.LabelFrame(frame4, text = "Login")
    topframe.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'new')

    sep = ttk.Separator(frame4, orient = 'horizontal')
    sep.grid(row = 1, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'nsew')

    botframe = ttk.LabelFrame(frame4, text = 'Report')
    botframe.grid(row = 2, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'new')

    user_lbl = tk.Label(topframe, text = "User Name:     ")
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
    hsptl_label = tk.Label(botframe, text = 'Hospital Value:')
    hsptl_label.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'nw')

    clnc_entry = ttk.Entry(botframe, textvariable = html_clncValue, width = 23)
    clnc_entry.grid(row = 2, column = 1, padx = 10, pady = 5, sticky = 'nw')
    clnc_label = tk.Label(botframe, text = 'Clinic Value:')
    clnc_label.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = 'nw')

    report_btn = ttk.Button(frame4, textvariable = htmlstatusVar, command = lambda:web.login(self.username, self.password,  html_location_dropdown.get), width = 17)
    report_btn.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'nw')
    
    ## CSV Tab
    global fileVar, runBtn, outVar, statusVar, hsptlValue, clncValue

    fileVar = tk.StringVar(value = "No file selected")
    statusVar = tk.StringVar(value = "Ready")
    hsptlValue = tk.StringVar(value = '5')
    clncValue = tk.StringVar(value = '10')
    outVar = tk.StringVar(value = 'No destination selected')

    openBtn = ttk.Button(frame1, text = "Open File", width = 15, command = spreadsheet.open_file)
    openBtn.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = 'se')

    runBtn = ttk.Button(frame1, text = "Run", state = 'disabled', width = 15, command = lambda:spreadsheet.run_report(location_dropdown.get()))
    runBtn.grid(row = 5, column = 1, padx = 10, pady = 5, sticky = 'se')

    inputFrame = ttk.LabelFrame(frame1, text = "Report Settings")
    inputFrame['borderwidth'] = 2
    inputFrame['relief'] = 'groove'
    inputFrame.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'nwe')

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

    hsptlValue_label = tk.Label(inputFrame, text = "Hospital Value:")
    hsptlValue_label.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'nw')

    clncValue_entry = ttk.Entry(inputFrame, textvariable = clncValue, width = 23)
    clncValue_entry.grid(row = 2, column = 1, padx = 10, pady = 5, sticky = 'nw')

    clncValue_label = tk.Label(inputFrame, text = "Clinic Value:")
    clncValue_label.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = 'nw')

    file_label = tk.Label(inputFrame, text = 'File Selected:')
    file_label.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'nw')

    fileVarlabel = tk.Label(inputFrame, textvariable = fileVar, width = 23, anchor = 'w')
    fileVarlabel.grid(row = 3, column = 1, padx = 10, pady = 5, sticky = 'nw')

    output_label = tk.Label(inputFrame, text = "Output Destination:")
    output_label.grid(row = 4, column = 0, padx = 10, pady = 5, sticky = 'nw')

    destination_label = tk.Label(inputFrame, textvariable = outVar, width = 23, anchor = 'w')
    destination_label.grid(row = 4, column = 1, padx = 10, pady = 5, sticky = 'nw')

    window.columnconfigure([0, 1], weight = 1)
    #root.rowconfigure([1, 0], weight = 1)
