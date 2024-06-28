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
    def __init__(self,photo_id,path,title="null",description="null",category="null",tags="null"):
        self.photo_id = photo_id
        self.path = path
        self.title = title
        self.description = description
        self.category = category
        self.tags = tags

class article():
    def __init__(self,article_id,content="null",title="null",category="null",keywords="null"):
        self.article_id = article_id
        self.content = content
        self.title = title
        self.category = category
        self.keywords = keywords

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
    sql2 = """
    SELECT t.tag_name
    FROM tags t
    JOIN phototag pt ON t.tag_id = pt.tag_id
    WHERE pt.photo_id = %s;

    """
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
    except Exception as e:
        print(e)
    else:
        a = cur.fetchall()
    finally:
        cur.close()
    
    result = []
    for i in a:
        try:
            cur = conn.cursor()
            data = (i[0],)
            cur.execute(sql2,data)
        except Exception as e:
            print(e)
        else:
            tags = cur.fetchall()
        finally:
            cur.close()
        alltags = ""
        r = 0
        for b in tags:
            if r == 0:
                alltags = alltags + b[0]
            else:
                alltags = alltags +","+ b[0]
            r+=1
        img = image(i[0],i[1],i[2],i[3],i[4],alltags)
        result.append(img)
    cur.close()
    conn.close()
    return result

def get_images_categorys():
    sql = f"SELECT category FROM images;"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    a = cur.fetchall()
    result = []
    result.append("ALL")
    for i in a:
        if i[0] not in result:
            result.append(i[0])
    cur.close()
    conn.close()
    return result
def get_image_by_category(category):
    if category == "all":
        sql = "SELECT * FROM images;"
    else:
        sql = f"SELECT * FROM images WHERE category ILIKE '{category}'"
    sql2 = """
    SELECT t.tag_name
    FROM tags t
    JOIN phototag pt ON t.tag_id = pt.tag_id
    WHERE pt.photo_id = %s;

    """
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
    except Exception as e:
        print(e)
    else:
        a = cur.fetchall()
    finally:
        cur.close()
    
    result = []
    for i in a:
        try:
            cur = conn.cursor()
            data = (i[0],)
            cur.execute(sql2,data)
        except Exception as e:
            print(e)
        else:
            tags = cur.fetchall()
        finally:
            cur.close()
        alltags = ""
        r = 0
        for b in tags:
            if r == 0:
                alltags = alltags + b[0]
            else:
                alltags = alltags +","+ b[0]
            r+=1
        img = image(i[0],i[1],i[2],i[3],i[4],alltags)
        result.append(img)
    cur.close()
    conn.close()
    return result

def get_articles_byid(id):
    sql = f"SELECT * FROM articles WHERE w_id = {id}"
    sql2 = """
    SELECT t.keyword_name
    FROM keywords t
    JOIN article_keyword pt ON t.keyword_id = pt.keyword_id
    WHERE pt.article_id = %s;

    """
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
    except Exception as e:
        print(e)
    else:
        a = cur.fetchall()
    finally:
        cur.close()

    result = []
    for i in a:
        try:
            cur = conn.cursor()
            data = (i[0],)
            cur.execute(sql2,data)
        except Exception as e:
            print(e)
        else:
            keywords = cur.fetchall()
        finally:
            cur.close()
        allkeywords = ""
        r = 0
        for b in keywords:
            if r == 0:
                allkeywords = allkeywords + b[0]
            else:
                allkeywords = allkeywords +","+ b[0]
            r+=1
        art = article(i[0],i[1],i[2],i[3],allkeywords)
        result.append(art)
    cur.close()
    conn.close()
    return result

def get_articles_by_category(category):
    if category == 'all':
        sql = f"SELECT * FROM articles;"
    else:
        sql = f"SELECT * FROM articles WHERE category ILIKE '{category}'"
    sql2 = """
    SELECT t.keyword_name
    FROM keywords t
    JOIN article_keyword pt ON t.keyword_id = pt.keyword_id
    WHERE pt.article_id = %s;

    """
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
    except Exception as e:
        print(e)
    else:
        a = cur.fetchall()
    finally:
        cur.close()
    result = []
    for i in a:
        try:
            cur = conn.cursor()
            data = (i[0],)
            cur.execute(sql2,data)
        except Exception as e:
            print(e)
        else:
            keywords = cur.fetchall()
        finally:
            cur.close()
        allkeywords = ""
        r = 0
        for b in keywords:
            if r == 0:
                allkeywords = allkeywords + b[0]
            else:
                allkeywords = allkeywords +","+ b[0]
            r+=1
        art = article(i[0],i[1],i[2],i[3],allkeywords)
        result.append(art)
    cur.close()
    conn.close()
    return result

def get_article_categorys():
    sql = f"SELECT category FROM articles;"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    a = cur.fetchall()
    result = []
    result.append("ALL")

    for i in a:
        if i[0] not in result:
            result.append(i[0])
    return result
