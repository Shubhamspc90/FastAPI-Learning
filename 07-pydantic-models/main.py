from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


# Pydantic Model
class User(BaseModel):
    name: str
    age: int
    city: str


@app.post("/users")
def create_user(user: User):
    return {
        "message": "User created successfully",
        "user": user
    }


# Model with default value
class Product(BaseModel):
    name: str
    price: float
    category: str
    in_stock: bool = True


@app.post("/products")
def create_product(product: Product):
    return {
        "message": "Product created successfully",
        "product": product
    }


# Model with validation
class Student(BaseModel):
    name: str
    age: int = Field(ge=5, le=100)
    marks: float = Field(ge=0, le=100)


@app.post("/students")
def create_student(student: Student):
    return {
        "message": "Student created successfully",
        "student": student
    }