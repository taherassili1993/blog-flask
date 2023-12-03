from flask import Flask, request, render_template, redirect, url_for, session
import pymysql
from database import db
from controller.blog import blog_app
from controller.login import login_app

app = Flask(__name__)
app.register_blueprint(blog_app)
app.register_blueprint(login_app)

@app.route('/')
def welcome():
    db_config = db.db_config

    db_conn = pymysql.connect(**db_config)
    cursor = db_conn.cursor()

    sql = db.sql
    sql_blog = db.sql_blog
 
    cursor.execute(sql)
    cursor.execute(sql_blog)

    cursor.execute('select id, titre, content, created_at from articles limit 2')
    articles = cursor.fetchall()

    return render_template("index.html", articles = articles)


app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.run()
