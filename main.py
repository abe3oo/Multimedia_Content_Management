import psycopg2 as ps
from config import load_config, check_id, check_tagname
import csv
#---------------------
config = load_config()
#---------------------
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

conn = ps.connect(**config)
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
            print("data imported.")
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


                        


    









"""

sql = "SELECT * FROM users;"
cnn = ps.connect(**config)
cur = cnn.cursor()
cur.execute(sql)
a = cur.fetchall()
print(a)
"""