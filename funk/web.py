from bs4 import BeautifulSoup
from . import blacklist, readwriteJSON
import csv
import os, os.path
import platform
from playwright.sync_api import sync_playwright
import re
from tkinter import filedialog as fd, messagebox

global ope
ope = platform.system()

def login(username, password, hValue: int, cValue: int, location, blist):
    pv_login = 'https://loffler.printfleet.com/login.aspx'
    report_url = 'https://loffler.printfleet.com/reportDetail.aspx?reportId=0afcca2e-f240-4ac3-ae81-438da7176e99'

    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True, slow_mo=0)
        page = browser.new_page()

        page.goto(pv_login)
        page.fill('input#txtUserName', username)
        page.fill('input#txtPassword', password)
        page.click('input#cmdLogin')

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
                devicecount = result.string.strip('()')
                print(f'Found device count: {devicecount}')
                break
            else:
                # print('still looking')
                continue

        page.get_by_role("img", name="@").click()
        page.get_by_role("link", name = f"HCMC ({devicecount})").click()
        page.click('#run')
        page.wait_for_selector('.pfReport')
        report = page.inner_html('#content')
        soup = BeautifulSoup(report, 'html.parser')

    readwriteJSON.writeJSON({'Username': username})
    readwriteJSON.writeJSON({'Password': password})
    which_html(soup, hValue, cValue, location, blist)

def which_html(soup, hValue, cValue, location, blist):

    if location == 'All':
        html_report(soup, hValue, cValue, ['10.200', '10.205', '10.210'], blist)
    elif location == 'Hospital':
        html_report(soup, hValue, cValue, ['10.200', '10.205'], blist)
    elif location == 'Clinic':
        html_report(soup, hValue, cValue, ['10.210'], blist)

def html_report(soup, hValue, cValue, IP_list, blist):
    if ope == 'Windows':
        os.chdir('C:/Users/Public')
    elif ope == 'Darwin':
        os.chdir('/Users/ethanwiens/Downloads')
    
    if os.path.isfile('report.csv'):
        os.remove('report.csv')
        open('report.csv', 'x')
        print('File created')

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
        row_count = 0

        body = soup.find('tbody')
        for ip in IP_list:
            for x in body.find_all('tr'):
                rows = x.find_all('td')
                list = []
                for y in rows:
                    beep = y.text.strip('\n')
                    beep = beep.strip('\xa0\n')
                    boop = beep.split('\n')
                    list.append(boop[0])
                
                if ip in list[2]:
                    toners = []

                    if ip =='10.210':
                        black = htmlToner(list[6], cValue, toners)
                        cyan = htmlToner(list[7], cValue, toners)
                        magenta = htmlToner(list[8], cValue, toners)
                        yellow = htmlToner(list[9], cValue, toners)
                    else:
                        black = htmlToner(list[6], hValue, toners)
                        cyan = htmlToner(list[7], hValue, toners)
                        magenta = htmlToner(list[8], hValue, toners)
                        yellow = htmlToner(list[9], hValue, toners)

                    if len(toners) > 0:
                        if blist:
                            checkedLine = blacklist.checkBlacklist(list)
                            if len(checkedLine) > 1:
                                row_count += 1
                                # print(f'\rRows Added: ({row_count})', end = '')
                                spamwriter.writerow(checkedLine)
                            else:
                                continue
                        elif not blist:
                            row_count += 1
                            # print(f'\rRows Added: ({row_count})', end = '')
                            spamwriter.writerow(list)
                
                else:
                    continue

    print(f'Rows Added: {row_count}')

    saved = False
    while not saved:
        try:
            outLocation = fd.askdirectory(
            title = "Save new report",
            initialdir = "/"
        )
            
            if len(outLocation) > 0:
                if ope == "Windows":
                    os.replace('C:/Users/Public/report.csv', f"{outLocation}/report.csv")
                elif ope == "Darwin":
                    os.replace('/Users/ethanwiens/Downloads/report.csv', f"{outLocation}/report.csv") # type: ignore
            else:
                os.remove("C:/Users/Public/report.csv")
            saved = True
        except PermissionError:
            messagebox.showwarning("Unable to save", "If a previous report is still open, make sure you close it before running another report.")
            continue
    
    view = messagebox.askyesno("Report Complete", "Would you like to view the report?")
    if view:
        os.system(f"start excel.exe {outLocation}/report.csv") # type: ignore

def htmlToner(toner: str, value: int, tonerList: list):
    try:    
        toner = toner.strip("%")

        if int(toner) <= value:
            tonerList.append(toner)
            return f"{toner}%"
        else:
            return ''

    except ValueError:
        return
    except TypeError:
        return
