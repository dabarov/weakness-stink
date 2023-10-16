import sqlite3

open("db.sql", "w").close()

connection = sqlite3.connect("db.sql")
db_cursor = connection.cursor()

with open("init.sql", "r") as init_sql_file:
    init_query = init_sql_file.read()
    db_cursor.execute(init_query)
    connection.commit()

db_cursor.close()
connection.close()
