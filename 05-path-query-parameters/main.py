from fastapi import FastAPI, Query

app = FastAPI()


# -------------------------
# Path Parameter
# -------------------------

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "message": "User found",
        "user_id": user_id
    }


# Multiple Path Parameters
@app.get("/users/{user_id}/posts/{post_id}")
def get_user_post(user_id: int, post_id: int):
    return {
        "user_id": user_id,
        "post_id": post_id
    }


# -------------------------
# Query Parameter
# -------------------------

@app.get("/products")
def get_products(limit: int = 10):
    return {
        "limit": limit,
        "message": "Products fetched"
    }


# Optional Query Parameter
@app.get("/search")
def search_products(
    keyword: str | None = None,
    limit: int = 10
):
    return {
        "keyword": keyword,
        "limit": limit
    }


# Query Parameter with Validation
@app.get("/items")
def get_items(
    limit: int = Query(10, ge=1, le=100)
):
    return {
        "limit": limit
    }