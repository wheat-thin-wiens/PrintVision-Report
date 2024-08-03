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


def pdf_report(file, IP, hValue, cValue):
    return
