import psycopg2 as ps
from config import load_config
#---------------------
config = load_config()
#---------------------










"""

sql = "SELECT * FROM users;"
cnn = ps.connect(**config)
cur = cnn.cursor()
cur.execute(sql)
a = cur.fetchall()
print(a)
"""