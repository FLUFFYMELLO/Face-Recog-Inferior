from fastapi import FastAPI
from pathlib import Path
import json

app = FastAPI()

DATA_FILE = Path("data/studentprofiles.json")

# Load JSON once at startup
def load_students():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

@app.get("/students")
def get_students():
    """Return all student profiles"""
    return load_students()

@app.get("/students/{student_id}")
def get_student(student_id: str):
    """Return a single student by ID"""
    students = load_students()
    for student in students:
        if student["Student_Id"] == student_id:
            return student
    return {"error": "Student not found"}

@app.get("/students/name/{student_name}")
def get_student_by_name(student_name: str):
    """Search student by name"""
    students = load_students()
    for student in students:
        if student["Student_Name"].lower() == student_name.lower():
            return student
    return {"error": "Student not found"}
