# src/save_database.py

import os
import sqlite3
import json
from datetime import datetime
from courses import Course # Assuming courses.py is in the same directory or PYTHONPATH

# --- Constants ---
# Determine the base directory (src) and data directory (../data)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

# Define full paths for database and JSON files
DB_PATH = os.path.join(DATA_DIR, "courses.db")
ROADMAP_JSON_PATH = os.path.join(DATA_DIR, "roadmap_data.json")

# Ensure the data directory exists before proceeding
os.makedirs(DATA_DIR, exist_ok=True)

# --- Database Initialization ---

def init_db():
    """
    Initializes the database by connecting and ensuring all necessary tables
    (courses, expenses, weekly_goals) exist with the correct schema.
    Uses 'CREATE TABLE IF NOT EXISTS' for idempotency.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create 'courses' table
        cursor.execute("""
          CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL, -- Course name must be unique
            category TEXT,
            length REAL DEFAULT 0.0,   -- Default length to 0.0
            link TEXT,
            status TEXT DEFAULT 'Pending', -- Default status
            progress REAL DEFAULT 0.0,     -- Default progress
            due_date TEXT,                 -- Format: YYYY-MM-DD or NULL
            priority TEXT DEFAULT 'Medium',-- Default priority
            last_progress_update_date TEXT -- Format: YYYY-MM-DD or NULL
          )
        """)

        # Create 'expenses' table
        cursor.execute("""
          CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- Use AUTOINCREMENT for expenses
            course_name TEXT,
            price REAL NOT NULL, -- Price should not be null
            purchase_date TEXT NOT NULL -- Date should not be null
          )
        """)

        # Create 'weekly_goals' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weekly_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week_start_date TEXT UNIQUE NOT NULL, -- Week identifier (e.g., YYYY-MM-DD of Monday)
                goal_hours REAL NOT NULL             -- Goal hours for that week
            )
        """)

        conn.commit()
        print(f"Database initialized successfully at {DB_PATH}")

    except sqlite3.Error as e:
        print(f"Database Error during initialization: {e}")
    finally:
        if conn:
            conn.close()

# --- Course Data Operations ---

def save_to_db(course_list: list[Course]):
    """
    Saves the entire list of Course objects to the database.
    Uses INSERT OR REPLACE to update existing courses (based on unique name)
    or insert new ones.
    Args:
        course_list: A list of Course objects.
    """
    if not course_list: # Don't do anything if the list is empty
        return

    sql = """
        INSERT OR REPLACE INTO courses
        (name, category, length, link, status, progress, due_date, priority, last_progress_update_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    data_to_save = [
        (c.name, c.category, c.length, c.link, c.status, c.progress,
         c.due_date, c.priority, c.last_progress_update_date)
        for c in course_list
    ]

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.executemany(sql, data_to_save)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database Error during save_to_db: {e}")
    finally:
        if conn:
            conn.close()

def load_from_db() -> list[Course]:
    """
    Loads all courses from the database and returns them as a list of Course objects.
    Returns:
        A list of Course objects, or an empty list if an error occurs or no courses exist.
    """
    sql = "SELECT name, category, length, link, status, progress, due_date, priority, last_progress_update_date FROM courses"
    results = []
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        for name, category, length, link, status, progress, due_date, priority, last_update in rows:
            # Create Course object directly with loaded data
            course = Course(
                name=name,
                category=category,
                length=float(length) if length is not None else 0.0,
                link=link if link else "",
                due_date=due_date,
                priority=priority if priority else "Medium"
            )
            # Set status and progress after creation to avoid triggering update logic unnecessarily
            course.status = status if status else "Pending"
            course.progress = float(progress) if progress is not None else 0.0
            course.last_progress_update_date = last_update
            results.append(course)
    except sqlite3.Error as e:
        print(f"Database Error during load_from_db: {e}")
    finally:
        if conn:
            conn.close()
    return results

def populate_db_from_json_if_empty():
    """
    Populates the 'courses' table from the roadmap JSON file,
    but only if the 'courses' table is currently empty.
    Sets default status to 'Pending' and progress to 0.0.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM courses")
        count = cursor.fetchone()[0]

        if count == 0:
            print("Courses table is empty, attempting to populate from JSON...")
            try:
                with open(ROADMAP_JSON_PATH, 'r', encoding='utf-8') as f:
                    roadmap_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Warning: Could not load or parse {ROADMAP_JSON_PATH}. Error: {e}")
                return # Exit if JSON cannot be loaded/parsed

            courses_to_add = []
            for section in roadmap_data.get('sections', []):
                category = section.get('title', 'Uncategorized') # Default category
                for course_data in section.get('courses', []):
                    name = course_data.get('name')
                    if not name: continue # Skip courses without a name

                    hours_str = str(course_data.get('hours', "0"))
                    length = 0.0
                    try:
                        # Attempt to extract the first number found
                        cleaned_hours_str = ''.join(filter(lambda x: x.isdigit() or x == '.', hours_str.split('-')[0].replace('h','').replace('~','').strip()))
                        if cleaned_hours_str:
                            length = float(cleaned_hours_str)
                    except ValueError:
                        length = 0.0 # Default to 0 if conversion fails

                    # Add tuple for executemany (matching table columns order in save_to_db)
                    courses_to_add.append(
                        (name, category, length, "", "Pending", 0.0, None, "Medium", None)
                    )

            if courses_to_add:
                sql_insert = """
                    INSERT OR IGNORE INTO courses
                    (name, category, length, link, status, progress, due_date, priority, last_progress_update_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor.executemany(sql_insert, courses_to_add)
                conn.commit()
                print(f"Populated {len(courses_to_add)} courses from JSON.")
            else:
                print("No valid courses found in JSON to populate.")
        else:
            print(f"Courses table already has {count} entries. Skipping JSON population.")

    except sqlite3.Error as e:
        print(f"Database Error during populate_db_from_json_if_empty: {e}")
    finally:
        if conn:
            conn.close()

# --- Expense Data Operations ---

def add_expense(course_name: str, price: float, purchase_date: str):
    """Adds a new expense record to the database."""
    sql = "INSERT INTO expenses (course_name, price, purchase_date) VALUES (?, ?, ?)"
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql, (course_name, price, purchase_date))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database Error during add_expense: {e}")
    finally:
        if conn:
            conn.close()

def load_expenses() -> list[dict]:
    """Loads all expense records from the database, ordered by date descending."""
    sql = "SELECT id, course_name, price, purchase_date FROM expenses ORDER BY purchase_date DESC"
    results = []
    try:
        conn = sqlite3.connect(DB_PATH)
        # Use dictionary row factory for easier access
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        # Convert Row objects to dictionaries
        results = [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f"Database Error during load_expenses: {e}")
    finally:
        if conn:
            conn.close()
    return results

def get_total_spent() -> float:
    """Calculates the sum of all prices in the expenses table."""
    sql = "SELECT SUM(price) FROM expenses"
    total = 0.0
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        total = result if result is not None else 0.0
    except sqlite3.Error as e:
        print(f"Database Error during get_total_spent: {e}")
    finally:
        if conn:
            conn.close()
    return total

# --- Weekly Goal Operations ---

def save_weekly_goal(week_start_date_str: str, goal_hours: float):
    """Saves or updates the weekly goal hours for a specific week."""
    sql = "INSERT OR REPLACE INTO weekly_goals (week_start_date, goal_hours) VALUES (?, ?)"
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql, (week_start_date_str, goal_hours))
        conn.commit()
        print(f"Saved weekly goal: {goal_hours} for week starting {week_start_date_str}")
    except sqlite3.Error as e:
        print(f"Database Error during save_weekly_goal: {e}")
    finally:
        if conn:
            conn.close()

def load_weekly_goal(week_start_date_str: str) -> float | None:
    """Loads the weekly goal hours for a specific week."""
    sql = "SELECT goal_hours FROM weekly_goals WHERE week_start_date = ?"
    result = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql, (week_start_date_str,))
        row = cursor.fetchone()
        result = row[0] if row else None
    except sqlite3.Error as e:
        # If the table doesn't exist yet (e.g., first run after schema change), return None
        if "no such table" not in str(e):
             print(f"Database Error during load_weekly_goal: {e}")
        result = None # Ensure None is returned on error
    finally:
        if conn:
            conn.close()
    return result
