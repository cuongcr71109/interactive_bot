import re
from flask import Flask, render_template, redirect, session, request, url_for
from functools import wraps
from passlib.hash import pbkdf2_sha256 as sha256
import hashlib

from db import *


app = Flask(__name__)
app.secret_key = b'\xa3\x92.\x8b\\\x06\x17\x9e1\x1c4\xb6\xf2\xff}\xfb'



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
    return render_template('index.html')

@app.route('/login', methods =['GET', 'POST']) 
def login(): 
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username'] 
        password_raw = request.form['password']
        password_hash = hashlib.md5(password_raw.encode())
        password = password_hash.hexdigest()
        print(password)

        cursor.execute('SELECT * FROM customers WHERE username = %s AND password = %s', (username, password)) 
        account = cursor.fetchone()
        print(account)

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username'] 
            msg = 'Logged in successfully! Redirecting...'
            print(msg)
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
        print(username, password, phone, fname)
        

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
            regError = 'You have successfully registered! Redirecting...'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        regError = 'Please fill out the form !'
    return render_template('register.html', regError = regError, username_Error = username_Error, password_Error = password_Error, phone_Error = phone_Error)

