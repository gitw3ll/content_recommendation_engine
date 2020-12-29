import sqlite3


conn = sqlite3.connect('user_content_data.db')

conn.executescript('''DROP TABLE IF EXISTS user_data''')

conn.executescript('''DROP TABLE IF EXISTS content_data''')

conn.executescript('''CREATE TABLE user_data (person_id int, content_id int, title text)''')

conn.executescript('''CREATE TABLE content_data (content_id int, title text)''')


with open('../database_schema.sql', 'w') as f:
    for line in conn.iterdump():
       f.write('%s\n' % line)
        
        
        
#f = open('../database_schema.sql')
#conn.executescript(f.read())

#conn.close()