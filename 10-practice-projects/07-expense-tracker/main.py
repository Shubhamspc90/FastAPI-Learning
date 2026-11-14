
from datetime import date
from typing import Literal

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field


app = FastAPI(
    title="Expense Tracker API",
    description="A practice REST API for tracking and managing expenses",
    version="1.0.0",
)


ExpenseCategory = Literal[
    "food",
    "travel",
    "shopping",
    "bills",
    "health",
    "education",
    "other",
]


class ExpenseCreate(BaseModel):
    description: str = Field(min_length=2, max_length=150)
    amount: float = Field(gt=0)
    category: ExpenseCategory
    expense_date: date


class ExpenseUpdate(ExpenseCreate):
    pass


class ExpenseResponse(ExpenseCreate):
    id: int


expenses: list[dict] = [
    {
        "id": 1,
        "description": "Grocery shopping",
        "amount": 1500.0,
        "category": "food",
        "expense_date": date(2026, 11, 10),
    },
    {
        "id": 2,
        "description": "Bus ticket",
        "amount": 500.0,
        "category": "travel",
        "expense_date": date(2026, 11, 11),
    },
    {
        "id": 3,
        "description": "Electricity bill",
        "amount": 1200.0,
        "category": "bills",
        "expense_date": date(2026, 11, 12),
    },
]


@app.post(
    "/expenses",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_expense(expense: ExpenseCreate):
    new_id = max(
        (existing["id"] for existing in expenses),
        default=0,
    ) + 1

    new_expense = {
        "id": new_id,
        **expense.model_dump(),
    }

    expenses.append(new_expense)
    return new_expense


# Fixed routes must appear before /expenses/{expense_id}.
@app.get("/expenses/search", response_model=list[ExpenseResponse])
def search_expenses(
    description: str = Query(min_length=2),
):
    return [
        expense for expense in expenses
        if description.lower() in expense["description"].lower()
    ]


@app.get("/expenses/summary")
def get_expense_summary():
    total_amount = sum(expense["amount"] for expense in expenses)

    category_totals: dict[str, float] = {}

    for expense in expenses:
        category = expense["category"]
        category_totals[category] = (
            category_totals.get(category, 0.0) + expense["amount"]
        )

    return {
        "total_expenses": len(expenses),
        "total_amount": round(total_amount, 2),
        "category_wise_totals": {
            category: round(amount, 2)
            for category, amount in category_totals.items()
        },
    }


@app.get("/expenses", response_model=list[ExpenseResponse])
def get_expenses(
    category: ExpenseCategory | None = Query(default=None),
    min_amount: float | None = Query(default=None, gt=0),
    max_amount: float | None = Query(default=None, gt=0),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
):
    if (
        min_amount is not None
        and max_amount is not None
        and min_amount > max_amount
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_amount cannot be greater than max_amount",
        )

    if (
        start_date is not None
        and end_date is not None
        and start_date > end_date
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date cannot be later than end_date",
        )

    result = expenses

    if category is not None:
        result = [
            expense for expense in result
            if expense["category"] == category
        ]

    if min_amount is not None:
        result = [
            expense for expense in result
            if expense["amount"] >= min_amount
        ]

    if max_amount is not None:
        result = [
            expense for expense in result
            if expense["amount"] <= max_amount
        ]

    if start_date is not None:
        result = [
            expense for expense in result
            if expense["expense_date"] >= start_date
        ]

    if end_date is not None:
        result = [
            expense for expense in result
            if expense["expense_date"] <= end_date
        ]

    return result


@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int):
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Expense not found",
    )


@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, updated_expense: ExpenseUpdate):
    for index, existing_expense in enumerate(expenses):
        if existing_expense["id"] == expense_id:
            new_expense = {
                "id": expense_id,
                **updated_expense.model_dump(),
            }

            expenses[index] = new_expense
            return new_expense

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Expense not found",
    )


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            expenses.pop(index)

            return {
                "message": "Expense deleted successfully",
                "expense_id": expense_id,
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Expense not found",
    )


# cd 10-practice-projects\07-expense-tracker
# uvicorn main:app --reload