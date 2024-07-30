# PrintVision Report Parser by Ethan Wiens
from bs4 import BeautifulSoup
import csv
import os, os.path
from playwright.sync_api import sync_playwright
#from selenium import webdriver
#from selenium.webdriver.chrome.service import Service as ChromeService
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.support.ui import WebDriverWait, Select
import time
import tkinter as tk
from tkinter import filedialog as fd, messagebox, ttk
#from webdriver_manager.chrome import ChromeDriverManager

global credsPresent

try:
    import creds
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
        browser = p.chromium.launch(headless = True, )
        page = browser.new_page()
        page.goto(pv_login)
        page.fill('input#txtUserName', user)
        page.fill('input#txtPassword', passw)
        page.click('input#cmdLogin')

        htmlstatusVar.set('Collecting report...')
        page.goto(report_url)
        page.get_by_role("img", name="@").click()
        page.get_by_role("link", name="HCMC (1373)").click()
        page.click('#run')
        page.wait_for_selector('.pfReport')
        report = page.inner_html('#content')
        soup = BeautifulSoup(report, 'lxml')
        
    begin_report(soup)

# def logincel():
#     #htmlstatusVar.set('Logging in...')

#     pv_login = 'https://loffler.printfleet.com/login.aspx'
#     report_url = 'https://loffler.printfleet.com/reportDetail.aspx?reportId=0afcca2e-f240-4ac3-ae81-438da7176e99'
#     user = username.get()
#     passw = password.get()

#     #driver = webdriver.Chrome(service = ChromeService(ChromeDriverManager().install()))
#     driver = webdriver.Chrome()
#     actions = ActionChains(driver)
    
#     driver.get(pv_login)
#     driver.find_element(by = By.XPATH, value = '//*[@id="txtUserName"]').send_keys(user)
#     driver.find_element(by = By.XPATH, value = '//*[@id="txtPassword"]').send_keys(passw)
#     driver.find_element(by = By.NAME, value = 'cmdLogin').send_keys(Keys.RETURN)
    
#     wait = WebDriverWait(driver, 10)
#     wait.until(EC.url_matches(('https://loffler.printfleet.com/mast_home.aspx')))
#     report_link = driver.find_element(by = By.LINK_TEXT, value = 'Reports')
#     #report_link = driver.find_element(by = By.XPATH, value = '//*[@id="pagecontent"]/div/ul/li[3]/a')
#     actions.click(report_link)
#     actions.perform()

#     wait.until(EC.url_matches(('https://loffler.printfleet.com/reportList.aspx')))
#     drpdwn = Select(driver.find_element(by = By.CSS_SELECTOR, value = '#ContentPlaceHolder1_uiReportList > div > div.pDiv > div.pDiv2 > div:nth-child(1) > select'))
#     drpdwn.select_by_value('200')
#     refresh = driver.find_element(by = By.CSS_SELECTOR, value = '#ContentPlaceHolder1_uiReportList > div > div.pDiv > div.pDiv2 > div:nth-child(9) > div')
#     actions.click(refresh)
#     actions.perform()
#     wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Toner Low Report (10%)")))
#     report_link = driver.find_element(by = By.LINK_TEXT, value = "Toner Low Report (10%)")
#     actions.click(report_link)
#     actions.perform()
    
#     wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ContentPlaceHolder1_runParameters_groupList_button')))
#     print('butts')
#     drpdwn = driver.find_element(by = By.XPATH, value = '//img[@alt="@"]')
#     #drpdwn = driver.find_element(by = By.CSS_SELECTOR, value = '#ContentPlaceHolder1_runParameters_groupList_button')
#     actions.click(drpdwn)
#     actions.perform()
#     #devices = '//*[@id="ContentPlaceHolder1_runParameters_groupList_uiTree-02dcbb93-6c2d-43dc-83ab-382f0c9878a2"]/a'
#     devices = driver.find_element(by = By.LINK_TEXT, value = "HCMC (1373)")
#     actions.click(devices)
#     actions.perform()
#     run = driver.find_element(by = By.XPATH, value = '//*[@id="run"]')
#     actions.click(run)
#     actions.perform()

#     wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="rd063"]/h1')))
#     print('more butts')
    #driver.find_element(by = By.XPATH, value = '//*[@id="ContentPlaceHolder1_runParameters_groupList_button"]')
    #driver.find_element(by = By.LINK_TEXT, value = "HCMC (1373)").click
    #driver.find_element(by = By.XPATH, value = '//*[@id="run"]').click
    

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

## CSV Functions
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

    hValue = int(html_hsptlValue.get())
    cValue = int(html_clncValue.get())

    if location == 'Hospital':
        report('Main Campus', '10.200', hValue)
        report('Main Campus', '10.205', hValue)
    elif location == 'Clinic':
        report('Clinic', '10.210', cValue)
    elif location == 'All':
        report('Main Campus', '10.200', hValue)
        report('Main Campus', '10.205', hValue)
        report('Clinic', '10.210', cValue)

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
    frame4 = ttk.Frame(tabs, width = 400, height = 280)
    frame4.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'n')
    frame1.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = 'n')
    frame2.grid(row = 0, column = 2, padx = 10, pady = 5, sticky = 'n')
    frame3.grid(row = 0, column = 3, padx = 10, pady = 5, sticky = 'n')
    tabs.add(frame4, text = 'HTML')
    tabs.add(frame1, text = "CSV")
    tabs.add(frame2, text = "Configure")
    tabs.add(frame3, text = 'Info')

    #canvas = tk.Canvas(frame2, width = 400, height = 280)
    #canvas.grid(row = 0, column = 0)
    #scrollbar = ttk.Scrollbar(frame2, orient = 'vertical', command = canvas.yview)
    #scrollbar.grid(row = 0, column = 2, rowspan = 10, sticky = 'e')
    #canvas.config(yscrollcommand=scrollbar.set, scrollregion=(0,0,100,100))
    #frame = tk.Frame(canvas, bg='white', width=200, height=100)
    #canvas.create_window(100, 500, window=frame)
    
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
    global fileVar, runBtn, outVar, statusVar

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
    output_label.grid(row = 4, column = 0, padx = 10, pady = 10, sticky = 'nw')

    destination_label = tk.Label(inputFrame, textvariable = outVar, width = 23, anchor = 'w')
    destination_label.grid(row = 4, column = 1, padx = 10, pady = 10, sticky = 'nw')

    #stsLabel = tk.Label(frame1, textvariable = statusVar, anchor = 'e')
    #stsLabel.grid(row = 5, column = 2, padx = 10, pady = 10, sticky = 'nw')

    #dumbbutton = tk.Button(root, text = 'dumb', command = printy)
    #dumbbutton.grid(row = 4, column = 1, padx = 10, pady = 5, sticky = 'nw')

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
