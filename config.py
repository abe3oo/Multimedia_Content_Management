from configparser import ConfigParser
import psycopg2
def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config


def check_id(id):
    config = load_config()
    conn = psycopg2.connect(**config)
    cur = conn.cursor()
    sql = f"""
    SELECT * FROM person WHERE id = {id}
    """
    cur.execute(sql)
    result = cur.fetchall()
    if len(result)> 0:
        return True
    else:
        return False

def check_tagname(name):
    config = load_config()
    conn = psycopg2.connect(**config)
    cur = conn.cursor()
    sql = f"""
    SELECT tag_name FROM tags WHERE tag_name = {name};
    """
    cur.execute(sql)
    result = cur.fetchall()
    if len(result)> 0:
        return True
    else:
        return False
"""
if __name__ == '__main__':
    config = load_config()
    print(config)
    """