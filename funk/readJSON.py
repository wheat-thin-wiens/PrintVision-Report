import json
import os, os.path
import platform

global ope
ope = platform.system()

def checkJSON(newData, dataName):
    if ope == "Windows":
        os.chdir("C:/Users/Public")

    if os.path.isfile("printvision.json"):
        # try:
        with open("printvision.json", "r") as file:
            oldData = json.load(file)
            readData = oldData.get(dataName)

        

    else:
        with open("printvision.json", "x") as file:
            json.dump(newData, file, indent = 4)