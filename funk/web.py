import asyncio
from bs4 import BeautifulSoup
from . import blacklist, readwriteJSON, gooey, files
from playwright.async_api import async_playwright
import re

async def login(username, password, hValue: int, cValue: int, location, blist):
    pv_login = 'https://loffler.printfleet.com/login.aspx'
    report_url = 'https://loffler.printfleet.com/reportDetail.aspx?reportId=0afcca2e-f240-4ac3-ae81-438da7176e99'

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless = True, slow_mo = 0)
        page = await browser.new_page()

        await page.goto(pv_login)
        await page.fill('input#txtUserName', username)
        await page.fill('input#txtPassword', password)
        await page.click('input#cmdLogin')

        if await page.get_by_text("Invalid email address and/or password").is_visible():
            await browser.close()
            gooey.loginError()
            return

        await page.goto(report_url)
        report_page = await page.inner_html('#content')
        soup = BeautifulSoup(report_page, 'html.parser')
        all_spans = soup.find_all('span')
        
        list_spans = [x.text for x in all_spans]

        for x in list_spans:
            num = re.compile(r"([\d]{4})")
            result = num.search(x)
            if result:
                devicecount = result.string.strip('()')
                print(f'Found device count: {devicecount}')
                break
            else:
                continue

        await page.get_by_role("img", name="@").click()
        await page.get_by_role("link", name = f"HCMC ({devicecount})").click()
        await page.click('#run')
        await page.wait_for_selector('.pfReport')
        report = await page.inner_html('#content')
        soup = BeautifulSoup(report, 'html.parser')

    readwriteJSON.writeJSON({'Username': username})
    readwriteJSON.writeJSON({'Password': password})
    await which_html(soup, hValue, cValue, location, blist)

async def which_html(soup, hValue, cValue, location, blist):
    initDir = files.createFile()

    head = soup.find('thead')
    header = [x.text for x in head.find_all('th')]
    files.writeLine(header)

    match location:
        case "All":
            await html_report(soup, hValue, "10.200", blist)
            await html_report(soup, hValue, "10.205", blist)
            await html_report(soup, cValue, "10.210", blist)
        case "Hospital":
            await html_report(soup, hValue, "10.200", blist)
            await html_report(soup, hValue, "10.205", blist)
        case "Clinic":
            await html_report(soup, cValue, "10.210", blist)

    gooey.saveDialog(initDir)

async def html_report(soup, value, IP, blist):
    row_count = 0
    body = soup.find('tbody')
    table = body.find_all("tr")

    for x in table:
        rows = x.find_all('td')

        line = [y.text.strip('\n').strip('\xa0\n') for y in rows]
        toners = []

        ip = line[2]
        black = line[6]
        cyan = line[7]
        magenta = line[8]
        yellow = line[9]

        if IP in ip:
            line[6] = htmlToner(black, value, toners)
            line[7] = htmlToner(cyan, value, toners)
            line[8] = htmlToner(magenta, value, toners)
            line[9] = htmlToner(yellow, value, toners)
        else:
            continue
        
        if len(toners) > 0:
            if blist:
                checkedLine = blacklist.checkBlacklist(line)
                if len(checkedLine) > 1:
                    row_count += 1
                    files.writeLine(checkedLine)
                else:
                    continue
            elif not blist:
                row_count += 1
                files.writeLine(line)

    match IP:
        case "10.200":
            print(f"Hospital: {row_count}")
        case "10.205":
            print(f"CSC: {row_count}")
        case "10.210":
            print(f"Clinics: {row_count}")

def htmlToner(toner: str, value: int, tonerList: list):
    try:    
        toner = toner.strip("%")

        if int(toner) <= value:
            tonerList.append(toner)
            return f"{toner}%"
        else:
            return ' '

    except ValueError:
        return ' '
    except TypeError:
        return ' '
    