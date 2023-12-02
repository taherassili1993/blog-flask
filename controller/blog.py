from flask import Blueprint, request, render_template, session, redirect, url_for
import pymysql
from datetime import datetime
from database import db

blog_app = Blueprint('blog_app', __name__, template_folder='templates')

@blog_app.route('/ajouter-article')
def ajouter_article():
    return render_template("ajouter_article.html")

@blog_app.route('/ajouter-article', methods = ['POST'])
def article_post():
    titre = request.form.get('titre')
    content = request.form.get('content')
    user_id = session['id']
    created_at = datetime.now()

    db_config = db.db_config

    db_conn = pymysql.connect(**db_config)
    cursor = db_conn.cursor()

    cursor.execute('insert into articles(titre, content, user_id, created_at) values(%s, %s, %s, NOW())', (titre, content, user_id))
    
    # add the article to the database
    db_conn.commit()

    cursor.execute('select id from articles where titre = %s and content = %s and user_id = %s', (titre, content, user_id))
    findArticle = cursor.fetchone()

    return redirect(url_for('blog_app.article', id = findArticle[0]))

@blog_app.route('/article/<id>')
def article(id):
    return render_template("article.html")