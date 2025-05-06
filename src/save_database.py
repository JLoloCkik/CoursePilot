# save_database.py

import os
import sqlite3
from courses import Course

# Database file path
DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "courses.db"
)
# Ensure data folder exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
      CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        length REAL,
        link TEXT,
        status TEXT,
        progress REAL
      )
    """)
    conn.commit()
    conn.close()

def save_to_db(course_list: list):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM courses")
    for c in course_list:
        cur.execute("""
          INSERT INTO courses (name, category, length, link, status, progress)
          VALUES (?, ?, ?, ?, ?, ?)
        """, (c.name, c.category, c.length,
              c.link, c.status, c.progress))
    conn.commit()
    conn.close()

def load_from_db() -> list:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name,category,length,link,status,progress FROM courses")
    rows = cur.fetchall()
    conn.close()
    result = []
    for name, category, length, link, status, progress in rows:
        c = Course(name, category, length, link)
        c.update_status(status)
        c.progress = progress
        result.append(c)
    return result
