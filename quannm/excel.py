from tkinter import Event
import PySimpleGUI as sg
import pandas as pd
import mysql.connector

account = []
content = []
order = []

def getExcel():
    import_file_path = values['file']
    data = pd.read_excel(import_file_path)
    df = pd.DataFrame(data=data)

    # global account, content, order

    account = data.iloc[:, 0]
    content = data.iloc[:, 1]
    order = data.iloc[:, 2]

    print(df)


    # ret
    


def upload():
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database="test")
    mycursor = mydb.cursor()
    sql = "INSERT INTO user (Account, Content, Order) VALUES (%s, %s, %s)"
    data = getExcel()
    mycursor.executemany(sql, data)
    mydb.commit()
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
        # upload()
        break


window.close()
