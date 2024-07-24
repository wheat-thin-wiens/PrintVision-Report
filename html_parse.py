from bs4 import BeautifulSoup
import creds
import csv
import html
import lxml
import os
from playwright.sync_api import sync_playwright, expect
import requests
import time
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk

root = tk.Tk()
root.geometry("390x239")
root.title("PrintVision Report (HTML)")

def login():
    global pv_base

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

        page.goto(report_url)
        dropdown = 'id=ContentPlaceHolder1_runParameters_groupList_button'
        dropdown_btn = 'id=ContentPlaceHolder1_runParameters_groupList_button'
        page.get_by_role("img", name="@").click()
        page.get_by_role("link", name="HCMC (1373)").click()
        page.click('#run')
        page.wait_for_selector('.pfReport')
        report = page.inner_html('#content')
        soup = BeautifulSoup(report, 'lxml')
        
    html_report(soup)
    
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

    runBtn.config(state = 'normal')

def html_report(soup):
    os.chdir('C:/Users/Public')

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

        body = soup.find('tbody')
        for x in body.find_all('tr'):
            rows = x.find_all('td')
            printer = []
            dick = {}
            for y in rows:
                beep = y.text.strip('\n')
                beep = beep.strip('\xa0\n')
                printer.append(beep)
            spamwriter.writerow(printer)
            for a, b in zip(columns, printer):
                if len(b) == 0:
                    pass
                else:
                    dick.update({a: b})
        print(dick)

def create_gui():
    global hsptlValue, clncValue, statusVar, runBtn

    statusVar = tk.StringVar(value = "Ready")
    hsptlValue = tk.StringVar(value = '5')
    clncValue = tk.StringVar(value = '10')

    global username, password

    username = tk.StringVar(value = creds.username)
    password = tk.StringVar(value = creds.password)

    #frame1 = ttk.Frame(root)
    #frame1['borderwidth'] = 2
    #frame1['relief'] = 'groove'
    #frame1.grid(row = 0, column = 0, columnspan = 3, padx = 5, pady = 5, sticky = 'nsew')
    #frame1.columnconfigure([0, 1], weight = 1)

    frame1 = ttk.LabelFrame(root, text = "Login")
    frame1.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'new')

    #frame2 = tk.Frame(root)
    #frame2['borderwidth'] = 2
    #frame2['relief'] = 'groove'
    #frame2.grid(row = 2, column = 0, columnspan = 3, padx = 5, pady = 5, sticky = 'nsew')

    frame2 = ttk.LabelFrame(root, text = 'Report')
    frame2.grid(row = 2, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'new')

    sep = ttk.Separator(root, orient = 'horizontal')
    sep.grid(row = 1, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'nsew')

    user_lbl = tk.Label(frame1, text = "User Name:     ")
    user_lbl.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'nw')
    user_entry = ttk.Entry(frame1, textvariable = username, width = 23, state = 'normal')
    user_entry.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = 'nw')

    pass_lbl = tk.Label(frame1, text = 'Password:')
    pass_lbl.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'nw')
    pass_entry = ttk.Entry(frame1, textvariable = password, width = 23, show = '*')
    pass_entry.grid(row = 1, column = 1, padx = 10, pady = 5, sticky = 'nw')

    login_btn = ttk.Button(frame1, text = 'Login', command = login)
    login_btn.grid(row = 1, column = 3, padx = 10, pady = 5, sticky = 'e')

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

    runBtn = ttk.Button(frame2, text = "Run", state = 'disabled',)# command = lambda:run_report(location_dropdown.get()))
    runBtn.grid(row = 2, column = 3, padx = 10, pady = 5, sticky = 'se')

    #root.columnconfigure([0, 1], weight = 1, uniform = 'key')

if __name__ == '__main__':
    create_gui()
    root.mainloop()


