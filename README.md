# TaskFlow API

A learning project built while learning **FastAPI** and modern Python API development.

The project is being developed step by step through multiple learning modules. Each completed module is saved in Git history so previous versions of the project can be revisited.

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- uv

---

# Module 1 — FastAPI Fundamentals

## What I learned

### 1. First FastAPI application

Created a FastAPI application and learned:

- How to import `FastAPI`
- How `FastAPI()` creates the application object
- What the `app` object represents
- How decorators define API routes
- How GET requests work
- How route functions work
- How Python dictionaries are automatically converted to JSON responses

Example:

```python
from fastapi import FastAPI

app = FastAPI(title="TaskFlow API")


@app.get("/")
def read_root() -> dict:
    return {"message": "TaskFlow API is running"}
```

### 2. GET routes

Created endpoints for retrieving tasks.

```text
GET /
GET /tasks
```

### 3. Path parameters

Learned how to capture values from URLs.

```python
@app.get("/tasks/{task_id}")
def read_task_id(task_id: int) -> dict[str, int]:
    return {"task_id": task_id}
```

Learned that FastAPI uses Python type hints to validate and convert path parameters.

### 4. POST requests

Learned how to receive data from the request body using Pydantic models.

```python
from pydantic import BaseModel


class Task(BaseModel):
    title: str
```

### 5. Nested request bodies

Learned how Pydantic models can represent nested JSON structures.

For example:

```json
{
  "task": {
    "title": "Learn FastAPI"
  }
}
```

### 6. Response models

Learned how `response_model` controls the structure of API responses.

```python
@app.post("/tasks", response_model=TaskResponse)
```

### 7. Automatic API documentation

Learned about:

- `/docs`
- `/redoc`
- OpenAPI

FastAPI automatically generates API documentation from routes, type hints, and Pydantic models.

---

# Module 2 — CRUD API

## What I built

Built a complete in-memory Task CRUD API.

The API supports:

```text
POST   /tasks
GET    /tasks
GET    /tasks/{task_id}
PUT    /tasks/{task_id}
PATCH  /tasks/{task_id}
DELETE /tasks/{task_id}
```

## What I learned

### 1. In-memory storage

Tasks are temporarily stored in a Python list.

```python
tasks = []
curr_id = 0
```

This storage is only for learning purposes and is reset when the application restarts.

### 2. Separate request and task models

Created different Pydantic models for different purposes.

```python
class TaskRequest(BaseModel):
    title: str
    completed: bool
```

```python
class Task(BaseModel):
    id: int
    title: str
    completed: bool
```

The client does not provide the task ID because the backend generates it.

### 3. ID generation

Used a separate counter to generate unique IDs during the lifetime of the application.

```python
curr_id = 0
```

This avoids using `len(tasks) + 1`, which can create duplicate IDs after deleting tasks.

### 4. GET — Read tasks

Implemented endpoints to retrieve:

- All tasks
- A specific task by ID

### 5. POST — Create a task

Implemented task creation where the backend:

1. Generates an ID
2. Creates a task
3. Stores it
4. Returns the created task

### 6. PUT — Replace/update a task

PUT requires the complete task data.

```python
class TaskRequest(BaseModel):
    title: str
    completed: bool
```

### 7. PATCH — Partially update a task

Created a separate model where fields are optional.

```python
class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None
```

Learned that:

```python
if updated.completed is not None:
```

must be used instead of:

```python
if updated.completed:
```

because `False` is a valid value that the client may intentionally send.

### 8. DELETE — Delete a task

Implemented deletion by task ID and returned a `404` error when the task does not exist.

### 9. HTTPException

Learned how to return proper HTTP errors:

```python
raise HTTPException(
    status_code=404,
    detail="Task not found"
)
```

### 10. PUT vs PATCH

Learned the difference:

- **PUT** → update/replace the complete resource
- **PATCH** → update only the fields provided

---

# Current Status

- ✅ Module 1 — FastAPI Fundamentals
- ✅ Module 2 — CRUD API
- 🚧 Module 3 — Project Structure

The project will continue evolving as new FastAPI concepts are learned.

## Running the Project

Install/sync dependencies:

```bash
uv sync
```

Run the development server:

```bash
uv run fastapi dev main.py
```

Then open the automatically generated API documentation at:

```text
http://127.0.0.1:8000/docs
```
