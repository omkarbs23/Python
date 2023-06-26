import pymysql as p

def universal_function(query, show=0):
    conn = p.connect(user="omkarbs23", password="MYsql_9029338161", host="omkarbs23.mysql.pythonanywhere-services.com", database="omkarbs23$chat_app")
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    if (show == 1):
        records = cur.fetchall()
        return records
    conn.close()
