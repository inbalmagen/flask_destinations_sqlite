import sqlite3

# Connect to the database
conn = sqlite3.connect('destinations.db')
c = conn.cursor()

# Create the reviews table
c.execute('''
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_id INTEGER,
    review TEXT NOT NULL,
    FOREIGN KEY(destination_id) REFERENCES destinations(id)
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
