import PySimpleGUI as sg
import pandas as pd
import mysql.connector
from db import *
import db

def getExcel():
    # get file path in gui windows
    import_file_path = values['file']

    # read data from excel file
    data = pd.read_excel(import_file_path)

    # convert data to dataframe
    df = pd.DataFrame(data=data)

    # Result:
    #        Account Content  Order
    # 0     Quan     abc      1
    # 1    Cuong     Xyz      2
    # 2     Phuc     Dce      3
    # 3      Duc     ghf      1
    # 4    Khang     abc      2

    # get data along columns Account, Content, Order
    val= data.values.tolist()

    # Result:
    # [('Quan', 'abc', 1), ('Cuong', 'Xyz', 2), ('Phuc', 'Dce', 3), ('Duc', 'ghf', 1), ('Khang', 'abc', 2)]

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
