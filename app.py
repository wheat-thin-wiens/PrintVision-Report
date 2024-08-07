# PrintVision Report Parser by Ethan Wiens
import funk
import platform
import tkinter as tk

ope = platform.system()
root = tk.Tk()

if ope == "Windows":
    root.geometry("365x300")
elif ope == "Darwin":
    root.geometry('525x365')

root.title("PrintVision Report")
root.iconbitmap('printing.ico')

## Running the Program
if __name__ == '__main__':
    funk.create_gui(root)
    root.mainloop()
