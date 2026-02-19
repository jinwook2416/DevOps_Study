import sqlite3, os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 함수는 한 번만 정의하면 됩니다
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS challenges 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  title TEXT, content TEXT, filename TEXT, flag TEXT)''')
    conn.commit()
    conn.close()

init_db() # 실행도 한 번만!

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
        file = request.files['file']
        
        filename = ''
        if file:
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)