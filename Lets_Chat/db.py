import pymysql as p

def universal_function(query, show=0):
    conn = p.connect(user="your__username", password="your__password", host="your__host", database="your__dbname")
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    if (show == 1):
        records = cur.fetchall()
        return records
    conn.close()
