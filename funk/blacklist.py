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