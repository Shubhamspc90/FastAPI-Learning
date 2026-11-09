
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Product Management API",
    description="A practice REST API for managing products",
    version="1.0.0",
)


# -----------------------------
# Pydantic Models
# -----------------------------

class Product(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=300)
    price: float = Field(gt=0)
    category: str = Field(min_length=2, max_length=50)
    stock: int = Field(ge=0)


class ProductResponse(Product):
    id: int


# -----------------------------
# In-Memory Data Store
# -----------------------------

products: list[dict] = [
    {
        "id": 1,
        "name": "Laptop",
        "description": "Business laptop",
        "price": 55000.0,
        "category": "Electronics",
        "stock": 10,
    },
    {
        "id": 2,
        "name": "Mouse",
        "description": "Wireless mouse",
        "price": 800.0,
        "category": "Accessories",
        "stock": 25,
    },
]


# -----------------------------
# Create Product
# -----------------------------

@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(product: Product):
    new_id = max(
        (existing["id"] for existing in products),
        default=0,
    ) + 1

    new_product = {
        "id": new_id,
        **product.model_dump(),
    }

    products.append(new_product)
    return new_product


# -----------------------------
# Get All Products / Filter
# -----------------------------

@app.get("/products", response_model=list[ProductResponse])
def get_products(
    category: str | None = Query(default=None),
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, gt=0),
):
    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_price cannot be greater than max_price",
        )

    result = products

    if category:
        result = [
            product for product in result
            if product["category"].lower() == category.lower()
        ]

    if min_price is not None:
        result = [
            product for product in result
            if product["price"] >= min_price
        ]

    if max_price is not None:
        result = [
            product for product in result
            if product["price"] <= max_price
        ]

    return result


# -----------------------------
# Search Products by Name
# -----------------------------

@app.get("/products/search", response_model=list[ProductResponse])
def search_products(
    name: str = Query(min_length=2, description="Product name to search"),
):
    return [
        product for product in products
        if name.lower() in product["name"].lower()
    ]


# -----------------------------
# Get Product by ID
# -----------------------------

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found",
    )


# -----------------------------
# Update Product
# -----------------------------

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: Product):
    for index, existing_product in enumerate(products):
        if existing_product["id"] == product_id:
            updated_product = {
                "id": product_id,
                **product.model_dump(),
            }

            products[index] = updated_product
            return updated_product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found",
    )


# -----------------------------
# Delete Product
# -----------------------------

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            products.pop(index)

            return {
                "message": "Product deleted successfully",
                "product_id": product_id,
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found",
    )
