import sqlite3, os
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
def index():
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        flag = request.form['flag']
        file = request.files.get('file')
        
        filename = ''
        if file and file.filename != '':
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO challenges (title, content, filename, flag) VALUES (?, ?, ?, ?)',
                  (title, content, filename, flag))
        conn.commit()
        conn.close()
        
        return redirect(url_for('problem_list'))
    return render_template('register.html')

@app.route('/solve/<int:problem_id>', methods=['GET', 'POST'])
def solve(problem_id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM challenges WHERE id = ?', (problem_id,))
    problem = c.fetchone()
    conn.close()

    if request.method == 'POST':
        data = request.get_json()
        user_flag = data.get('flag')

        if user_flag == problem['flag']:
            return jsonify({'success': True, 'message': 'Correct Flag! 🎉'})
        else:
            return jsonify({'success': False, 'message': 'Wrong Flag. Try Again! 😭'})

    return render_template('solve.html', problem=problem)

def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    host_addr = os.getenv('FLASK_HOST', '127.0.0.1')
    app.run(host=host_addr, port=5000)