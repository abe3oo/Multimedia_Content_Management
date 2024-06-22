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
    categories = ['Nature', 'Portraits', 'Abstract', 'Urban', 'Wildlife']
    return render_template('index.html',categories=categories)

@app.route('/photographers')
def photographers():
    persons = get_allpersons()
    return render_template('photographer.html',persons=persons)


@app.route('/photographers/<int:person_id>')
def person_action(person_id):
    photos = get_images_byid(person_id)
    articless = get_articles_byid(person_id)
    return render_template('photos.html', photos=photos, articless=articless)

@app.route('/photos')
def photos():
    return render_template('photos.html')

@app.route('/articles')
def articles():
    return render_template('articles.html')


if __name__ == '__main__':
    app.run(debug=True)
    

