# FastAPI Practice Projects 🚀

This section contains practice projects designed to apply the FastAPI concepts learned throughout this repository.

The projects gradually increase in complexity and help build practical REST API development skills.

---

# Project 1: Student Management API 🎓

## Objective

Build a REST API to manage student records.

## Features

* Add a new student
* Get all students
* Get a student by ID
* Search students
* Update student information
* Delete a student
* Validate student data
* Handle invalid student IDs
* Return structured API responses

## Example Student

```json
{
    "name": "Shubham",
    "age": 22,
    "course": "Computer Science",
    "marks": 85
}
```

## Possible Endpoints

```text
POST   /students
GET    /students
GET    /students/{student_id}
GET    /students/search
PUT    /students/{student_id}
DELETE /students/{student_id}
```

## FastAPI Concepts Used

* GET
* POST
* PUT
* DELETE
* Path Parameters
* Query Parameters
* Request Body
* Pydantic Models
* Response Models
* HTTPException
* Request Validation
* Response Validation

---

# Project 2: Product Management API 🛒

## Objective

Build an API to manage products in an online store.

## Features

* Add products
* Get all products
* Get product by ID
* Search products
* Filter products
* Update products
* Delete products
* Validate product price
* Validate stock quantity
* Handle product-not-found errors

## Example Product

```json
{
    "name": "Laptop",
    "price": 55000,
    "category": "Electronics",
    "stock": 10
}
```

## Possible Endpoints

```text
POST   /products
GET    /products
GET    /products/{product_id}
GET    /products/search
PUT    /products/{product_id}
DELETE /products/{product_id}
```

## FastAPI Concepts Used

* HTTP Methods
* Path Parameters
* Query Parameters
* Request Body
* Pydantic Models
* Response Models
* Request Validation
* HTTPException
* Status Codes

---

# Project 3: Task Management API ✅

## Objective

Build an API to create and manage daily tasks.

## Features

* Create a task
* Get all tasks
* Get task by ID
* Update a task
* Delete a task
* Mark task as completed
* Filter tasks by status
* Handle invalid task IDs

## Example Task

```json
{
    "title": "Learn FastAPI",
    "description": "Complete FastAPI practice",
    "status": "pending"
}
```

## Possible Endpoints

```text
POST   /tasks
GET    /tasks
GET    /tasks/{task_id}
GET    /tasks?status=pending
PUT    /tasks/{task_id}
DELETE /tasks/{task_id}
```

## FastAPI Concepts Used

* CRUD Operations
* HTTP Methods
* Path Parameters
* Query Parameters
* Request Body
* Pydantic Models
* Response Models
* Validation
* HTTPException
* Status Codes

---

# Project 4: Employee Management API 👨‍💼

## Objective

Build an API to manage employee information.

## Features

* Add employees
* Get all employees
* Get employee by ID
* Search employees
* Filter employees by department
* Update employee information
* Delete employees
* Validate employee data
* Handle employee-not-found errors

## Example Employee

```json
{
    "name": "Rahul",
    "age": 25,
    "department": "IT",
    "salary": 50000
}
```

## Possible Endpoints

```text
POST   /employees
GET    /employees
GET    /employees/{employee_id}
GET    /employees/search
GET    /employees?department=IT
PUT    /employees/{employee_id}
DELETE /employees/{employee_id}
```

## FastAPI Concepts Used

* REST API
* CRUD Operations
* Path Parameters
* Query Parameters
* Request Body
* Pydantic Models
* Response Models
* Request Validation
* HTTPException
* Status Codes

---

# Project 5: Student Attendance API 📋

## Objective

Build an API to manage student attendance records.

## Features

* Add attendance record
* Get attendance records
* Get attendance by student
* Get attendance by date
* Update attendance
* Delete attendance
* Calculate attendance percentage
* Handle invalid student IDs

## Example Attendance

```json
{
    "student_id": 101,
    "date": "2026-09-29",
    "status": "present"
}
```

## Possible Endpoints

