import sqlite3

connection = sqlite3.connect('user_content_data.db')

with open(r'C:/Users/Vikram/rec_database_schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()