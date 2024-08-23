# PrintVision Report Parser by Ethan Wiens
import funk
import os
import platform
import tkinter as tk

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll
    myappid = "mycompany.myproduct.subproduct.version"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

ope = platform.system()
root = tk.Tk()

if ope == "Windows":
    root.geometry("365x300")
elif ope == "Darwin":
    root.geometry('525x365')

root.title("PrintVision Report")
root.iconbitmap(os.path.join(basedir, 'printing.ico'))

## Running the Program
if __name__ == '__main__':
    funk.create_gui(root)
    root.mainloop()
