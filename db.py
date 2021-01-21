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
    data = pd.read_excel(file)
    val = data.values.tolist()
    return val

# get data from excel file and insert data to database
def insertUsers():
    # empty_table()
    query =  "INSERT IGNORE INTO users (id, user_id, api_id, api_hash, username, phone) VALUES (%s, %s, %s, %s, %s, %s)"
    val = getExcel('users.xlsx')
    cursor.executemany(query, val)
    mydb.commit()
    print(cursor.rowcount, "was inserted to [users] table")

def insertGroups():
    # empty_table()
    val = getExcel('groups.xlsx')
    # val [[1, -1001158850531, 'Test BOT', 'private', 'https://t.me/joinchat/HZesgX2L5zcpKvq0']]
    query =  "INSERT IGNORE INTO groups (id, group_id, group_title, group_type, group_link) VALUES (%s, %s, %s, %s, %s)"
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
    return users


# get groups info from database
def getGroup():
    query = "SELECT * FROM groups"
    cursor.execute(query)
    groups = cursor.fetchall()
    return groups

# get dialogue data from database
def getDialogue():
    query = "SELECT * FROM dialogue"
    cursor.execute(query)
    dialogue = cursor.fetchall()
    return dialogue
