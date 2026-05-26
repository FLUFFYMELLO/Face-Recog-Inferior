import json
from database import get_connection

with open("../data/studentprofiles.json", "r") as f:
    students = json.load(f)

conn = get_connection()
cursor = conn.cursor()

for student in students:
    cursor.execute("""
    INSERT OR REPLACE INTO students VALUES (?, ?, ?, ?, ?, ?)
    """, (
        student["Student_Id"],
        student["Student_Name"],
        student["Course"],
        student["Year_level"],
        student["Records"],
        student["image"]
    ))

conn.commit()
conn.close()

print("Data inserted successfully!")