import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd = 'Kode0487^*'
    )

my_cursor = mydb.cursor()

my_cursor.execute('CREATE DATABASE mydb')

my_cursor.execute('SHOW DATABASES')
for db in my_cursor:
    print(db)
