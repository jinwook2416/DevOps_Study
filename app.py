import sqlite3
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS challenges 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  title TEXT, content TEXT, filename TEXT, flag TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/list')
def problem_list():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row 
    c = conn.cursor()
    c.execute('SELECT * FROM challenges')
    problems = c.fetchall()
    conn.close()
    return render_template('list.html', problems=problems)  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)