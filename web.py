from flask import Flask, render_template, request
from config import load_config
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
class Person2():
    def __init__(self,id,fname,lname,age):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.age = age


def get_db_connection():
    conn = ps.connect(**config)
    return conn
def get_allpersons():

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM person;")
    a = cur.fetchall()
    result = []
    for i in a:
        p = Person2(i[0],i[1],i[2],i[3])
        result.append(p)
    return result

#app ----------------------------------------
@app.route('/')

def index():
    return render_template('index.html')

@app.route('/photographers')
def photographers():
    persons = get_allpersons()
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM person;')
    photographers = cur.fetchall()
    cur.close()
    conn.close()
    """
    return render_template('photographer.html',persons=persons)


@app.route('/person/<int:person_id>')
def person_action(person_id):
    person = "a"
    if person:
        # انجام عملیات خاص، برای مثال نمایش اطلاعات فرد
        return f"Performing action for person: {person.name}, Age: {person.age}"
    else:
        return "Person not found", 404
    

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
    

