from fastapi import FastAPI, HTTPException, status

app = FastAPI()


# Basic HTTPException
@app.get("/users/{user_id}")
def get_user(user_id: int):

    if user_id != 1:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": 1,
        "name": "Shubham"
    }


# Using status constants
@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    if user_id != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )

    return {
        "message": "User deleted successfully"
    }


# Custom error response
@app.get("/products/{product_id}")
def get_product(product_id: int):

    if product_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product ID must be greater than 0"
        )

    if product_id != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Product not found",
                "product_id": product_id
            }
        )

    return {
        "id": 1,
        "name": "Laptop",
        "price": 55000
    }


# Authorization example
@app.get("/admin")
def admin_panel(is_admin: bool = False):

    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return {
        "message": "Welcome to admin panel Shubham Chauhan" 
    }