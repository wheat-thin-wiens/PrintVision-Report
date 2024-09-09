from . import readwriteJSON

def saveList(list):
    list = list.split(', ')

    blacklist = {
        'Blacklist': list
    }

    readwriteJSON.writeJSON(blacklist)

def checkBlacklist(line):
    theList = readwriteJSON.readJSON("Blacklist")

    line_copy = []

    for x in line:
        if x is None:
            line_copy.append(" ")
        else:
            line_copy.append(x.replace('"', ''))

    for x in theList:
        if x in line_copy:
            print(f'Found blacklisted item: {line_copy[3]}')
            line_copy = []
            return line_copy
        else:
            continue
    return line_copy
