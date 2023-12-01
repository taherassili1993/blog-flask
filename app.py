from flask import Flask, request, render_template
import pymysql
from database import db
app = Flask(__name__)
@app.route('/')
def welcome():
    db_config = db.db_config

    db_conn = pymysql.connect(**db_config)
    cursor = db_conn.cursor()

    sql = db.sql
 
    cursor.execute(sql)
    return render_template("index.html");
app.run()
