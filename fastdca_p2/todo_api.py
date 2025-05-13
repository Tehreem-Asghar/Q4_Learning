from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Simple TODO API")

# Pydantic model
class Todo(BaseModel):
    id: int
    task: str
    completed: bool = False

# In-memory list to store todos
todo_list: List[Todo] = []

# 1. GET /todos/ - List all todos
@app.get("/todos/", response_model=List[Todo])
def get_todos():
    return todo_list

# 2. POST /todos/ - Add a new todo
@app.post("/todos/", response_model=Todo)
def create_todo(todo: Todo):
    todo_list.append(todo)
    return todo

# 3. PUT /todos/{todo_id} - Mark a todo as completed
@app.put("/todos/{todo_id}", response_model=Todo)
def mark_completed(todo_id: int):
    for todo in todo_list:
        if todo.id == todo_id:
            todo.completed = True
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")