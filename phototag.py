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
    allmissed = []
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
        if i[1] not in allmissed:
            allmissed.append(i[1])
    cur.execute(sql2)
    result2 = cur.fetchall()
    for i in result2:
        if i[0] not in allmissed:
            allmissed.append(i[0])
    return allmissed

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
        
a = fetch_additional_info(photo_path)
#with open('data.json', 'w') as file:
#    json.dump(a, file)
#result = fetch_not_complite_path()
print(a)