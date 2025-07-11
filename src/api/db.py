import sqlite3

def init_db():
    conn = sqlite3.connect("logs.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        question TEXT,
        answer TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

def insert_log(user_id, question, answer):
    conn = sqlite3.connect("logs.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO logs (user_id, question, answer) VALUES (?, ?, ?)", (user_id, question, answer))
    conn.commit()
    conn.close()

def get_logs_for_user(user_id):
    conn = sqlite3.connect("logs.db")
    cur = conn.cursor()
    cur.execute("SELECT question, answer, timestamp FROM logs WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows