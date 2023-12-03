from flask import Blueprint, request, render_template, session, redirect, url_for
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from database import db

login_app = Blueprint('login_app', __name__, template_folder='templates')

@login_app.route('/login')
def login():
    return render_template("login.html")

@login_app.route('/signup')
def signup():
    return render_template("signup.html")

@login_app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)

    # Redirect to login page
    return redirect(url_for('login_app.login'))

@login_app.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    db_config = db.db_config

    db_conn = pymysql.connect(**db_config)
    cursor = db_conn.cursor()

    cursor.execute('SELECT id, name FROM users where email = %s', (email))
    findUser = cursor.fetchone()

    
    if findUser: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('login_app.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    cursor.execute('insert into users(email, name, password) values(%s, %s, %s)', (email, name, generate_password_hash(password)))
    
    # add the new user to the database
    db_conn.commit()

    return redirect(url_for('login_app.login'))

@login_app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    db_config = db.db_config

    db_conn = pymysql.connect(**db_config)
    cursor = db_conn.cursor()

    cursor.execute('SELECT email, password, id, name FROM users where email = %s', (email))
    findUser = cursor.fetchone()

    if not findUser or not check_password_hash(findUser[1], password):
        return redirect(url_for('login_app.login'))

    if findUser:
        session['loggedin'] = True
        session['email'] = findUser[0]
        session['id'] = findUser[2]
        session['username'] = findUser[3]
        return redirect(url_for('welcome'))

    return redirect(url_for('welcome'))