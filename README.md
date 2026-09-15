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

# Module 3 — Project Structure & Code Organization

## Goal

Learn how to organize a FastAPI application into multiple files and separate different responsibilities instead of keeping everything inside `main.py`.

---

## Project Structure

The project was refactored from a single `main.py` into:

```text
taskflow-api/
├── main.py
├── schemas.py
├── storage.py
├── routes/
│   ├── __init__.py
│   └── tasks.py
├── README.md
├── pyproject.toml
└── uv.lock
```

### Responsibilities

| File                 | Responsibility                                       |
| -------------------- | ---------------------------------------------------- |
| `main.py`            | Creates the FastAPI application and connects routers |
| `schemas.py`         | Contains Pydantic models                             |
| `storage.py`         | Contains temporary in-memory storage                 |
| `routes/tasks.py`    | Contains task-related API endpoints                  |
| `routes/__init__.py` | Makes `routes` an explicit Python package            |

---

## Important Concepts Learned

## 1. Separation of Responsibilities

Different parts of the application have different responsibilities.

```text
main.py
   ↓
Application setup

schemas.py
   ↓
Data models

storage.py
   ↓
Data storage

routes/tasks.py
   ↓
API endpoints
```

This makes the project easier to understand, maintain, and expand.

---

## 2. Python Modules

Every `.py` file can act as a Python module.

For example:

```text
schemas.py
storage.py
tasks.py
```

are separate modules.

Modules allow code to be divided across multiple files while still allowing those files to work together using imports.

---

## 3. Python Packages

A directory containing Python modules can be organized as a package.

Example:

```text
routes/
├── __init__.py
└── tasks.py
```

Here:

- `routes` → package
- `tasks.py` → module
- `__init__.py` → package initialization file

---

## 4. `__init__.py`

`__init__.py` is a special Python file associated with a package.

Historically, it was required for Python to recognize a directory as a regular package.

Modern Python supports namespace packages without it, but `__init__.py` is still useful because:

- It explicitly identifies a package.
- It can contain package initialization code.
- It can control what the package exposes.

For TaskFlow, `routes/__init__.py` is intentionally empty.

---

## 5. Imports

Learned how different Python files can use code from each other.

### Import a specific item

```python
from schemas import Task
```

This makes `Task` directly available:

```python
task: Task
```

### Import a module

```python
import storage
```

Then access its contents using:

```python
storage.tasks
storage.curr_id
```

---

## 6. `import module` vs `from module import item`

### Import the whole module

```python
import storage

storage.tasks
storage.curr_id
```

Useful when:

- Multiple things are needed from a module.
- You want to clearly show where something comes from.
- You want to avoid naming conflicts.

### Import specific items

```python
from schemas import Task, TaskRequest, TaskUpdate
```

Then use:

```python
Task
TaskRequest
TaskUpdate
```

Useful when:

- Only a few specific items are needed.
- Direct access makes the code easier to read.

### Rule of thumb

```text
Few specific items
    ↓
from module import item

Several items / clear ownership
    ↓
import module
```

---

## 7. Absolute Imports

An absolute import searches for a module using Python's module search path.

Example:

```python
from schemas import Task
```

This does **not** mean:

> Go one directory above.

It means:

> Find a module named `schemas` in Python's import search path.

In a properly packaged application, absolute imports can look like:

```python
from taskflow.schemas import Task
```

Absolute imports are generally preferred in larger, properly packaged Python applications because they are explicit and easier to understand.

---

## 8. Relative Imports

Relative imports navigate through the package hierarchy.

Examples:

```python
from .models import Task
```

```python
from ..models import Task
```

```python
from ...models import Task
```

The dots represent package levels:

```text
.       → current package
..      → parent package
...     → grandparent package
```

Relative imports are based on **packages**, not simply filesystem directories.

For the current TaskFlow structure, we use:

```python
from schemas import Task
```

rather than a relative import.

---

## 9. `APIRouter`

`APIRouter` allows related API routes to be grouped together.

Instead of putting everything directly on the FastAPI application:

```python
@app.get("/tasks")
```

we create a router:

```python
from fastapi import APIRouter

router = APIRouter()
```

Then define routes using:

```python
@router.get("/tasks")
@router.post("/tasks")
@router.put("/tasks/{task_id}")
@router.patch("/tasks/{task_id}")
@router.delete("/tasks/{task_id}")
```

The router acts like a collection of related routes.

---

## 10. `app.include_router()`

The router must be connected to the main FastAPI application.

In `main.py`:

```python
from fastapi import FastAPI
from routes.tasks import router

app = FastAPI(title="TaskFlow API")

app.include_router(router)
```

`include_router()` tells FastAPI:

> Include all the routes defined in this router in the application.

Conceptually:

```text
routes/tasks.py
      │
      │ router
      ▼
main.py
      │
      │ app.include_router(router)
      ▼
FastAPI application
```

---

## 11. Router Does Not Change the API

Moving a route from:

```python
@app.get("/tasks")
```

to:

```python
@router.get("/tasks")
```

does not change the API URL.

The client still uses:

```text
GET /tasks
```

The change is only in how the code is organized internally.

---

## 12. Module Variables and `global`

Learned an important Python concept while moving storage into `storage.py`.

If:

```python
# storage.py

curr_id = 0
```

and another module contains:

```python
global curr_id
```

`global` does **not** mean:

> Use the `curr_id` from every module.

It means:

> Use the global variable belonging to the current module.

Therefore, when modifying the counter from `routes/tasks.py`, we use:

```python
import storage

storage.curr_id += 1
```

This explicitly modifies the variable belonging to `storage.py`.

---

## 13. Why `storage.tasks` and `storage.curr_id`?

Instead of:

```python
from storage import tasks
```

we use:

```python
import storage
```

and:

```python
storage.tasks
storage.curr_id
```

This makes it clear that both pieces of state belong to the storage module.

It also avoids confusion when modifying module-level variables.

---

## 14. Final Architecture

After Module 3, TaskFlow follows a basic separation of concerns:

```text
                    FastAPI Application
                           │
                         main.py
                           │
                    include_router()
                           │
                           ▼
                    routes/tasks.py
                     /     |      \
                    /      |       \
                   ▼       ▼        ▼
             schemas.py  storage.py
                  │          │
                  ▼          ▼
             Pydantic     In-memory
              models       storage
```

---

## Key Takeaways

The most important things learned in Module 3:

1. **A large application should be divided into multiple modules.**
2. **Separate responsibilities between files.**
3. **A `.py` file is a Python module.**
4. **A directory can be organized as a Python package.**
5. **Understand the purpose of `__init__.py`.**
6. **Know the difference between `import module` and `from module import item`.**
7. **Understand absolute vs relative imports.**
8. **Use `APIRouter` to organize related FastAPI routes.**
9. **Use `app.include_router()` to connect routers to the FastAPI application.**
10. **Understand that `global` refers to the current module, not the entire project.**
11. **Use module-qualified names such as `storage.curr_id` when you need to clearly access module state.**

---

## Module Status

- ✅ Module 1 — FastAPI Fundamentals
- ✅ Module 2 — CRUD API
- ✅ Module 3 — Project Structure & Code Organization
- 🚧 Module 4 — Coming next

# Running the Project

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
