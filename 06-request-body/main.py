from fastapi import FastAPI

app = FastAPI()


@app.post("/users")
def create_user(user: dict):
    return {
        "message": "User created successfully",
        "user": user
    }


@app.post("/products")
def create_product(product: dict):
    return {
        "message": "Product created successfully",
        "product": product
    }


@app.put("/users/{user_id}")
def update_user(user_id: int, user: dict):
    return {
        "message": "User updated successfully",
        "user_id": user_id,
        "user": user
    }