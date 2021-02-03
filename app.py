from datetime import date, datetime
import os
from random import triangular
import re
from flask import Flask, render_template, redirect, session, request, url_for
from flask_apscheduler import APScheduler
from functools import wraps
import hashlib
from werkzeug.utils import secure_filename
from flask.helpers import flash
from db import *
from telethon.sync import TelegramClient
from telethon.tl.types import ChatInvite,ChatInviteAlready, Chat, ChannelForbidden
from telethon.tl.functions.messages import CheckChatInviteRequest, ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from time import sleep
# ---------------
async def interact(client, group_id, content):
    me = await client.get_me()
    await client.send_message(group_id, content)
    print('From', session['username'], ':', me.phone, 'sent to {} -->'.format(group_id), content)

# check user in group or not
def check_and_join(client, group_type, group_link):
    if group_type == 'private':
        hash = group_link[22:]
        check = client(CheckChatInviteRequest(hash))
        if isinstance(check, ChatInvite):
            print('No join')
            join = client(ImportChatInviteRequest(hash = hash))
            print('join.chats[0].id', join.chats[0].id)
            return join.chats[0].id
        elif isinstance(check, ChatInviteAlready):
            if isinstance(check.chat, Chat):
                print('Joined')
                print(check.chat.id)
                return check.chat.id
            elif isinstance(check.chat, ChannelForbidden):
                print('be kicked')
    elif group_type == 'public':
        try:
            check = client(JoinChannelRequest(channel = group_link))
            print(check.chats[0].id)
            return check.chats[0].id
        except:
            print("be kicked")

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

        client = TelegramClient(session='{}'.format(user['phone']), api_id = int(user['api_id']), api_hash = user['api_hash'])
        with client:
            check_and_join(client, gr_typelink['group_type'], gr_typelink['group_link'])
            client.loop.run_until_complete(interact(client, group_id, content))
        sleep(dial['delay'])

# ---------------------------

# DATABASE FUNCTIONS ---------------
# get data from Excel file
def getExcel(file):
    data = pd.read_excel(file)
    val = data.values.tolist()
    return val

# create new dialog table in DB for new customer
def newTable(username):
    cursor.execute('CREATE TABLE IF NOT EXISTS {} (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT(10), content VARCHAR(255), group_id VARCHAR(255), delay INT(10))'.format(username))
    mydb.commit()

# get users info from database
def getUser():
    query = "SELECT * FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    return users

# get groups info from database
def getGroup():
    query = 'SELECT * FROM groups WHERE customer_username = "{}"'.format(session['username'])
    cursor.execute(query)
    groups = cursor.fetchall()
    return groups

# get dialogue data from database
def getDialogue():
    query = "SELECT * FROM {}".format(session['username'])
    cursor.execute(query)
    dialogue = cursor.fetchall()
    return dialogue


# end database functions -------------


# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'loggedin' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap
def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['isAdmin'] == 1:
            return f(*args, **kwargs)
        else:
            return redirect('/index')
    return wrap

# FLASK ROUTES ---------------
UPLOAD_FOLDER = "uploaded_files"

app = Flask(__name__)
app.secret_key = b'\xa3\x92.\x8b\\\x06\x17\x9e1\x1c4\xb6\xf2\xff}\xfb'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


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
    # dialogue [{'id': 1, 'customer_username': 0, 'user_id': 1, 'content': 'Hello.', 'group_id': '-1001158850531'}]
    return render_template('index.html', groups = groups, dialog = dialogue, session = session)

@app.route('/login', methods =['GET', 'POST']) 
def login():
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
            session['isAdmin'] = account['isAdmin']
            msg = 'Logged in successfully! Redirecting...'
            return redirect('/index')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html') 
  
@app.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('username', None) 
    return redirect(url_for('login')) 
  
@app.route('/register', methods =['GET', 'POST'])
# @admin_required
def register():
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
        else: 
            cursor.execute('INSERT INTO customers VALUES (NULL, %s, %s, %s, %s, 0)', (username, password, fname, phone)) 
            mydb.commit()

            newTable(request.form['username']) #create new table on db for new user

            try:
                # create new folders to store user's uploaded files
                new_folder = os.path.join(app.config['UPLOAD_FOLDER'], request.form['username'])
                os.makedirs(new_folder)
            except OSError:
                print('Folder existed')
                pass

            regError = 'You have successfully registered! Redirecting...'
            return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('register.html')

@app.route('/deleteAllContent')
def deleteAllContent():
    cursor.execute('TRUNCATE TABLE {}'.format(session['username']))
    mydb.commit()
    print('All content deleted')
    return redirect(url_for('index'))

