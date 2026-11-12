
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field


app = FastAPI(
    title="Book Management API",
    description="A practice REST API for managing library books",
    version="1.0.0",
)


class BookCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    author: str = Field(min_length=2, max_length=100)
    genre: str = Field(min_length=2, max_length=50)
    publication_year: int = Field(ge=1000, le=2026)
    is_available: bool = True


class BookUpdate(BookCreate):
    pass


class BookAvailabilityUpdate(BaseModel):
    is_available: bool


class BookResponse(BookCreate):
    id: int


books: list[dict] = [
    {
        "id": 1,
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "genre": "Fiction",
        "publication_year": 1988,
        "is_available": True,
    },
    {
        "id": 2,
        "title": "Wings of Fire",
        "author": "A. P. J. Abdul Kalam",
        "genre": "Autobiography",
        "publication_year": 1999,
        "is_available": True,
    },
    {
        "id": 3,
        "title": "1984",
        "author": "George Orwell",
        "genre": "Dystopian",
        "publication_year": 1949,
        "is_available": False,
    },
]


@app.post(
    "/books",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_book(book: BookCreate):
    new_id = max(
        (existing["id"] for existing in books),
        default=0,
    ) + 1

    new_book = {
        "id": new_id,
        **book.model_dump(),
    }

    books.append(new_book)
    return new_book


# Keep fixed routes such as /search and /available
# before the dynamic /{book_id} route.
@app.get("/books/search", response_model=list[BookResponse])
def search_books(
    title: str | None = Query(default=None, min_length=2),
    author: str | None = Query(default=None, min_length=2),
):
    if title is None and author is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide at least a title or author to search",
        )

    result = books

    if title is not None:
        result = [
            book for book in result
            if title.lower() in book["title"].lower()
        ]

    if author is not None:
        result = [
            book for book in result
            if author.lower() in book["author"].lower()
        ]

    return result


@app.get("/books/available", response_model=list[BookResponse])
def get_available_books():
    return [
        book for book in books
        if book["is_available"] is True
    ]


@app.get("/books", response_model=list[BookResponse])
def get_books(
    genre: str | None = Query(default=None, min_length=2),
    is_available: bool | None = Query(default=None),
):
    result = books

    if genre is not None:
        result = [
            book for book in result
            if book["genre"].lower() == genre.lower()
        ]

    if is_available is not None:
        result = [
            book for book in result
            if book["is_available"] == is_available
        ]

    return result


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found",
    )


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, updated_book: BookUpdate):
    for index, existing_book in enumerate(books):
        if existing_book["id"] == book_id:
            new_book = {
                "id": book_id,
                **updated_book.model_dump(),
            }

            books[index] = new_book
            return new_book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found",
    )


@app.patch(
    "/books/{book_id}/availability",
    response_model=BookResponse,
)
def update_book_availability(
    book_id: int,
    availability: BookAvailabilityUpdate,
):
    for book in books:
        if book["id"] == book_id:
            book["is_available"] = availability.is_available
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found",
    )


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(index)

            return {
                "message": "Book deleted successfully",
                "book_id": book_id,
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found",
    )



# cd 10-practice-projects\06-book-management
# uvicorn main:app --reload