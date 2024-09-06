import json
import os, os.path
import platform

global ope, fileName
ope = platform.system()
fileName = "printvision.json"

def readJSON(dataName, newData = {}):
    match ope:
        case "Windows":
            os.chdir("C:/Users/Public")
        case "Darwin":
            os.chdir("/Users/ethanwiens/dev/PrintVision-Report")
        case _:
            print("Are you even using a computer?")

    if os.path.isfile(fileName):
        # try:
        with open(fileName, "r") as file:
            oldData = json.load(file)
            readData = oldData.get(dataName)

        match readData:
            case None:
                print(f"{dataName} not stored in JSON")
                writeJSON(newData)
                
                    

    else:
        with open(fileName, "x") as file:
            json.dump(newData, file, indent = 4)

def writeJSON(newData: dict):
    match ope:
        case "Windows":
            os.chdir("C:/Users/Public")
        case "Darwin":
            os.chdir("/Users/ethanwiens/dev/PrintVision-Report")
        case _:
            print("Are you even using a computer?")

    if os.path.isfile(fileName):
        return
    
    else:
        open(fileName, 'x')
        writeJSON(newData)
        
    