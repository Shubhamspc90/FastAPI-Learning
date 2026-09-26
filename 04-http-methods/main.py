from fastapi import FastAPI

app = FastAPI()


# GET - Retrieve data
@app.get("/users")
def get_users():
    return {
        "message": "Fetching users",
        "users": ["Shubham", "Rahul", "Amit"]
    }


# POST - Create data
@app.post("/users")
def create_user():
    return {
        "message": "User created successfully"
    }


# PUT - Update complete data
@app.put("/users/{user_id}")
def update_user(user_id: int):
    return {
        "message": "User updated successfully",
        "user_id": user_id
    }


# PATCH - Partially update data
@app.patch("/users/{user_id}")
def partial_update_user(user_id: int):
    return {
        "message": "User partially updated",
        "user_id": user_id
    }


# DELETE - Delete data
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    return {
        "message": "User deleted successfully",
        "user_id": user_id
    }