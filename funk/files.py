import asyncio
import csv
import os, os.path
import platform

global ope
ope = platform.system()

def createFile() -> str:
    match ope:
        case "Windows":
            initDir = "C:/Users/Public"
            os.chdir(initDir)
        case "Darwin":
            initDir = "/Users/ethanwiens/Downloads"
            os.chdir(initDir)

    if os.path.isfile('report.csv'):
        os.remove('report.csv')
        open('report.csv', 'x')

    return initDir

def writeLine(line):
    with open('report.csv', 'a', newline = '') as csvfile:
        spamwriter = csv.writer(
            csvfile,
            delimiter = ',',
            quotechar = '|',
            quoting = csv.QUOTE_MINIMAL,
        )

        spamwriter.writerow(line)