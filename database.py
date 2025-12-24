import sqlite3
from config import DB_NAME

def connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            year TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_book(title, author, year):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
    conn.commit()
    conn.close()

def fetch_books():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    data = cursor.fetchall()
    conn.close()
    return data

def search_books(keyword):
    conn = connection()
    cursor = conn.cursor()
    # Gunakan LOWER agar tidak sensitif huruf besar/kecil
    query = "SELECT * FROM books WHERE LOWER(title) LIKE LOWER(?) OR LOWER(author) LIKE LOWER(?)"
    cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
    data = cursor.fetchall()
    conn.close()
    return data

def delete_book(book_id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()