from bs4 import BeautifulSoup
import creds
import csv
import html
import lxml
import os
from playwright.sync_api import sync_playwright
import tkinter as tk
from tkinter import filedialog as fd, ttk, messagebox

root = tk.Tk()
root.geometry("295x265")
root.title("HTML")

def login():
    global pv_base
    statusVar.set('Logging in...')

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

        statusVar.set('Collecting report...')
        page.goto(report_url)
        dropdown = 'id=ContentPlaceHolder1_runParameters_groupList_button'
        dropdown_btn = 'id=ContentPlaceHolder1_runParameters_groupList_button'
        page.get_by_role("img", name="@").click()
        page.get_by_role("link", name="HCMC (1373)").click()
        page.click('#run')
        page.wait_for_selector('.pfReport')
        report = page.inner_html('#content')
        soup = BeautifulSoup(report, 'lxml')
        
    begin_report(soup)
    
    #payload = {
    #    'txtUserName' : user,
    #    'txtPassword' : passw
    #}

    #with requests.session() as s:
    #    s.post(pv_login, data = payload)
    #    r = s.get(report_url)
    #    soup = BeautifulSoup(r.content, 'html.parser')
    #    print(soup.prettify())
    
    #soup = BeautifulSoup(response.content, 'html.parser')
    #protected_content = soup.find()

    #page = requests.get(url)
    #print(page.status_code)

def begin_report(soup):
    statusVar.set('Analyzing report...')
    global hValue, cValue
    hValue = int(hsptlValue.get())
    cValue = int(clncValue.get())
    location = location_dropdown.get()

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
                printer = []
                list = []
                for y in rows:
                    beep = y.text.strip('\n')
                    beep = beep.strip('\xa0\n')
                    boop = beep.split('\n')
                    list.append(boop[0])
                print(list)
                
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

    outLocation = fd.askdirectory(
            title = "Save new report",
            initialdir = "/"
        )

    if len(outLocation) > 0:
        os.replace('C:/Users/Public/report.csv', f"{outLocation}/report.csv")
    else:
        os.remove("C:/Users/Public/report.csv")

    view = messagebox.askyesno("Report Complete", "Would you like to view the report?")
    if view:
        os.system(f"start excel.exe {outLocation}/report.csv")

    statusVar.set('Report complete.')

def create_gui():
    global hsptlValue, clncValue, statusVar, runBtn, location_dropdown

    statusVar = tk.StringVar(value = "Run Report")
    hsptlValue = tk.StringVar(value = '5')
    clncValue = tk.StringVar(value = '10')

    global username, password

    username = tk.StringVar(value = creds.username)
    password = tk.StringVar(value = creds.password)

    frame1 = ttk.LabelFrame(root, text = "Login")
    frame1.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'new')

    sep = ttk.Separator(root, orient = 'horizontal')
    sep.grid(row = 1, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'nsew')

    frame2 = ttk.LabelFrame(root, text = 'Report')
    frame2.grid(row = 2, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'new')

    user_lbl = tk.Label(frame1, text = "User Name:     ")
    user_lbl.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'nw')
    user_entry = ttk.Entry(frame1, textvariable = username, width = 23, state = 'normal')
    user_entry.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = 'nw')

    pass_lbl = tk.Label(frame1, text = 'Password:')
    pass_lbl.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'nw')
    pass_entry = ttk.Entry(frame1, textvariable = password, width = 23, show = '*')
    pass_entry.grid(row = 1, column = 1, padx = 10, pady = 5, sticky = 'nw')

    #login_btn = ttk.Button(frame1, text = 'Login', command = login)
    #login_btn.grid(row = 1, column = 3, padx = 10, pady = 5, sticky = 'e')

    location_dropdown = ttk.Combobox(
        frame2, 
        state = 'readonly', 
        values = ['All', 'Hospital', 'Clinics'],
        width = 20,
    )
    location_dropdown.current(0)
    location_dropdown.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = 'nw')
    location_label = tk.Label(frame2, text = 'Location:')
    location_label.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'nw')

    hsptl_entry = ttk.Entry(frame2, textvariable = hsptlValue, width = 23)
    hsptl_entry.grid(row = 1, column = 1, padx = 10, pady = 5, sticky = 'nw')
    hsptl_label = tk.Label(frame2, text = 'Hospital Value:')
    hsptl_label.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'nw')

    clnc_entry = ttk.Entry(frame2, textvariable = clncValue, width = 23)
    clnc_entry.grid(row = 2, column = 1, padx = 10, pady = 5, sticky = 'nw')
    clnc_label = tk.Label(frame2, text = 'Clinic Value:')
    clnc_label.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = 'nw')

    #root.columnconfigure([0, 1], weight = 1, uniform = 'key')

    #status_label = tk.Label(root, textvariable = statusVar)
    #status_label.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'nw')

    report_btn = ttk.Button(root, textvariable = statusVar, command = login, width = 17)
    report_btn.grid(row = 3, column = 0, padx = 10, pady = 5, sticky = 'nw')

if __name__ == '__main__':
    create_gui()
    root.mainloop()
