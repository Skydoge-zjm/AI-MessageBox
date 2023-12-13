from pymysql import Connection
import json
conn = Connection(
    host='localhost',
    port=3306,
    user='root',
    password='gc041009',
    autocommit=True
)
cursor = conn.cursor()
conn.select_db("new_database")
def create_table():
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS message (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            time DATETIME,
            place VARCHAR(255),
            participants VARCHAR(255),
            content JSON,
            link VARCHAR(255)
        )
        '''
    cursor.execute(create_table_query)
    conn.commit()
def insert_data(item):
    if type(item) != dict:
        item = eval(item)
    insert_query = '''
    INSERT INTO message (title,time,place,participants,content,link)
    VALUES (%s, %s, %s, %s, %s,%s)
    '''
    cursor.execute(insert_query, (item["title"], item["time"], item["site"], item["participants"], json.dumps(item["content"]), item["link"]))
    conn.commit()

def load_data():
    sql = "SELECT * FROM message ORDER BY STR_TO_DATE(time, '%Y-%m-%d') DESC"
    cursor.execute(sql)
    columns = [column[0] for column in cursor.description]

    # 处理每条数据并输出为字典形式
    results = []
    for row in cursor.fetchall():
        result = {}
        for i, value in enumerate(row):
            result[columns[i]] = value
        results.append(result)
    return results
