import sqlite3

def get_db_connection(filepath: str):
    conn = sqlite3.connect(filepath)
    conn.row_factory = sqlite3.Row
    return conn