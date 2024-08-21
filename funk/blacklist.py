import json
import os, os.path
import platform

global ope
ope = platform.system()

def saveList(list):
    list = list.split(', ')

    blacklist = {
        'Blacklist': list
    }

    if ope == 'Windows':
        os.chdir('C:/Users/Public')
    elif ope == 'Darwin':
        os.chdir('/Users/ethanwiens/dev/PrintVision-Report')

    try:
        with open('printvision.json', 'r') as file:
            data = json.load(file)
            data.update(blacklist)
        with open('printvision.json', 'w') as file:
            json.dump(data, file, indent = 4)
    except FileNotFoundError:
        with open('printvision.json', 'x') as file:
            json.dump(blacklist, file, indent = 4)

def readList(data, blacklist):
    for x in blacklist:
        if x in data:
            data = []
            return data
        else:
            return data
        
def checkBlacklist(line):
    if ope == 'Windows':
        os.chdir('C:/Users/Public')
    elif ope == 'Darwin':
        os.chdir('/Users/ethanwiens/dev/PrintVision-Report')

    with open('printvision.json', 'r') as file:
        data = json.load(file)
        theList = data.get('Blacklist')

    for x in theList:
        if x in line:
            print(f'Found blacklisted item: {line[3]}')
            line = []
            return line
        else:
            continue
    return line

def csvCheckBlacklist(line):
    if ope == "windows":
        os.chdir('C:/Users/Public')

    with open('printvision.json', 'r') as file:
        data = json.load(file)
        theList = data.get('Blacklist')

    line_copy = []
    for x in line:
        line_copy.append(x.replace('"', ''))

    for x in theList:
        if x in line_copy:
            print(f'Found blacklisted item: {line_copy[3]}')
            line_copy = []
            return line_copy
        else:
            continue
    return line_copy