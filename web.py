from flask import Flask, render_template, request
from config import load_config
from querys import *
import psycopg2 as ps
import sqlite3
from flask_sqlalchemy import SQLAlchemy
config = load_config()


app = Flask(__name__)
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Ara41148@localhost/multimedia'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=True)
    lname = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=False)
"""

#app ----------------------------------------
@app.route('/')

def index():
    return render_template('index.html')

@app.route('/photographers')
def photographers():
    persons = get_allpersons()
    return render_template('photographer.html',persons=persons)


@app.route('/photographers/<int:person_id>')
def person_action(person_id):
    photos = get_images_byid(person_id)
    return render_template('photos.html', photos=photos)

@app.route('/photos')
def photos():
    category = request.args.get('category')
    conn = get_db_connection()
    cur = conn.cursor()
    if category:
        cur.execute('SELECT * FROM images;')
        photos = cur.fetchall()
    else:
        cur.execute('SELECT * FROM images;')
        photos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('photos.html', photos=photos)

@app.route('/articles')
def articles():
    category = request.args.get('category')
    conn = get_db_connection()
    cur = conn.cursor()
    if category:
        cur.execute('SELECT * FROM articles;')
        articles = cur.fetchall()
        
    else:
        cur.execute('SELECT * FROM articles;')
        articles = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('articles.html', articles=articles)


if __name__ == '__main__':
    app.run(debug=True)
    

