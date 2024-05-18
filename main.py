import psycopg2 as ps
from config import load_config, check_id, check_tagname, check_keywordname
import csv
#---------------------
config = load_config()
#---------------------
#image_csv_parser ====>>>>

image_result = []
imagefilepath = "image.csv"
with open (imagefilepath, newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    i = 0
    for row in csv_reader:
        if i == 0:
            pass
        else:
            image_result.append(row)
        i+=1

#<<<<

#make_connection
conn = ps.connect(**config)

#image_to_DB ===>>>

cur = conn.cursor()
for i in image_result:
    photo_id = 0
    if check_id(i[5]) == False:
        #person ===============
        sql1 = """
            INSERT INTO person VALUES
            (%s,%s,%s,%s)
            """
        data1 = (i[5],i[6],i[7],i[8])

        try:
            cur.execute(sql1,data1)
        
        except Exception as e:
            print(e)
        else:
            conn.commit()
            #photo =====================
            sql2 = """
            INSERT INTO images(path,title,description,category,p_id) VALUES
            (%s,%s,%s,%s,%s) RETURNING photo_id
            """
            data2 = (i[0], i[1], i[3], i[4], i[5])
            try:
                cur.execute(sql2, data2)
            except Exception as e:
                print(e)
            else:
                a = cur.fetchall()
                photo_id = a[0][0]
                conn.commit()
            
        #tags ====================
        
        insert_tag_sql = """
            INSERT INTO tags(tag_name) VALUES
            (%s) RETURNING tag_id
            """
        select_tag_sql = """
            SELECT tag_id FROM tags WHERE tag_name = %s;
        """
        tags = i[2].split(",")
        tag_ids = []
        if tags[0] != "":
            for i in tags:
                data = (i,)
                if check_tagname(i) == False:
                    try:
                        cur.execute(insert_tag_sql,data)
                    except Exception as e:
                        print(e)
                    else:
                        a = cur.fetchall()
                        tag_ids.append(a[0][0])
                        conn.commit()
                else:
                    data = (i,)
                    try:

                        cur.execute(select_tag_sql, data)
                    except Exception as e:
                        print(e)
                    else:
                        a = cur.fetchall()
                        tag_ids.append(a[0][0])
        # phototag ======
        if len(tag_ids) != 0:
            for i in tag_ids:

                phototag_sql = """
                    INSERT INTO phototag VALUES (%s,%s)
                """
                data = (photo_id,i)
                try:

                    cur.execute(phototag_sql,data)
                except Exception as e:
                    print(e)
                else:
                    conn.commit()
# photo_only =========== 
        
    else:
        sql1 = """
            INSERT INTO images(path,title,description,category,p_id) VALUES
            (%s,%s,%s,%s,%s) RETURNING photo_id
            """
        data1 = (i[0], i[1], i[3], i[4], i[5])
        try:
            cur.execute(sql1,data1)
        except Exception as e:
            print(e)
        else:
            a = cur.fetchall()
            photo_id = a[0][0]
            conn.commit()
        
        #tags ================
        insert_tag_sql = """
            INSERT INTO tags(tag_name) VALUES
            (%s) RETURNING tag_id
            """
        select_tag_sql = """
            SELECT tag_id FROM tags WHERE tag_name = %s;
        """
        tags = i[2].split(",")
        tag_ids = []
        if tags[0] != "":
            for i in tags:
                data = (i,)
                if check_tagname(i) == False:
                    try:
                        cur.execute(insert_tag_sql,data)
                    except Exception as e:
                        print(e)
                    else:
                        a = cur.fetchall()
                        tag_ids.append(a[0][0])
                        conn.commit()
                else:
                    data = (i,)
                    try:

                        cur.execute(select_tag_sql, data)
                    except Exception as e:
                        print(e)
                    else:
                        a = cur.fetchall()
                        tag_ids.append(a[0][0])
        # phototag ======
        if len(tag_ids) != 0:
            for i in tag_ids:

                phototag_sql = """
                    INSERT INTO phototag VALUES (%s,%s)
                """
                data = (photo_id,i)
                try:

                    cur.execute(phototag_sql,data)
                except Exception as e:
                    print(e)
                else:
                    conn.commit()
    print(f"image imported with id {photo_id}.")
cur.close()
#<<<<
                    
#article_csv_parser ====>>>>

article_result = []
articlefilepath = "Article.csv"
with open (articlefilepath, newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    i = 0
    for row in csv_reader:
        if i == 0:
            pass
        else:
            article_result.append(row)
        i+=1
#<<<<

cur = conn.cursor()

#Artcle_to_DB ===>>>

for i in article_result:
    article_id = 0
    if check_id(i[4]) == False:
        #person ===============
        sql1 = """
            INSERT INTO person VALUES
            (%s,%s,%s,%s)
            """
        data1 = (i[4],i[5],i[6],i[7])

        try:
            cur.execute(sql1,data1)
        
        except Exception as e:
            print(e)
        else:
            conn.commit()
            #Article =====================
            sql2 = """
            INSERT INTO articles(content,title,category,w_id) VALUES
            (%s,%s,%s,%s) RETURNING article_id
            """
            data2 = (i[0], i[2], i[3], i[4])
            try:
                cur.execute(sql2, data2)
            except Exception as e:
                print(e)
            else:
                a = cur.fetchall()
                article_id = a[0][0]
                conn.commit()
        #keywords ====================
        
        insert_keyword_sql = """
            INSERT INTO keywords(keyword_name) VALUES
            (%s) RETURNING keyword_id
            """
        select_keyword_sql = """
            SELECT keyword_id FROM keywords WHERE keyword_name = %s;
        """
        keywords = i[1].split(",")
        keyword_ids = []
        if keywords[0] != "":
            for i in keywords:
                data = (i,)
                if check_keywordname(i) == False:
                    try:
                        cur.execute(insert_keyword_sql,data)
                    except Exception as e:
                        print(e)
                    else:
                        a = cur.fetchall()
                        keyword_ids.append(a[0][0])
                        conn.commit()
                else:
                    data = (i,)
                    try:
                        cur.execute(select_keyword_sql, data)
                    except Exception as e:
                        print(e)
                    else:
                        a = cur.fetchall()
                        keyword_ids.append(a[0][0])
        # article_keyword ======
        if len(keyword_ids) != 0:
            for i in keyword_ids:

                article_keyword_sql = """
                    INSERT INTO article_keyword VALUES (%s,%s)
                """
                data = (article_id,i)
                try:

                    cur.execute(article_keyword_sql,data)
                except Exception as e:
                    print(e)
                else:
                    conn.commit()

    else:
        sql2 = """
            INSERT INTO articles(content,title,category,w_id) VALUES
            (%s,%s,%s,%s) RETURNING article_id
            """
        data2 = (i[0], i[2], i[3], i[4])
        try:
            cur.execute(sql2, data2)
        except Exception as e:
            print(e)
        else:
            a = cur.fetchall()
            article_id = a[0][0]
            conn.commit()
        #keywords ================
            
        insert_keyword_sql = """
            INSERT INTO keywords(keyword_name) VALUES
            (%s) RETURNING keyword_id
            """
        select_keyword_sql = """
            SELECT keyword_id FROM keywords WHERE keyword_name = %s;
        """
        keywords = i[1].split(",")
        keyword_ids = []
        if keywords[0] != "":
            for i in keywords:
                data = (i,)
                if check_keywordname(i) == False:
                    try:
                        cur.execute(insert_keyword_sql,data)
                    except Exception as e:
                        print(e)
                    else:
                        a = cur.fetchall()
                        keyword_ids.append(a[0][0])
                        conn.commit()
                else:
                    data = (i,)
                    try:
                        cur.execute(select_keyword_sql, data)
                    except Exception as e:
                        print(e)
                    else:
                        a = cur.fetchall()
                        keyword_ids.append(a[0][0])
        # article_keyword ======
        
        if len(keyword_ids) != 0:
            for i in keyword_ids:

                article_keyword_sql = """
                    INSERT INTO article_keyword VALUES (%s,%s)
                """
                data = (article_id,i)
                try:

                    cur.execute(article_keyword_sql,data)
                except Exception as e:
                    print(e)
                else:
                    conn.commit()
    print(f"article imported with id {article_id}")
cur.close()
conn.close()
