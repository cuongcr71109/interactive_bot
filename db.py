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
def getExcel(file):
    print(file, type(file))
    # import_file_path = 'dialogue.xlsx'
    data = pd.read_excel(file)
    val = data.values.tolist()
    return val

# get data from excel file and insert data to database
def insertUsers():
    # empty_table()
    query =  "INSERT IGNORE INTO users (id, api_id, api_hash, username, phone) VALUES (%s, %s, %s, %s, %s)"
    val = getExcel('users.xlsx')
    cursor.executemany(query, val)
    mydb.commit()
    print(cursor.rowcount, "was inserted to [users] table")

def insertGroups():
    # empty_table()
    query =  "INSERT IGNORE INTO groups (id, group_id, group_title, group_type, group_link) VALUES (%s, %s, %s, %s, %s)"
    val = getExcel('groups.xlsx')
    cursor.executemany(query, val)
    mydb.commit()
    print(cursor.rowcount, "was inserted to [groups] table")

def insertDialog():
    # empty_table()
    query =  "INSERT IGNORE INTO dialogue (id, user_id, content, group_id) VALUES (%s, %s, %s, %s)"
    val = getExcel('dialogue.xlsx')
    cursor.executemany(query, val)
    mydb.commit()
    print(cursor.rowcount, "was inserted to [dialog] table")


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
