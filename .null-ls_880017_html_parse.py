from bs4 import BeautifulSoup
import os
import requests
import time
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk

root = tk.Tk()
root.geometry("390x239")
root.title("PrintVision Report (HTML)")

def login():
    global pv_base

    pv_base = 'https://loffler.printfleet.com'
    user = username.get()
    passw = password.get()

    url = pv_base
    page = requests.get(url)
    print(page.status_code)

    runBtn.config(state = 'normal')

def create_gui():
    global hsptlValue, clncValue, statusVar, runBtn

    statusVar = tk.StringVar(value = "Ready")
    hsptlValue = tk.StringVar(value = '5')
    clncValue = tk.StringVar(value = '10')

    global username, password

    username = tk.StringVar(value = '')
    password = tk.StringVar(value = '')

    #frame1 = ttk.Frame(root)
    #frame1['borderwidth'] = 2
    #frame1['relief'] = 'groove'
    #frame1.grid(row = 0, column = 0, columnspan = 3, padx = 5, pady = 5, sticky = 'nsew')
    #frame1.columnconfigure([0, 1], weight = 1)

    frame1 = ttk.LabelFrame(root, text = "Login")
    frame1.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'new')

    #frame2 = tk.Frame(root)
    #frame2['borderwidth'] = 2
    #frame2['relief'] = 'groove'
    #frame2.grid(row = 2, column = 0, columnspan = 3, padx = 5, pady = 5, sticky = 'nsew')

    frame2 = ttk.LabelFrame(root, text = 'Report')
    frame2.grid(row = 2, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'new')

    sep = ttk.Separator(root, orient = 'horizontal')
    sep.grid(row = 1, column = 0, columnspan = 3, padx = 10, pady = 5, sticky = 'nsew')

    user_lbl = tk.Label(frame1, text = "User Name:     ")
    user_lbl.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'nw')
    user_entry = ttk.Entry(frame1, textvariable = username, width = 23, state = 'normal')
    user_entry.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = 'nw')

    pass_lbl = tk.Label(frame1, text = 'Password:')
    pass_lbl.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'nw')
    pass_entry = ttk.Entry(frame1, textvariable = password, width = 23)
    pass_entry.grid(row = 1, column = 1, padx = 10, pady = 5, sticky = 'nw')

    login_btn = ttk.Button(frame1, text = 'Login', command = login)
    login_btn.grid(row = 1, column = 3, padx = 10, pady = 5, sticky = 'e')

    location_dropdown = ttk.Combobox(
        frame2, 
        state = 'readonly', 
        values = ['All', 'Hospital', 'Clinics'],
        width = 20,
    )
    location_dropdown.current(0)
    location_dropdown.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = 'nw')
    location_label = tk.Label(frame2, text = 'Location:')
    location_label.grid(row = 0, column = 0, padx = 10, pady = 5, sticky = 'nw')

    hsptl_entry = ttk.Entry(frame2, textvariable = hsptlValue, width = 23)
    hsptl_entry.grid(row = 1, column = 1, padx = 10, pady = 5, sticky = 'nw')
    hsptl_label = tk.Label(frame2, text = 'Hospital Value:')
    hsptl_label.grid(row = 1, column = 0, padx = 10, pady = 5, sticky = 'nw')

    clnc_entry = ttk.Entry(frame2, textvariable = clncValue, width = 23)
    clnc_entry.grid(row = 2, column = 1, padx = 10, pady = 5, sticky = 'nw')
    clnc_label = tk.Label(frame2, text = 'Clinic Value:')
    clnc_label.grid(row = 2, column = 0, padx = 10, pady = 5, sticky = 'nw')

    runBtn = ttk.Button(frame2, text = "Run", state = 'disabled',)# command = lambda:run_report(location_dropdown.get()))
    runBtn.grid(row = 2, column = 3, padx = 10, pady = 5, sticky = 'se')

    #root.columnconfigure([0, 1], weight = 1, uniform = 'key')

if __name__ == '__main__':
    create_gui()
    root.mainloop()