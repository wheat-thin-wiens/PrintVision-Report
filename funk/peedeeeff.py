import csv
import os, os.path
from pypdf import PdfReader
from tkinter import filedialog as fd

def open_pdf(location, hValue, cValue):
    file_chosen = False

    while not file_chosen:
        file = fd.askopenfilename(
            title = "open file",
            initialdir = '/',
            filetypes = (
                ('PDF Files', '*.pdf'),
                #('All Files', '*.*'),
            )
        )

        if len(file) > 0:
            file_chosen = True
            which_pdf(file, location, hValue, cValue)
        else:
            continue

def which_pdf(file, location, hValue, cValue):
    reader = PdfReader(file)
    num_pages = len(reader.pages)
    
    for x in range(0, num_pages):
        page = reader.pages[x]
        page.rotate(270)
        content = page.extract_text()
        print(content)

def pdf_report(file, IP, hValue, cValue):
    return


#open_pdf('All', 5, 10)