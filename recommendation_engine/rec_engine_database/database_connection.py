import sqlite3

def database_connection(filepath):
    conn = sqlite3.connect(filepath)
    conn.row_factory = sqlite3.Row
    return conn