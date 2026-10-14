from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Student Management API",
    description="A practice REST API for managing students",
    version="1.0.0"
)


# -----------------------------
# Pydantic Models
# -----------------------------

class Student(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=5, le=100)
    course: str = Field(min_length=2, max_length=50)
    marks: float = Field(ge=0, le=100)


class StudentResponse(Student):
    id: int


# -----------------------------
# Temporary In-Memory Database
# -----------------------------

students = [
    {
        "id": 1,
        "name": "Shubham",
        "age": 22,
        "course": "Computer Science",
        "marks": 85
    },
    {
        "id": 2,
        "name": "Varun",
        "age": 21,
        "course": "Information Technology",
        "marks": 78
    }
]

# -----------------------------
# about
# -----------------------------
@app.get('/')
def home():
    return{ 'message': ' welcome to page '}
# -----------------------------
# Create Student
# -----------------------------

@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(student: Student):

    new_id = max(
        [existing_student["id"] for existing_student in students],
        default=0
    ) + 1

    new_student = {
        "id": new_id,
        **student.model_dump()
    }

    students.append(new_student)

    return new_student


# -----------------------------
# Get All Students
# -----------------------------

@app.get(
    "/students",
    response_model=list[StudentResponse]
)
def get_students(
    course: str | None = Query(
        default=None,
        description="Filter students by course"
    )
):
    if course:
        return [
            student
            for student in students
            if student["course"].lower() == course.lower()
        ]

    return students


# -----------------------------
# Get Student By ID
# -----------------------------

@app.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
def get_student(student_id: int):

    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


# -----------------------------
# Search Students
# -----------------------------

@app.get(
    "/students/search",
    response_model=list[StudentResponse]
)
def search_students(
    name: str = Query(
        min_length=2,
        description="Search student by name"
    )
):
    return [
        student
        for student in students
        if name.lower() in student["name"].lower()
    ]


# -----------------------------
# Update Student
# -----------------------------

@app.put(
    "/students/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student: Student
):

    for index, existing_student in enumerate(students):

        if existing_student["id"] == student_id:

            updated_student = {
                "id": student_id,
                **student.model_dump()
            }

            students[index] = updated_student

            return updated_student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


# -----------------------------
# Delete Student
# -----------------------------

@app.delete(
    "/students/{student_id}"
)
def delete_student(student_id: int):

    for index, student in enumerate(students):

        if student["id"] == student_id:

            students.pop(index)

            return {
                "message": "Student deleted successfully",
                "student_id": student_id
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )