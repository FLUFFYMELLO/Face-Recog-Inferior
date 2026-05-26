from fastapi import FastAPI
from backend.database import get_connection, init_db

app = FastAPI()

# Initialize DB on startup
init_db()


@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/students")
def get_students():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()

        students = [dict(row) for row in rows]

        conn.close()
        return students

    except Exception as e:
        return {"error": str(e)}


@app.get("/students/{student_id}")
def get_student(student_id: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students WHERE Student_Id = ?", (student_id,))
        row = cursor.fetchone()

        conn.close()

        if row:
            return dict(row)
        return {"error": "Student not found"}

    except Exception as e:
        return {"error": str(e)}


@app.get("/students/name/{student_name}")
def get_student_by_name(student_name: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM students 
            WHERE LOWER(Student_Name) = LOWER(?)
        """, (student_name,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return {"error": "Student not found"}

    except Exception as e:
        return {"error": str(e)}