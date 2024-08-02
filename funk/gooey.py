import spreadsheet
import tkinter as tk
from tkinter import filedialog as fd, messagebox, ttk
import web

class Gooey:
    def __init__(self, window, username, password):
        self.window = window
        self.username = username
        self.password = password
    
    def create_gui(self):
    # Tabbed UI
        tabs = ttk.Notebook(self.window)
        tabs.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'n')

        frame1 = ttk.Frame(tabs, width = 400, height = 280)
        frame2 = ttk.Frame(tabs, width = 400, height = 280)
        frame3 = ttk.Frame(tabs, width = 400, height = 280)
        frame4 = ttk.Frame(tabs, width = 400, height = 280)
        frame4.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'n')
        frame1.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = 'n')
        frame2.grid(row = 0, column = 2, padx = 10, pady = 5, sticky = 'n')
        frame3.grid(row = 0, column = 3, padx = 10, pady = 5, sticky = 'n')
        tabs.add(frame4, text = 'HTML')
        tabs.add(frame1, text = "CSV")
        tabs.add(frame2, text = "Configure")
        tabs.add(frame3, text = 'Info')
        
        ## HTML Tab
        global username, password, htmlstatusVar, html_hsptlValue, html_clncValue, html_location_dropdown

        htmlstatusVar = tk.StringVar(value = "Run Report")
        html_hsptlValue = tk.StringVar(value = '5')
        html_clncValue = tk.StringVar(value = '10')

        username = tk.StringVar(value = self.username)
        password = tk.StringVar(value = self.password)

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

        ## Config Tab
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

        dumbass_check = tk.Checkbutton(frame2, text = "I know what I'm doing", variable = btnchck, onvalue = 1, offvalue = 0, command = spreadsheet.notadumbass)
        dumbass_check.grid(row = 8, column = 0, padx = 10, pady = 5, sticky = 'nw')

        # Info Tab
        info_text = tk.Label(frame3, text = 'Intended for use with PrintVision toner reports.')
        info_text.grid(row = 0, column = 0)
        copyright = tk.Label(frame3, text = '© 2024 - Ethan Wiens - All Rights Reserved', anchor = 'w')
        copyright.grid(row = 1, column = 0)

        self.window.columnconfigure([0, 1], weight = 1)
        #root.rowconfigure([1, 0], weight = 1)