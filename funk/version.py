import json
import os, os.path
import platform

global ope 
ope = platform.system()

def checkVersion(appVer: str):
    if ope == "Windows":
        os.chdir('C:/Users/Public')

    verDick = {
        'Version': appVer
    }

    if os.path.isfile("printvision.json"):
        try:
            with open('printvision.json', 'r') as file:
                data = json.load(file)
                ver = data.get('Version')
        
            if ver == None:
                print('Version not stored in JSON')
                update_app(appVer, verDick)

            elif ver != appVer:
                print('Version does not match')
                # update_app(appVer, verDick)
                return
            
            elif ver == appVer:
                print('Version matches')
                return
        except ValueError:
            # JSON is present but contents are empty
            with open('printvision.json', 'x') as file:
                json.dump(verDick, file, indent = 4)
        
    else:
        with open('printvision.json', 'x') as file:
            json.dump(verDick, file, indent = 4)

def update_app(appVer: str, verDick: dict):
    if ope == "Windows":
        os.chdir("C:/Users/Public")

    with open('printvision.json', 'r') as file:
        data = json.load(file)
        data.update(verDick)
    
    with open('printvision.json', 'w') as file:
        json.dump(data, file, indent = 4)

    print(f'Version updated to {appVer}')