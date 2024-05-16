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
    if check_id(i[5]) == False:

        sql1 = """
            INSERT INTO person VALUES
            (%s,%s,%s,%s)
            """
        data1 = (i[5],i[6],i[7],i[8])

        sql2 = """
            INSERT INTO images(path,title,description,category,p_id) VALUES
            (%s,%s,%s,%s,%s)
            """
        data2 = (i[0], i[1], i[3], i[4], i[5])
        try:
            cur.execute(sql1,data1)
        
        except Exception as e:
            print(e)
        else:
            conn.commit()
            try:
                cur.execute(sql2, data2)
            except Exception as e:
                print(e)
            else:
                conn.commit()
            print("data imported.")
    else:
        sql1 = """
            INSERT INTO images(path,title,description,category,p_id) VALUES
            (%s,%s,%s,%s,%s)
            """
        data1 = (i[0], i[1], i[3], i[4], i[5])
        try:
            cur.execute(sql1,data1)
        except Exception as e:
            print(e)
        else:
            conn.commit()
        sql2 = """
            INSERT INTO tags(tag_name) VALUES
            (%s)
            """
        tags = i[2].split(",")
        for i in tags:
            if check_tagname(i) == False:
                try:

                    cur.execute(sql2)
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