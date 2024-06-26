import csv
import psycopg2 as ps
from config import load_config, check_id, check_tagname
import requests
import json
lst1 = []
lst2 = []
config = load_config()

#photo_path = "D:/backup windows 10/pic/Cosmos-flowers-lead.jpg"
api_token = "1Fdo-vfrC-CECB-JO0z-TC"
api_url = "https://server.phototag.ai/api/keywords"

def fetch_not_complete_path():
    conn = ps.connect(**config)
    cur = conn.cursor()
    allmissedpath = []
    sql = "SELECT photo_id, path, title, description FROM images WHERE title = '' or description = '';"
    sql2 = """
    SELECT images.path
    FROM images
    LEFT JOIN phototag ON images.photo_id = phototag.photo_id
    WHERE phototag.photo_id IS NULL;
    """
    try:
        cur.execute(sql)
    except Exception as e:
        print(e)
    else:
        result = cur.fetchall()

    for i in result:
        if i[1] not in allmissedpath:
            allmissedpath.append(i[1])
    try:
        cur.execute(sql2)
    except Exception as e:
        print(e)
    else:
        result2 = cur.fetchall()

    for i in result2:
        if i[0] not in allmissedpath:
            allmissedpath.append(i[0])
    return allmissedpath

def fetch_additional_info(photo_path):
    with open(photo_path, 'rb') as image_file:
        files = {'file': image_file}
        headers = {
            'Authorization': f'Bearer {api_token}'
        }
        payload = {
        "language": "en",
        "maxKeywords": 4
        }
        response = requests.post(api_url, files=files, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

def fill_db_missitems():
    print("finding not completed path items ... ")
    allmissespath = fetch_not_complete_path()
    print("finded ...")
    conn = ps.connect(**config)
    cur = conn.cursor()
    sql = """
    SELECT DISTINCT img.photo_id,
    img.path, 
    img.title, 
    img.description, 
    CASE 
        WHEN img.title IS NULL OR img.title = '' THEN 'Title is empty' 
        ELSE 'Title is not empty' 
    END AS title_status,
    CASE 
        WHEN img.description IS NULL OR img.description = '' THEN 'Description is empty' 
        ELSE 'Description is not empty' 
    END AS description_status,
    CASE 
        WHEN pt.photo_id IS NULL THEN 'Tag is empty'
        ELSE 'Tag is not empty'
    END AS tag_status
    FROM images img
    LEFT JOIN phototag pt ON img.photo_id = pt.photo_id
    WHERE img.title IS NULL OR img.title = ''
    OR img.description IS NULL OR img.description = ''
    OR pt.photo_id IS NULL;
    """
    try:

        cur.execute(sql)
    except Exception as e:
        print(e)
    else:

    
        missresult = cur.fetchall()
    finally:
        cur.close()
    print(missresult)
    for i in allmissespath:
        print("connecting to phototag.ai for additional info ...")
        result = fetch_additional_info(i)
        print("completed ...")
        print("updating data ...")
        for j in missresult:
            if i == j[1]:
                if j[4] == 'Title is empty':
                    newtitle = result['data']['title']
                    updatetitlesql = f"""
                        UPDATE images SET title = '{newtitle}' WHERE path = '{i}';
                    """
                    try:
                        cur = conn.cursor()
                        cur.execute(updatetitlesql)
                    except Exception as e:
                        print(e)
                    else:
                        conn.commit()
                        print("title db for this item updated")
                    finally:
                        cur.close()
                if j[5] == 'Description is empty':
                    newdescription = result['data']['description']
                    updateDescriptionsql = f"""
                        UPDATE images SET description = '{newdescription}' WHERE path = '{i}';
                    """
                    try:
                        cur = conn.cursor()
                        cur.execute(updateDescriptionsql)
                    except Exception as e:
                        print(e)
                    else:
                        conn.commit()
                        print("Description db for this item updated")
                    finally:
                        cur.close()
                if j[6] == 'Tag is empty':
                    newtags = result['data']['keywords']
                    insert_tag_sql = """
                        INSERT INTO tags(tag_name) VALUES
                        (%s) RETURNING tag_id
                        """
                    select_tag_sql = """
                        SELECT tag_id FROM tags WHERE tag_name = %s;
                    """
                    #tag --------------------------
                    tag_ids = []
                    for t in newtags:
                        data = (t,)
                        if check_tagname(i) == False:
                            try:
                                cur = conn.cursor()
                                cur.execute(insert_tag_sql,data)
                            except Exception as e:
                                print(e)
                            else:
                                a = cur.fetchall()
                                tag_ids.append(a[0][0])
                                conn.commit()
                            finally:
                                cur.close()
                        else:
                            data = (i,)
                            try:
                                cur = conn.cursor()
                                cur.execute(select_tag_sql, data)
                            except Exception as e:
                                print(e)
                            else:
                                a = cur.fetchall()
                                tag_ids.append(a[0][0])
                            finally:
                                cur.close()
                    #phototag ---------------------
                    find_id_sql = f"""
                        SELECT photo_id FROM images WHERE path = '{i}'
                    """
                    try:
                        cur = conn.cursor()
                        cur.execute(find_id_sql)
                    except Exception as e:
                        print(e)
                    else:

                        this_id = cur.fetchall()
                    finally:
                        cur.close()
                    for tags in tag_ids:

                        phototag_sql = """
                            INSERT INTO phototag VALUES (%s,%s)
                        """
                        data = (this_id[0][0],tags)
                        try:
                            cur = conn.cursor()
                            cur.execute(phototag_sql,data)
                        except Exception as e:
                            print(e)
                        else:
                            conn.commit()
                            print("tag db for this item updated")
                        finally:
                            cur.close()
        
        
fill_db_missitems()



#a = fetch_additional_info(photo_path)
#with open('data.json', 'w') as file:
#    json.dump(a, file)
#result = fetch_not_complite_path()
