import json
import os, os.path
import platform

global ope, fileName
ope = platform.system()
fileName = "printvision.json"

def readJSON(dataName):
    match ope:
        case "Windows":
            os.chdir("C:/Users/Public")
        case "Darwin":
            os.chdir("/Users/ethanwiens/dev/PrintVision-Report")
        case "Linux":
            os.chdir("/Users/ethanwiens/dev/PrintVision-Report")
        case _:
            print("Are you even using a computer?")

    if os.path.isfile(fileName):
        try:
            with open(fileName, 'r') as file:
                oldData = json.load(file)
                readData = oldData.get(dataName)

            match readData:
                case None:
                    print(f"{dataName} is not saved")
                    return ''
                case _:
                    return readData

        except ValueError: # JSON file exists but its contents are empty
            return ''
    else:
        open(fileName, 'x')
        return ''

def writeJSON(newData: dict):
    dataName = list(newData.keys())[0]

    match ope:
        case "Windows":
            initDir = "C:/Users/Public"
            os.chdir(initDir)
        case "Darwin":
            initDir = "/Users/ethanwiens/dev/PrintVision-Report"
            os.chdir(initDir)
        case "Linux":
            initDir = "/Users/ethanwiens/dev/PrintVision-Report"
            os.chdir(initDir)
        case _:
            print("Are you even using a computer?")

    try:
        if os.path.isfile(fileName):
            with open(fileName, 'r') as file:
                oldData = json.load(file)
                oldData.update(newData)

            with open(fileName, 'w') as file:
                json.dump(oldData, file, indent = 4)
                print(f"Successfully saved {dataName}")
        
        else:
            open(fileName, 'x')
            writeJSON(newData)

    except ValueError:
        with open(fileName, 'w') as file:
            json.dump(newData, file, indent = 4)
    
