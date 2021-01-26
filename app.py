from configparser import Error
import re
from flask import Flask, render_template, redirect, session, request, url_for
from functools import wraps
import hashlib

from db import *

# ----------------
from telethon.sync import TelegramClient, events, types
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from time import sleep
# ---------------
async def interact(client, group_id, content):
    me = await client.get_me()
    await client.send_message(group_id, content)
    print(me.phone, 'sent to {} -->'.format(group_id), content)
    sleep(1)

# check user in group or not
def checkin_group(client, group_id):
    dialog_id = []
    for dialog in client.iter_dialogs():
        dialog_id.append(dialog.id)
    return group_id in dialog_id

# join group if user is not in group
def join_group(client, group_type, group_link):
    if group_type == 'private':
        join = client(ImportChatInviteRequest(hash=group_link))
        print('Join to private')

    elif group_type == 'public':
        join = client(JoinChannelRequest(channel=group_link))
        print('Join to public')
# ---------------------------


app = Flask(__name__)
app.secret_key = b'\xa3\x92.\x8b\\\x06\x17\x9e1\x1c4\xb6\xf2\xff}\xfb'


# get data from Excel file
def getExcel(file):
    data = pd.read_excel(file)
    val = data.values.tolist()
    return val

# create new dialog table in DB for new customer
def newTable(username):
    cursor.execute('CREATE TABLE IF NOT EXISTS {} (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT(10), content VARCHAR(255), group_id VARCHAR(255))'.format(username))
    mydb.commit()

# get users info from database
def getUser():
    query = "SELECT * FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    print(users)
    print('---------------------')
    return users

# get groups info from database
def getGroup():
    query = "SELECT * FROM groups WHERE customer_id = {}".format(session['id'])
    cursor.execute(query)
    groups = cursor.fetchall()
    print(groups)
    print('---------------------')
    return groups

# get dialogue data from database
def getDialogue():
    query = "SELECT * FROM {}".format(session['username'])
    cursor.execute(query)
    dialogue = cursor.fetchall()
    print(dialogue)
    print('---------------------')
    return dialogue

# get data from excel file and insert data to database
def insertUsers():
    # empty_table()
    query =  "INSERT IGNORE INTO users (id, user_id, api_id, api_hash, username, phone) VALUES (%s, %s, %s, %s, %s, %s)"
    val = getExcel('users.xlsx')
    cursor.executemany(query, val)
    mydb.commit()
    print(cursor.rowcount, "was inserted to [users] table")


# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'loggedin' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap

@app.route('/')
def main():
    return redirect(url_for('login'))

@app.route('/index')
@login_required
def index():
    users = getUser()
    # users [{'id': 1, 'user_id': 784093829, 'api_id': 2484767, 'api_hash': 'df8557fedd7d125f1128eec0fb021f27', 'username': 'quannmUET', 'phone': '84856852624'}]

    groups = getGroup()
    # groups [{'id': 1, 'group_id': '-1001158850531', 'group_title': 'Test BOT', 'group_type': 'private', 'group_link': 'HZesgX2L5zcpKvq0'}]

    dialogue = getDialogue()
    # dialogue [{'id': 1, 'customer_id': 0, 'user_id': 1, 'content': 'Hello.', 'group_id': '-1001158850531'}]
    return render_template('index.html', groups = groups, dialog = dialogue)

@app.route('/login', methods =['GET', 'POST']) 
def login(): 
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username'] 
        password_raw = request.form['password']
        password_hash = hashlib.md5(password_raw.encode())
        password = password_hash.hexdigest()

        cursor.execute('SELECT * FROM customers WHERE username = %s AND password = %s', (username, password)) 
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['phone'] = account['phone']
            msg = 'Logged in successfully! Redirecting...'
            return redirect('/index')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg) 
  
@app.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('username', None) 
    return redirect(url_for('login')) 
  
@app.route('/register', methods =['GET', 'POST']) 
def register(): 
    username_Error = '' 
    password_Error = ''
    phone_Error = ''
    regError = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'phone' in request.form : 
        username = request.form['username'] 
        password_raw = request.form['password']
        password_hash = hashlib.md5(password_raw.encode())
        password = password_hash.hexdigest()
        phone = request.form['phone']
        fname = request.form['fname']
        
        cursor.execute('SELECT * FROM customers WHERE username = %s', (username, )) 
        account = cursor.fetchone() 
        if account: 
            username_Error = 'Account already exists !'
        elif not re.match(r'^[+][0-9]', phone): 
            phone_Error = 'Invalid phone number! Example: +84123456789'
        elif not re.match(r'[A-Za-z0-9]+', username): 
            username_Error = 'Username must contain only characters and numbers !'
        elif not re.match(r'[A-Za-z ]+', fname): 
            username_Error = 'Name must contain only characters and space!'
        elif not username or not password or not phone:
            regError = 'Fields can not be empty'
        else: 
            cursor.execute('INSERT INTO customers VALUES (NULL, %s, %s, %s, %s)', (username, password, fname, phone, )) 
            mydb.commit()
            newTable(request.form['username'])
            regError = 'You have successfully registered! Redirecting...'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        regError = 'Please fill out the form !'
    return render_template('register.html', regError = regError, username_Error = username_Error, password_Error = password_Error, phone_Error = phone_Error)

@app.route('/insertGroups')
def insertGroups():
    val = getExcel('groups.xlsx')
    # val [[1, 1, -1001158850531, 'Test BOT', 'private', 'https://t.me/joinchat/HZesgX2L5zcpKvq0']]
    query =  "INSERT IGNORE INTO groups (id, customer_id, group_id, group_title, group_type, group_link) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, val)
    mydb.commit()
    print(cursor.rowcount, "was inserted to [groups] table")
    return redirect(url_for('index'))

@app.route('/insertDialogue')
def insertDialog():
    # empty_table()
    query =  "INSERT IGNORE INTO {} (id, user_id, content, group_id) VALUES (%s, %s, %s, %s)".format(session['username'])
    val = getExcel('dialogue.xlsx')
    cursor.executemany(query, val)
    mydb.commit()
    print(cursor.rowcount, "was inserted to [{}] table".format(session['username']))
    return redirect(url_for('index'))

@app.route('/start')
def main_function():
    dialogue = getDialogue()
    for dial in dialogue:
        group_id = int(dial['group_id'])
        content = dial['content']

        # get api_id and api_hash to create Client
        query = 'SELECT api_id, api_hash, phone FROM users WHERE id = {}'.format(dial['user_id'])
        cursor.execute(query)
        user = cursor.fetchone()
        # user [{'api_id': 2484767, 'api_hash': 'df8557fedd7d125f1128eec0fb021f27', 'phone': '84856852624'}]

        # get group_type and group_link to join
        query = 'SELECT group_type, group_link FROM groups WHERE group_id = {}'.format(group_id)
        cursor.execute(query)
        gr_typelink = cursor.fetchone()
        # gr_typelink [('private', 'https://t.me/joinchat/HZesgX2L5zcpKvq0')]
        print('ok')

        try:
            client = TelegramClient(session='{}'.format(user['phone']), api_id = int(user['api_id']), api_hash = user['api_hash'])

        except Error:
            print(Error)
        # print(client)
        # with client:
        #     if not checkin_group(client, group_id):
        #         join_group(client, gr_typelink['group_type'], gr_typelink['group_link'])
        #         client.loop.run_until_complete(interact(client, group_id, content))
        #     else:
        #         client.loop.run_until_complete(interact(client, group_id, content))
    return redirect(url_for('index'))