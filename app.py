import sqlite3
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

DATABASE = 'destinations.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    
    # Fetch destinations and their reviews
    cur.execute('''
    SELECT d.id, d.destination_name, d.description, d.image_url, d.score, 
           GROUP_CONCAT(r.review, '|') AS reviews
    FROM destinations_list d
    LEFT JOIN reviews r ON d.id = r.destination_id
    GROUP BY d.id
    ''')
    destinations = cur.fetchall()
    conn.close()
    return render_template('index.html', destinations=destinations)


@app.route('/add_destination', methods=['GET', 'POST'])
def add_destination():
    if request.method == 'POST':
        destination_name = request.form['destination_name']
        description = request.form['description']
        image_url = request.form['image_url']
        reviews = request.form['reviews']
        score = request.form['score']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO destinations_list (destination_name, description, image_url, reviews, score)
            VALUES (?, ?, ?, ?, ?)
        ''', (destination_name, description, image_url, reviews, score))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('add_destination.html')

@app.route('/delete_destination/<int:id>')
def delete_destination(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM destinations_list WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/edit_destination/<int:id>', methods=['GET', 'POST'])
def edit_destination(id):
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        destination_name = request.form['destination_name']
        description = request.form['description']
        image_url = request.form['image_url']
        reviews = request.form['reviews']
        score = request.form['score']
        
        cursor.execute('''
            UPDATE destinations_list
            SET destination_name = ?, description = ?, image_url = ?, reviews = ?, score = ?
            WHERE id = ?
        ''', (destination_name, description, image_url, reviews, score, id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    cursor.execute('SELECT * FROM destinations_list WHERE id = ?', (id,))
    destination = cursor.fetchone()
    conn.close()
    
    return render_template('edit_destination.html', destination=destination)

@app.route('/add_review/<int:destination_id>', methods=['GET', 'POST'])
def add_review(destination_id):
    conn = get_db()
    cur = conn.cursor()
    
    # Fetch the destination name
    cur.execute('SELECT destination_name FROM destinations_list WHERE id = ?', (destination_id,))
    destination = cur.fetchone()
    
    if request.method == 'POST':
        review = request.form['review']
        
        cur.execute('INSERT INTO reviews (destination_id, review) VALUES (?, ?)', 
                    (destination_id, review))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('add_review.html', destination_id=destination_id, destination_name=destination['destination_name'])


if __name__ == '__main__':
    app.run(debug=True)
