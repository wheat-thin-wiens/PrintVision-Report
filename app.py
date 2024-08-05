# PrintVision Report Parser by Ethan Wiens
import funk
import tkinter as tk

root = tk.Tk()
root.geometry("365x300")
root.title("PrintVision Report")
root.iconbitmap('printing.ico')

## Running the Program
if __name__ == '__main__':
    funk.create_gui(root)
    root.mainloop()
