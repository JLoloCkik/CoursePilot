import os, sqlite3, courses

DB = os.path.join(os.path.dirname(__file__), "..", "data", "courses.db")

os.makedirs(os.path.dirname(DB), exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
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

def save_to_db(course_list):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM courses")
    for course in course_list:
        c.execute(
            "INSERT INTO courses (name, category, length, link, status, progress) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (course.name, course.category, course.length,
             course.link, course.status, course.progress)
        )
    conn.commit()
    conn.close()

def load_from_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    results = []
    for row in c.execute("SELECT name,category,length,link,status,progress FROM courses"):
        course = courses.Course(row[0], row[1], row[2], row[3])
        course.status = row[4]
        course.progress = row[5]
        results.append(course)
    conn.close()
    return results
