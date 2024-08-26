import json
import os, os.path
import platform

global ope 
ope = platform.system()

def checkVersion(appVer):
    if ope == "Windows":
        os.chdir('C:/Users/Public')

    verDick = {
        'Version': appVer
    }

    if os.path.isfile("printvision.json"):
        with open('printvision.json', 'r') as file:
            data = json.load(file)
            ver = data.get('Version')
            print(ver)
    
        if ver == None:
            print('Version not stored in JSON')
            
            with open('printvision.json', 'r') as file:
                data = json.load(file)
                data.update(verDick)
            with open('printvision.json', 'w') as file:
                json.dump(data, file, indent = 4)

        elif ver != appVer:
            print('Version does not match')
            return
        
        elif ver == appVer:
            print('Version matches')
            return
        
    else:
        with open('printvision.json', 'x') as file:
            json.dump(verDick, file, indent = 4)
