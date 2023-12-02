from flask import Flask, request, render_template, redirect, url_for, session
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from controller.blog import blog_app

app = Flask(__name__)
app.register_blueprint(blog_app)

@app.route('/')
def welcome():
    db_config = db.db_config

    db_conn = pymysql.connect(**db_config)
    cursor = db_conn.cursor()

    sql = db.sql
    sql_blog = db.sql_blog
 
    cursor.execute(sql)
    cursor.execute(sql_blog)

    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)

    # Redirect to login page
    return redirect(url_for('login'))

@app.route('/signup', methods=['POST'])
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
        return redirect(url_for('signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    cursor.execute('insert into users(email, name, password) values(%s, %s, %s)', (email, name, generate_password_hash(password)))
    
    # add the new user to the database
    db_conn.commit()

    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    db_config = db.db_config

    db_conn = pymysql.connect(**db_config)
    cursor = db_conn.cursor()

    cursor.execute('SELECT email, password, id, name FROM users where email = %s', (email))
    findUser = cursor.fetchone()

    if not findUser or not check_password_hash(findUser[1], password):
        return redirect(url_for('login'))

    if findUser:
        session['loggedin'] = True
        session['email'] = findUser[0]
        session['id'] = findUser[2]
        session['username'] = findUser[3]
        return redirect(url_for('welcome'))

    return redirect(url_for('welcome'))


app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.run()
