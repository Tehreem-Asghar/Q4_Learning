from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, constr, validator
from datetime import date
from typing import Dict, List, Optional

app = FastAPI()

# In-memory data stores
USERS: Dict[int, "User"] = {}
TASKS: Dict[int, "Task"] = {}

# ID counters
user_id_counter = 1
task_id_counter = 1

# Pydantic Models

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=20)
    email: EmailStr

class UserRead(UserCreate):
    id: int

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: date
    user_id: int

    @validator("due_date")
    def check_due_date(cls, v):
        if v < date.today():
            raise ValueError("Due date must be today or in the future")
        return v

class Task(TaskCreate):
    id: int
    status: str = "pending"

class TaskUpdate(BaseModel):
    status: str

    @validator("status")
    def validate_status(cls, v):
        if v not in ["pending", "in_progress", "completed"]:
            raise ValueError("Status must be 'pending', 'in_progress', or 'completed'")
        return v

# FastAPI Endpoints

# Create user
@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate):
    global user_id_counter
    new_user = UserRead(id=user_id_counter, **user.dict())
    USERS[user_id_counter] = new_user
    user_id_counter += 1
    return new_user

# Get user  Fetch a User
@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int):
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    return USERS[user_id]

# Create a Task
@app.post("/tasks/", response_model=Task)
def create_task(task_data: TaskCreate):
    global task_id_counter
    if task_data.user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    new_task = Task(id=task_id_counter, **task_data.dict())
    TASKS[task_id_counter] = new_task
    task_id_counter += 1
    return new_task

# Get task
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Task not found")
    return TASKS[task_id]

# Update task status
@app.put("/tasks/{task_id}", response_model=Task)
def update_task_status(task_id: int, task_update: TaskUpdate):
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Task not found")
    TASKS[task_id].status = task_update.status
    return TASKS[task_id]

# Get all tasks for a user
@app.get("/users/{user_id}/tasks", response_model=List[Task])
def get_user_tasks(user_id: int):
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    return [task for task in TASKS.values() if task.user_id == user_id]






# 6️⃣ Task 06

# 📝 Project: Task Tracker API
# 📦 Overview
# Implement an API that manages Users and their Tasks, with:

# 🚀 Requirements
# Pydantic Models & Validation

# Define UserCreate and UserRead models inheriting BaseModel. 

# Use EmailStr for email validation. 

# Constrain username to 3–20 characters using constr.

# Ensure due_date ≥ today via a @validator. 

# FastAPI Endpoints

# Users
# POST /users/ – create a user (return UserRead).

# GET /users/{user_id} – retrieve user.

# Tasks
# POST /tasks/ – create a task (return full Task model).

# GET /tasks/{task_id} – get task.

# PUT /tasks/{task_id} – update status only, validating allowed values. 

# GET /users/{user_id}/tasks – list all tasks for a user.

# 💡Hint

# Store data in two global dicts:
# USERS: dict[int, User] = {}
# TASKS: dict[int, Task] = {}