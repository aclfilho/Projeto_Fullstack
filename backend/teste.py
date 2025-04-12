import pymysql

try:
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="040115",
        database="teste_intuitive",
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Conectado ao banco de dados!")
except pymysql.MySQLError as e:
    print(f"Erro ao conectar: {e}")
