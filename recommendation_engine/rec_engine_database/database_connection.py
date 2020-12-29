#Same as Ethan's code in database.py 
#database.py is in the webapp directory

import sqlite3

def get_db_connection(filepath):
    conn = sqlite3.connect(filepath)
    conn.row_factory = sqlite3.Row
    return conn
