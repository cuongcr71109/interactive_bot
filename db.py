import mysql.connector 
import pandas as pd 


mydb = mysql.connector.connect(host='localhost', username='root', password='', database='interact_tool')
cursor = mydb.cursor()

if cursor:
    print('Connected to DB.')
else:
    print('Connect failed')

def empty_table():
    query = 'TRUNCATE TABLE dialogue'
    cursor.execute(query)
    mydb.commit()

# import dialogue data from Excel file
def getExcel():
    import_file_path = 'Dialogue.xlsx'
    data = pd.read_excel(import_file_path)
    val = data.values.tolist()
    return val

def insertData():
    empty_table()
    query =  "INSERT INTO dialogue (user_id, content, group_id) VALUES (%s, %s, %s)"
    val = getExcel()
    cursor.executemany(query, val)
    mydb.commit()
    print(cursor.rowcount, "was inserted to database")

# get users info from database
def getUser():
    query = "SELECT * FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    print('users', users, type(users))
    print('--------------')
    return users


# get groups info from database
def getGroup():
    query = "SELECT * FROM groups"
    cursor.execute(query)
    groups = cursor.fetchall()
    print('groups', groups, type(groups), type(groups[0][0]))
    print('--------------')
    return groups

# get dialogue data from database
def getDialogue():
    query = "SELECT * FROM dialogue"
    cursor.execute(query)
    dialogue = cursor.fetchall()
    print('dialogue', dialogue, type(dialogue))
    print('--------------')
    return dialogue
