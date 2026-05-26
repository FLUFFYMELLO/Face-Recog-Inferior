import sqlite3
from pathlib import Path

# Get absolute path of this file (data/database.py)
BASE_DIR = Path(__file__).resolve().parent

# Database file path (data/students.db)
DB_PATH = BASE_DIR / "students.db"


# Connect to database
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Initialize database
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            Student_Id TEXT PRIMARY KEY,
            Student_Name TEXT,
            Course TEXT,
            Year_level TEXT,
            Records TEXT,
            Image TEXT
        )
    """)

    conn.commit()
    conn.close()