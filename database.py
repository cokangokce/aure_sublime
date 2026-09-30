import sqlite3

DB_NAME = "aurae_sublime.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            telefon TEXT NOT NULL,
            mesaj TEXT,
            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def lead_ekle(isim, telefon, mesaj=""):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)",
        (isim, telefon, mesaj)
    )
    conn.commit()
    conn.close()

def tum_leadleri_getir():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads ORDER BY tarih DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]