from . import readwriteJSON

def checkVersion(appVer: str):
    verDick = {
        'Version': appVer
    }

    savedVer = readwriteJSON.readJSON('Version')
    
    match savedVer:
        case None:
            print("Version not stored in JSON")
            readwriteJSON.writeJSON(verDick)
            return
        case '':
            readwriteJSON.writeJSON(verDick)
            return
        case savedVer if savedVer != appVer:
            print("Version does not match")
            return
        case savedVer if savedVer == appVer:
            print("Version matches")
            return
