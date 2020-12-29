#Same as Ethan's code in init_db.py
#Same notice; running this with existing database will erase the existing database

import sqlite3

connection = sqlite3.connect('user_content_data.db')

with open('../rec_database_schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()
