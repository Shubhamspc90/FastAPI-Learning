from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Response Model
class UserResponse(BaseModel):
    id: int
    name: str
    email: str


@app.get("/user", response_model=UserResponse)
def get_user():
    return {
        "id": 1,
        "name": "Shubham",
        "email": "shubham@example.com"
    }


# Response model filters unwanted fields
@app.get("/profile", response_model=UserResponse)
def get_profile():
    return {
        "id": 2,
        "name": "Rahul",
        "email": "rahul@example.com",
        "password": "secret123",
        "internal_id": 999
    }


# List Response Model
class ProductResponse(BaseModel):
    id: int
    name: str
    price: float


@app.get("/products", response_model=list[ProductResponse])
def get_products():
    return [
        {
            "id": 1,
            "name": "Laptop",
            "price": 55000
        },
        {
            "id": 2,
            "name": "Mouse",
            "price": 800
        }
    ]