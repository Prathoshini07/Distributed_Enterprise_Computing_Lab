import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('sleep_tracker.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sleep_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE NOT NULL,
                sleep_time TEXT NOT NULL,
                wakeup_time TEXT NOT NULL,
                duration TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def calculate_duration(sleep_time, wakeup_time):
    sleep_dt = datetime.strptime(sleep_time, "%H:%M")
    wakeup_dt = datetime.strptime(wakeup_time, "%H:%M")
    if wakeup_dt < sleep_dt:
        wakeup_dt += timedelta(days=1)
    duration = wakeup_dt - sleep_dt
    return str(duration)

@app.route('/')
def index():
    conn = sqlite3.connect('sleep_tracker.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sleep_records ORDER BY date DESC")
    records = c.fetchall()
    conn.close()
    return render_template('index.html', records=records)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        date = request.form['date']
        sleep_time = request.form['sleep_time']
        wakeup_time = request.form['wakeup_time']
        duration = calculate_duration(sleep_time, wakeup_time)
        
        conn = sqlite3.connect('sleep_tracker.db')
        c = conn.cursor()
        c.execute("INSERT INTO sleep_records (date, sleep_time, wakeup_time, duration) VALUES (?, ?, ?, ?)",
                  (date, sleep_time, wakeup_time, duration))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('insert.html')

@app.route('/delete/<date>', methods=['GET', 'POST'])
def delete(date):
    if request.method == 'POST':
        conn = sqlite3.connect('sleep_tracker.db')
        c = conn.cursor()
        c.execute("DELETE FROM sleep_records WHERE date = ?", (date,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('delete.html', date=date)

@app.route('/edit/<date>', methods=['GET', 'POST'])
def edit(date):
    conn = sqlite3.connect('sleep_tracker.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sleep_records WHERE date = ?", (date,))
    record = c.fetchone()
    conn.close()
    
    if request.method == 'POST':
        sleep_time = request.form['sleep_time']
        wakeup_time = request.form['wakeup_time']
        duration = calculate_duration(sleep_time, wakeup_time)
        
        conn = sqlite3.connect('sleep_tracker.db')
        c = conn.cursor()
        c.execute("UPDATE sleep_records SET sleep_time = ?, wakeup_time = ?, duration = ? WHERE date = ?",
                  (sleep_time, wakeup_time, duration, date))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('edit.html', record=record)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
