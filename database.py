import pymysql

connection = pymysql.connect(
    host='localhost',
    user='new_user',
    password='password',
    database='cpn_101'
)

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"Database version: {version}")
finally:
    connection.close()