```text
POST   /attendance
GET    /attendance
GET    /attendance/{student_id}
GET    /attendance?date=2026-09-29
PUT    /attendance/{attendance_id}
DELETE /attendance/{attendance_id}
```

## FastAPI Concepts Used

* CRUD Operations
* Path Parameters
* Query Parameters
* Request Body
* Pydantic Models
* Response Models
* Validation
* HTTPException

---

# Project 6: Book Management API 📚

## Objective

Build an API to manage books in a library.

## Features

* Add books
* Get all books
* Get book by ID
* Search books by title
* Search books by author
* Update book information
* Delete books
* Check book availability

## Example Book

```json
{
    "title": "Python Programming",
    "author": "John Smith",
    "price": 599,
    "available": true
}
```

## Possible Endpoints

```text
POST   /books
GET    /books
GET    /books/{book_id}
GET    /books/search
PUT    /books/{book_id}
DELETE /books/{book_id}
```

## FastAPI Concepts Used

* HTTP Methods
* Path Parameters
* Query Parameters
* Request Body
* Pydantic Models
* Response Models
* Validation
* HTTPException

---

# Project 7: Expense Tracker API 💰

## Objective

Build an API to track personal expenses.

## Features

* Add an expense
* Get all expenses
* Get expense by ID
* Filter expenses by category
* Filter expenses by date
* Update an expense
* Delete an expense
* Calculate total expenses

## Example Expense

```json
{
    "title": "Grocery",
    "amount": 1500,
    "category": "Food",
    "date": "2026-09-29"
}
```

## Possible Endpoints

```text
POST   /expenses
GET    /expenses
GET    /expenses/{expense_id}
GET    /expenses?category=Food
GET    /expenses?date=2026-09-29
PUT    /expenses/{expense_id}
DELETE /expenses/{expense_id}
GET    /expenses/total
```

## FastAPI Concepts Used

* CRUD Operations
* Path Parameters
* Query Parameters
* Request Body
* Pydantic Models
* Response Models
* Validation
* HTTPException

---

# Project 8: Simple Authentication API 🔐

## Objective

Build a basic authentication API for learning authentication concepts.

## Features

* User registration
* User login
* Validate user credentials
* Handle invalid credentials
* Protect a sample endpoint

## Possible Endpoints

```text
POST   /register
POST   /login
GET    /profile
```

## FastAPI Concepts Used

* POST
* Request Body
* Pydantic Models
* Response Models
* HTTPException
* Status Codes
* Basic Authentication Concepts

> Authentication and password security should be implemented properly before using such an API in a real production system.

---

# Recommended Learning Order 📈

Complete the projects in this order:

```text
1. Student Management API
        ↓
2. Product Management API
        ↓
3. Task Management API
        ↓
4. Employee Management API
        ↓
5. Student Attendance API
        ↓
6. Book Management API
        ↓
7. Expense Tracker API
        ↓
8. Simple Authentication API
```

Each project builds on concepts learned in the previous projects.

---

# FastAPI Concepts Covered

By completing these projects, you will practice:

```text
FastAPI
│
├── Routes
├── GET
├── POST
├── PUT
├── PATCH
├── DELETE
│
├── Path Parameters
├── Query Parameters
├── Request Body
│
├── Pydantic Models
├── Request Validation
├── Response Models
├── Response Validation
│
├── HTTPException
├── Status Codes
├── Error Handling
│
└── CRUD APIs
```

---

# Next Advanced Topics 🚀

After completing these practice projects, the next FastAPI learning stage can include:

* APIRouter
* Project Structure
* Dependency Injection
* Database Integration
* SQLAlchemy
* PostgreSQL
* Authentication
* JWT
* Password Hashing
* Middleware
* Background Tasks
* CORS
* Testing
* API Documentation
* Docker
* Production Deployment

---

# Goal 🎯

The goal of these projects is to move from:

```text
Learning Individual Concepts
            ↓
Writing Small APIs
            ↓
Building CRUD APIs
            ↓
Handling Validation & Errors
            ↓
Building Real-World APIs
```

By the end of these projects, you should be comfortable creating and testing basic REST APIs with FastAPI.
