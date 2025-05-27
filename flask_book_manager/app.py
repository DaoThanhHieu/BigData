from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from config import config

app = Flask(__name__)

def get_connection_and_table(db):
    if db not in config:
        return None, None
    conf = config[db]
    conn = mysql.connector.connect(
        host=conf['host'],
        user=conf['user'],
        password=conf['password'],
        database=conf['database']
    )
    return conn, conf['table']

@app.route('/')
def home():
    return render_template('index.html', books=[], columns=[], db=None)

@app.route('/books/<db>')
def list_books(db):
    conn, table = get_connection_and_table(db)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    books = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return render_template('index.html', books=books, columns=columns, db=db)

@app.route('/add/<db>', methods=['GET', 'POST'])
def add_book(db):
    if request.method == 'POST':
        title = request.form['title']
        price = float(request.form['price'])
        rating = float(request.form['rating'])
        url = request.form['url']
        conn, table = get_connection_and_table(db)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {table} (title, price, rating, url) VALUES (%s, %s, %s, %s)",
                       (title, price, rating, url))
        conn.commit()
        return redirect(url_for('list_books', db=db))
    return render_template('form.html', db=db, action='Add', book=None)

@app.route('/edit/<db>/<int:book_id>', methods=['GET', 'POST'])
def edit_book(db, book_id):
    conn, table = get_connection_and_table(db)
    cursor = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        price = float(request.form['price'])
        rating = float(request.form['rating'])
        url = request.form['url']
        cursor.execute(f"UPDATE {table} SET title=%s, price=%s, rating=%s, url=%s WHERE id=%s",
                       (title, price, rating, url, book_id))
        conn.commit()
        return redirect(url_for('list_books', db=db))
    cursor.execute(f"SELECT * FROM {table} WHERE id=%s", (book_id,))
    book = cursor.fetchone()
    return render_template('form.html', db=db, action='Edit', book=book)

@app.route('/delete/<db>/<int:book_id>')
def delete_book(db, book_id):
    conn, table = get_connection_and_table(db)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE id=%s", (book_id,))
    conn.commit()
    return redirect(url_for('list_books', db=db))

@app.route('/query/<db>', methods=['GET', 'POST'])
def query(db):
    conn, table = get_connection_and_table(db)
    result = None
    headers = None
    error = None
    if request.method == 'POST':
        sql = request.form['query']
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            if sql.strip().lower().startswith("select"):
                result = cursor.fetchall()
                headers = [desc[0] for desc in cursor.description]
            else:
                conn.commit()
                result = f"{cursor.rowcount} row(s) affected."
        except Exception as e:
            error = str(e)
    return render_template('query.html', db=db, result=result, headers=headers, error=error)

if __name__ == '__main__':
    app.run(debug=True)
