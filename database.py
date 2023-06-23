import pymysql

try:
    connection = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="pywinbd",
        cursorclass=pymysql.cursors.DictCursor
        )   
    print("successfully connected...")
    print("#" * 20)
except Exception as ex:
    print("Connection refused...")
    print(ex)
    

def req(request):    
    try:
        with connection.cursor() as cursor:
            cursor.execute(request)
            rows = cursor.fetchall()
            connection.commit()
            return rows
    except:
         rows = -1
