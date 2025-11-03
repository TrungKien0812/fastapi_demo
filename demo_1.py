from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel


app = FastAPI(title="DEMO 1")

students = {
    1: {
        "name": "kien",
        "age": 20,
        "username": "kien.nguyenlovefamily",
        "year": "C22-KHM2"
    },
    2: {
        "name": "an",
        "age": 20,
        "username": "an.builovefamily",
        "year": "C23-KHM2"
    }
}

class Student(BaseModel):
    name: str
    age: int
    username: str
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    username: Optional[str] = None
    year: Optional[str] = None

@app.get("/")
def index():
    return {"name": "First Data"}


@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(..., description="The ID of the student you want to view", gt=0, lt=4)):
    return students[student_id]

#google.com/result?search=Python
@app.get("/get-by-name/{student_id}")
def get_student(*, student_id: int, name: Optional [str] = None, test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"DATA": "Not Found"}

@app.post("/creat-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student exists"}
    students[student_id]=student
    return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    if student.name != None:
        students[student_id].name = student.name
    if student.age != None:
        students[student_id].age = student.age
    if student.username != None:
        students[student_id].username = student.username
    if student.year != None:
        students[student_id].year = student.year
    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    del students[student_id]
    return {"Message": "Student deleted successfully!"}