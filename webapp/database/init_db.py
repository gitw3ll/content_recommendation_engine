# Run this file to initialize the database
# Running this with an existing database will DELETE ALL existing content

import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()