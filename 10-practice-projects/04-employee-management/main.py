
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Employee Management API",
    description="A practice REST API for managing employee records",
    version="1.0.0",
)


# -----------------------------
# Pydantic Models
# -----------------------------

class Employee(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=18, le=65)
    department: str = Field(min_length=2, max_length=50)
    designation: str = Field(min_length=2, max_length=100)
    salary: float = Field(gt=0)


class EmployeeResponse(Employee):
    id: int


# -----------------------------
# In-Memory Data Store
# -----------------------------

employees: list[dict] = [
    {
        "id": 1,
        "name": "Rahul Sharma",
        "age": 25,
        "department": "IT",
        "designation": "Software Developer",
        "salary": 50000.0,
    },
    {
        "id": 2,
        "name": "Priya Singh",
        "age": 28,
        "department": "HR",
        "designation": "HR Manager",
        "salary": 60000.0,
    },
]


# -----------------------------
# Create Employee
# -----------------------------

@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(employee: Employee):
    new_id = max(
        (existing["id"] for existing in employees),
        default=0,
    ) + 1

    new_employee = {
        "id": new_id,
        **employee.model_dump(),
    }

    employees.append(new_employee)
    return new_employee


# -----------------------------
# Get All Employees / Filter
# -----------------------------

@app.get("/employees", response_model=list[EmployeeResponse])
def get_employees(
    department: str | None = Query(default=None),
    min_salary: float | None = Query(default=None, ge=0),
    max_salary: float | None = Query(default=None, gt=0),
):
    if (
        min_salary is not None
        and max_salary is not None
        and min_salary > max_salary
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_salary cannot be greater than max_salary",
        )

    result = employees

    if department:
        result = [
            employee for employee in result
            if employee["department"].lower() == department.lower()
        ]

    if min_salary is not None:
        result = [
            employee for employee in result
            if employee["salary"] >= min_salary
        ]

    if max_salary is not None:
        result = [
            employee for employee in result
            if employee["salary"] <= max_salary
        ]

    return result


# -----------------------------
# Search Employees by Name
# -----------------------------

@app.get("/employees/search", response_model=list[EmployeeResponse])
def search_employees(
    name: str = Query(min_length=2, description="Employee name to search"),
):
    return [
        employee for employee in employees
        if name.lower() in employee["name"].lower()
    ]


# -----------------------------
# Get Employee by ID
# -----------------------------

@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Employee not found",
    )


# -----------------------------
# Update Employee
# -----------------------------

@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, employee: Employee):
    for index, existing_employee in enumerate(employees):
        if existing_employee["id"] == employee_id:
            updated_employee = {
                "id": employee_id,
                **employee.model_dump(),
            }

            employees[index] = updated_employee
            return updated_employee

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Employee not found",
    )


# -----------------------------
# Delete Employee
# -----------------------------

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    for index, employee in enumerate(employees):
        if employee["id"] == employee_id:
            employees.pop(index)

            return {
                "message": "Employee deleted successfully",
                "employee_id": employee_id,
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Employee not found",
    )
