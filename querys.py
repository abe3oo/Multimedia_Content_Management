from config import load_config
import psycopg2 as ps

config = load_config()

class Person():
    def __init__(self,id,fname,lname,age):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.age = age

class image():
    def __init__(self,photo_id,path,title,description,category):
        self.photo_id = photo_id
        self.path = path
        self.title = title
        self.description = description
        self.category = category

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
        p = Person(i[0],i[1],i[2],i[3])
        result.append(p)
    cur.close()
    conn.close()
    return result

def get_images_byid(id):
    sql = f"SELECT * FROM images WHERE p_id = {id}"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    a = cur.fetchall()
    result = []
    for i in a:
        img = image(i[0],i[1],i[2],i[3],i[4])
        result.append(img)
    
    return result
