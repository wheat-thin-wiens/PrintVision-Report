# PrintVision Report Parser by Ethan Wiens
from bs4 import BeautifulSoup
import csv
import funk
import os, os.path
from playwright.sync_api import sync_playwright
import re
import tkinter as tk
from tkinter import filedialog as fd, messagebox, ttk

global credsPresent

try:
    import funk.creds
    credsPresent = True
except ImportError:
    credPresent = False
    pass

root = tk.Tk()
root.geometry("365x325")
root.title("PrintVision Report")
#root.iconbitmap('printing.ico')

## HTML Functions
def login():
    htmlstatusVar.set('Logging in...')

    pv_login = 'https://loffler.printfleet.com/login.aspx'
    report_url = 'https://loffler.printfleet.com/reportDetail.aspx?reportId=0afcca2e-f240-4ac3-ae81-438da7176e99'
    user = username.get()
    passw = password.get()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True, slow_mo=0)
        page = browser.new_page()
        page.goto(pv_login)
        page.fill('input#txtUserName', user)
        page.fill('input#txtPassword', passw)
        page.click('input#cmdLogin')

        htmlstatusVar.set('Collecting report...')
        page.goto(report_url)

        report_page = page.inner_html('#content')
        soup = BeautifulSoup(report_page, 'html.parser')
        all_spans = soup.find_all('span')
        list_spans = []
        devicecount = ''

        for x in all_spans:
            list_spans.append(x.text)

        for x in list_spans:
            num = re.compile(r"([\d]{4})")
            result = num.search(x)
            if result:
                print(f'found device count: {result.string.strip('()')}')
                devicecount = result.string.strip('()')
                break
            else:
                print('still looking')
                continue

        page.get_by_role("img", name="@").click()
        page.get_by_role("link", name = f"HCMC ({devicecount})").click()
        page.click('#run')
        page.wait_for_selector('.pfReport')
        report = page.inner_html('#content')
        soup = BeautifulSoup(report, 'html.parser')
        
    begin_report(soup)

def begin_report(soup):
    htmlstatusVar.set('Analyzing report...')
    global hValue, cValue
    hValue = int(html_hsptlValue.get())
    cValue = int(html_clncValue.get())
    location = html_location_dropdown.get()

    if location == 'All':
        html_report(soup, ['10.200', '10.205', '10.210'])
    elif location == 'Hospital':
        html_report(soup, ['10.200', '10.205'])
    elif location == 'Clinic':
        html_report(soup, ['10.210'])

def html_report(soup, IP_list):
    os.chdir('C:/Users/Public')
    #os.chdir('/Users/ethanwiens/Downloads')
    
    if os.path.isfile('report.csv'):
        os.remove('report.csv')
        open('report.csv', 'x')
        print('file created')

    with open('report.csv', 'a', newline = '') as csvfile:
        spamwriter = csv.writer(
            csvfile,
            delimiter = ',',
            quotechar = '|',
            quoting = csv.QUOTE_MINIMAL,
        )

        columns = []
        head = soup.find('thead')
        for x in head.find_all('th'):
            columns.append(x.text)
        spamwriter.writerow(columns)

        #tbody is the table containing the entire report
        body = soup.find('tbody')
        for ip in IP_list:
            #tr is each row in the report, effectively each printer
            for x in body.find_all('tr'):
                #td is each piece of data, or column, for an individual printer
                rows = x.find_all('td')
                list = []
                for y in rows:
                    beep = y.text.strip('\n')
                    beep = beep.strip('\xa0\n')
                    boop = beep.split('\n')
                    list.append(boop[0])
                
                crnt_ip = list[2]
                
                if ip in list[2]:
                    toners = []
                    try:
                        black = list[6].strip('%')
                        cyan = list[7].strip('%')
                        magenta = list[8].strip('%')
                        yellow = list[9].strip('%')
                        if ip == '10.210':
                            if int(black) <= cValue:
                                toners.append(black)
                            elif int(black) > cValue:
                                list[6] = ' '
                            if int(cyan) <= cValue:
                                toners.append(cyan)
                            elif int(cyan) > cValue:
                                list[7] = ' '
                            if int(magenta) <= cValue:
                                toners.append(magenta)
                            elif int(magenta) > cValue:
                                list[8] = ' '
                            if int(yellow) <= cValue:
                                toners.append(yellow)
                            elif int(yellow) > cValue:
                                list[9] = ' '
                        else:
                            if int(black) <= hValue:
                                toners.append(black)
                            elif int(black) > hValue:
                                list[6] = ' '
                            if int(cyan) <= hValue:
                                toners.append(cyan)
                            elif int(cyan) > hValue:
                                list[7] = ' '
                            if int(magenta) <= hValue:
                                toners.append(magenta)
                            elif int(magenta) > hValue:
                                list[8] = ' '
                            if int(yellow) <= hValue:
                                toners.append(yellow)
                            elif int(yellow) > hValue:
                                list[9] = ' '
                    except TypeError:
                        pass
                    except ValueError:
                        pass

                    if len(toners) > 0:
                        spamwriter.writerow(list)
                        print('row added')
                
                else:
                    continue

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

    htmlstatusVar.set('Report complete.')

def create_gui():
    # Tabbed UI
    tabs = ttk.Notebook(root)
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

    if credsPresent:
        username = tk.StringVar(value = funk.creds.username)
        password = tk.StringVar(value = funk.creds.password)
    else:
        username = tk.StringVar(value = '')
        password = tk.StringVar(value = '')

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

    report_btn = ttk.Button(frame4, textvariable = htmlstatusVar, command = login, width = 17)
    report_btn.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'nw')
    
    ## CSV Tab
    global fileVar, runBtn, outVar, statusVar, hsptlValue, clncValue

    fileVar = tk.StringVar(value = "No file selected")
    statusVar = tk.StringVar(value = "Ready")
    hsptlValue = tk.StringVar(value = '5')
    clncValue = tk.StringVar(value = '10')
    outVar = tk.StringVar(value = 'No destination selected')

    openBtn = ttk.Button(frame1, text = "Open File", width = 15, command = open_file)
    openBtn.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = 'se')

    runBtn = ttk.Button(frame1, text = "Run", state = 'disabled', width = 15, command = lambda:run_report(location_dropdown.get()))
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

## Running the Program
if __name__ == '__main__':
    funk.create_gui(root)
    root.mainloop()
