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
        CREATE TABLE IF NOT EXISTS kullanici_kayitlari (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            email TEXT NOT NULL,
            telefon TEXT,
            deneyim TEXT
        )
    ''')
    conn.commit()
    conn.close()

def kayit_ekle(isim, email, telefon="", deneyim=""):
    conn = get_db()
    cursor = conn.cursor()
    
    # Tablo yoksa oluşturulmasını garanti edelim
    init_db()
    
    cursor.execute(
        "INSERT INTO kullanici_kayitlari (isim, email, telefon, deneyim) VALUES (?, ?, ?, ?)",
        (isim, email, telefon, deneyim)
    )
    conn.commit()
    conn.close()

def tum_kayitlari_getir():
    conn = get_db()
    cursor = conn.cursor()
    
    init_db()
    
    cursor.execute("SELECT id, isim, email, telefon, deneyim FROM kullanici_kayitlari ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    kayitlar = []
    for row in rows:
        kayitlar.append({
            "_id": str(row["id"]),  # Wix Repeater için gerekli benzersiz ID
            "isim": row["isim"],
            "email": row["email"],
            "telefon": row["telefon"],
            "deneyim": row["deneyim"]
        })
    return kayitlar