
from typing import Literal

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Task Management API",
    description="A practice REST API for managing daily tasks",
    version="1.0.0",
)


# -----------------------------
# Pydantic Models
# -----------------------------

TaskStatus = Literal["pending", "in_progress", "completed"]


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    status: TaskStatus = "pending"


class TaskUpdate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    status: TaskStatus


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus


# -----------------------------
# In-Memory Data Store
# -----------------------------

tasks: list[dict] = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "description": "Complete FastAPI practice",
        "status": "in_progress",
    },
    {
        "id": 2,
        "title": "Practice Python",
        "description": "Solve Python programming problems",
        "status": "pending",
    },
]


# -----------------------------
# Create Task
# -----------------------------

@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(task: TaskCreate):
    new_id = max(
        (existing["id"] for existing in tasks),
        default=0,
    ) + 1

    new_task = {
        "id": new_id,
        **task.model_dump(),
    }

    tasks.append(new_task)
    return new_task


# -----------------------------
# Get All Tasks / Filter
# -----------------------------

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    task_status: TaskStatus | None = Query(
        default=None,
        alias="status",
        description="Filter tasks by status",
    ),
):
    if task_status is None:
        return tasks

    return [
        task for task in tasks
        if task["status"] == task_status
    ]


# -----------------------------
# Search Tasks by Title
# -----------------------------

@app.get("/tasks/search", response_model=list[TaskResponse])
def search_tasks(
    title: str = Query(
        min_length=2,
        description="Search tasks by title",
    ),
):
    return [
        task for task in tasks
        if title.lower() in task["title"].lower()
    ]


# -----------------------------
# Get Task by ID
# -----------------------------

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found",
    )


# -----------------------------
# Update Complete Task
# -----------------------------

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated_task: TaskUpdate):
    for index, existing_task in enumerate(tasks):
        if existing_task["id"] == task_id:
            task_data = {
                "id": task_id,
                **updated_task.model_dump(),
            }

            tasks[index] = task_data
            return task_data

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found",
    )


# -----------------------------
# Update Task Status
# -----------------------------

@app.patch(
    "/tasks/{task_id}/status",
    response_model=TaskResponse,
)
def update_task_status(
    task_id: int,
    status_update: TaskStatusUpdate,
):
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status_update.status
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found",
    )


# -----------------------------
# Delete Task
# -----------------------------

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)

            return {
                "message": "Task deleted successfully",
                "task_id": task_id,
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found",
    )



# cd 10-practice-projects\03-task-management
# uvicorn main:app --reload