@app.route('/deleteAllGroups')
def deleteAllGroups():
    cursor.execute('DELETE FROM groups WHERE customer_username = "{}"'.format(session['username']))
    mydb.commit()
    print('All groups deleted')
    return redirect(url_for('index'))

@app.route('/uploadGroupFile', methods=['GET', 'POST'])
def uploadGroupFile():
    if request.method == 'POST':
        if 'groupfile' not in request.files:
            flash('No file part')
            return redirect(request.url)

        groupfile = request.files['groupfile']
        if groupfile.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if groupfile:
            filename = secure_filename(groupfile.filename)
            path = app.config['UPLOAD_FOLDER'] + '\\' +  session['username']
            groupfile.save(os.path.join(path, filename))

            filepath = path + '\\' + filename
            print(filepath)
            val = getExcel(filepath)
            # val [[1, 1, -1001158850531, 'Test BOT', 'private', 'https://t.me/joinchat/HZesgX2L5zcpKvq0']]
            query =  'INSERT INTO groups (id, customer_username, group_id, group_title, group_type, group_link) VALUES (NULL, "{}", %s, %s, %s, %s)'.format(session['username'])
            print(query)
            print(val)
            cursor.executemany(query, val)
            mydb.commit()
            print(cursor.rowcount, "was inserted to [groups] table")
    return redirect(url_for('index'))

@app.route('/uploadContentFile', methods=['GET', 'POST'])
def uploadContentFile():
    if request.method == 'POST':
        if 'contentfile' not in request.files:
            flash('No file part')
            return redirect(request.url)

        contentfile = request.files['contentfile']
        if contentfile.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if contentfile:
            filename = secure_filename(contentfile.filename)
            path = app.config['UPLOAD_FOLDER'] + '\\' +  session['username']
            contentfile.save(os.path.join(path, filename))
            
            filepath = path + '\\' + filename
            query =  'INSERT INTO {} (user_id, content, group_id, delay) VALUES (%s, %s, %s, %s)'.format(session['username'])
            val = getExcel(filepath)
            print(query)
            print(val)
            cursor.executemany(query, val)
            mydb.commit()
            print(cursor.rowcount, 'was inserted to [{}] table'.format(session['username']))
    return redirect(url_for('index'))

# get data from excel file and insert data to database
@app.route('/insertUsers')
@admin_required
def insertUsers():
    query =  "INSERT IGNORE INTO users (id, user_id, api_id, api_hash, username, phone) VALUES (%s, %s, %s, %s, %s, %s)"
    val = getExcel('users.xlsx')
    cursor.executemany(query, val)
    mydb.commit()
    print(cursor.rowcount, "was inserted to [users] table")

@app.route('/renderSetAdmin')
def renderSetAdmin():
    cursor.execute('SELECT username, fname FROM customers WHERE isAdmin = 0')
    customer = cursor.fetchall()
    cursor.execute('SELECT username, fname FROM customers WHERE isAdmin = 1')
    admin = cursor.fetchall()
    return render_template('setadmin.html', customer = customer, admin = admin)

@app.route('/setAdmin', methods=['GET', 'POST'])
@admin_required
def setAdmin():
    username = tuple(request.form['setAdmin'].split())
    if len(username) != 1:
        query = 'UPDATE customers SET isAdmin = 1 WHERE username IN {}'.format(username)
    else:
        query = 'UPDATE customers SET isAdmin = 1 WHERE username = "{}"'.format(username[0])
    cursor.execute(query)
    mydb.commit()
    return redirect(url_for('renderSetAdmin'))

@app.route('/revokeAdmin', methods=['GET', 'POST'])
@admin_required
def revokeAdmin():
    username = tuple(request.form['revokeAdmin'].split())
    print(username)
    if len(username) != 1:
        query = 'UPDATE customers SET isAdmin = 0 WHERE username IN {}'.format(username)
    else:
        query = 'UPDATE customers SET isAdmin = 0 WHERE username = "{}"'.format(username[0])
    cursor.execute(query)
    mydb.commit()
    return redirect(url_for('renderSetAdmin'))

@app.route('/start')
def start():
    main_function()
    return redirect(url_for('index'))



@app.route('/schedule-tasks', methods=['GET', 'POST'])
def scheduler():
    now = datetime.now().strftime('%H%M%S')
    app.apscheduler.add_job(id=session['username']+now, trigger='cron', func=getTime, minute='*/1')
    return redirect(url_for('index')),'alert("Schedule successfully")'
    # return 'Success'

def getTime():
    time = datetime.now().strftime('%H:%M')
    print(time, 'at', datetime.now())
    # hourSelected = request.form['hourSelect']
    # if time == hourSelected:
    #     main_function()

# end flask routes ------------
