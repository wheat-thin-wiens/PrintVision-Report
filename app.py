# PrintVision Report Parser by Ethan Wiens
import funk
import os, os.path
import platform
import tkinter as tk

try:
    from ctypes import windll
    myappid = "mycompany.myproduct.subproduct.version"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

ope = platform.system()
basedir = os.path.dirname(__file__)
appVer = '0.6.0'

root = tk.Tk()
root.title("PrintVision Report")
root.resizable(0, 0)
root.iconbitmap(os.path.join(basedir, 'printing.ico'))

if ope == "Windows":
    root.geometry("365x300")
elif ope == "Darwin":
    root.geometry('525x365')

## Running the Program
if __name__ == '__main__':
    funk.checkVersion(appVer)
    funk.create_gui(root)
    root.mainloop()
