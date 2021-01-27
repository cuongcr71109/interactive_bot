import mysql.connector 
import pandas as pd


mydb = mysql.connector.connect(host='localhost', username='root', password='', database='interact_tool')
cursor = mydb.cursor(dictionary=True, buffered=True)

if cursor:
    print('Connected to DB.')
else:
    print('Connect failed')







