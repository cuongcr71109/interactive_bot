from tkinter import Event
import PySimpleGUI as sg
import pandas as pd
import mysql.connector
import db
from db import*

account = []
content = []
order = []

def getExcel():
    import_file_path = values['file']
    data = pd.read_excel(import_file_path)
    

    # global account, content, order

    val= data.values.tolist()
    return val
    
    


def upload():
    
    
    sql = "INSERT INTO data_tbl (account_name, text_content, ordered) VALUES (%s, %s, %s)"
    data = getExcel()
    mycursor.executemany(sql, data)
    datab.commit()
    print(mycursor.rowcount, "was inserted.")

window_title = 'Insert data'
window_loc = (0,0)
window_size = (800, 600)

layout = [
    [sg.Text('Choose file .xlsx to import:')],
    [sg.Input('Choose file .xlsx to import:', key='file'),
     sg.FileBrowse(file_types=(("Excel Files", "*.xlsx"), ("All Files", "*.*")))],
     [sg.Button('OK')]
]

window = sg.Window(title=window_title, size=window_size, location=window_loc, layout=layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    
    if event == 'OK':
        getExcel()
        upload()
        break


window.close()
