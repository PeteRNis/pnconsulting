import mysql.connector

newdb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd = 'Kode0487'
    )

my_cursor = newdb.cursor()

#my_cursor.execute('CREATE DATABASE newusers')

my_cursor.execute('SHOW DATABASES')
for db in my_cursor:
    print(db)
