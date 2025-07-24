from flask import Flask, render_template, request, redirect
import sqlite3
import datetime

app = Flask(__name__)

# DB 초기화 함수
def init_db():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user TEXT,
                    category TEXT,
                    amount INTEGER,
                    note TEXT,
                    date TEXT
                )''')
    conn.commit()
    conn.close()

# 메인 페이지
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = request.form['user']
        category = request.form['category']
        amount = request.form['amount']
        note = request.form['note']
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        conn = sqlite3.connect('budget.db')
        c = conn.cursor()
        c.execute("INSERT INTO expenses (user, category, amount, note, date) VALUES (?, ?, ?, ?, ?)",
                  (user, category, amount, note, date))
        conn.commit()
        conn.close()
        return redirect('/')

    # GET 요청 시, 전체 지출 내역 보여줌
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = c.fetchall()
    conn.close()
    return render_template('index.html', expenses=expenses)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
