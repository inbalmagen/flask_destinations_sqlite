import sqlite3

conn = sqlite3.connect('destinations.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS destinations_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_name TEXT UNIQUE NOT NULL,
    description TEXT NOT NULL,
    image_url TEXT,
    reviews TEXT,
    score REAL
)
''')

conn.commit()
conn.close()
