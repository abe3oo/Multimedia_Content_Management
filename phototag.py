import csv
import psycopg2 as ps
from config import load_config, check_id, check_tagname
import requests
import json
lst1 = []
lst2 = []
config = load_config()

photo_path = "D:/backup windows 10/pic/Cosmos-flowers-lead.jpg"
api_token = "BQPZ-Vovn-L5TF-oH4i-NAZ"
api_url = "https://server.phototag.ai/api/keywords"

def fetch_not_complite_path():
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
    cur.execute(sql)
    result = cur.fetchall()
    for i in result:
        if i[1] not in allmissedpath:
            allmissedpath.append(i[1])
    cur.execute(sql2)
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
    allmissespath = fetch_not_complite_path()
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
    cur.execute(sql)
    missresult = cur.fetchall()
    print(missresult)
    for i in allmissespath:
        result = fetch_additional_info(i)
        for j in missresult:
            if i == j[1]:
                if j[4] == 'Title is empty':
                    pass
                if j[5] == 'Description is empty':
                    pass
                if j[6] == 'Tag is empty':
                    pass

        
fill_db_missitems()



#a = fetch_additional_info(photo_path)
#with open('data.json', 'w') as file:
#    json.dump(a, file)
#result = fetch_not_complite_path()
