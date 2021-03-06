from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from functools import wraps

from sqlhelpers import *
from forms import *

import time

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'evote'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, please login.", "danger")
            return redirect(url_for('login'))
    return wrap

def log_in_user(username):
    users = Table("users", "name", "email", "username", "password")
    user = users.getone("username", username)

    session['logged_in'] = True
    session['username'] = username
    session['name'] = user.get('name')
    session['email'] = user.get('email')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    users = Table("users", "name", "email", "username", "password")
    ct = time.strftime("%I:%M %p")
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        name = form.name.data

        if isnewuser(username):
            password = sha256_crypt.encrypt(form.password.data)
            users.insert(name,email,username,password)
            send_money("TBMM", username, 1)
            log_in_user(username)
            return redirect(url_for('vote'))
        else:
            flash('User already exists', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        candidate = request.form['password']

        users = Table("users", "name", "email", "username", "password")
        user = users.getone("username", username)
        accPass = user.get('password')

        if accPass is None:
            flash("Username is not found", 'danger')
            return redirect(url_for('login'))
        else:
            if sha256_crypt.verify(candidate, accPass):
                log_in_user(username)
                flash('You are now logged in.', 'success')
                return redirect(url_for('vote'))
            else:
                flash("Invalid password", 'danger')
                return redirect(url_for('login'))

    return render_template('login.html')

@app.route("/results")
@is_logged_in
def results():
    users = Table("users", "name", "email", "username", "password","candidate")
    data = users.search("candidate", 1)
    usernames = [user.get('username') for user in data]
    usernames1 = len(usernames)
    balance1 = get_balance1(usernames)
    return render_template('results.html', usernames=usernames, balance1=balance1, usernames1=usernames1, page='results')


@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    flash("Logout success", "success")
    return redirect(url_for('login'))

@app.route("/layout")
def layout():
    return render_template('layout.html', page='layout')

@app.route("/vote", methods = ['GET', 'POST'])
@is_logged_in
def vote():
    balance = get_balance(session.get('username'))
    users = Table("users", "name", "email", "username", "password","candidate")
    data = users.search("candidate", 1)
    usernames = [user.get('username') for user in data]
    balance1 = get_balance1(usernames)

    if request.method == 'POST':
        try:
            select = request.form.get('username')
            send_money(session.get('username'), select, 1)
            flash("Vote Sent!", "success")
            return redirect(url_for('results'))
        except Exception as e:
            flash(str(e), 'danger')

        return redirect(url_for('vote'))
    blockchain = get_blockchain().chain
    ct = time.strftime("%I:%M %p")
    return render_template('vote.html', balance=balance, balance1=balance1, candidatelist=usernames, session=session, ct=ct, blockchain=blockchain, page='vote')

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug = True)
