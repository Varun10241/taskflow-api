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

# Module 4 — Database Integration with SQLite & SQLAlchemy

## What We Learned

In this module, we replaced the in-memory Python list with a real SQLite database using SQLAlchemy.

Before:

```text
FastAPI
   ↓
storage.py
   ↓
Python list
```

After:

```text
FastAPI
   ↓
SQLAlchemy Session
   ↓
Engine
   ↓
SQLite
   ↓
taskflow.db
```

---

## 1. SQLite

SQLite is a database engine that stores the database in a file.

Our database URL:

```python
DATABASE_URL = "sqlite:///./taskflow.db"
```

This means:

- `sqlite` → use SQLite
- `./taskflow.db` → database file in the current project directory

Unlike databases such as PostgreSQL, SQLite does not normally require a separate database server.

---

## 2. SQLAlchemy

SQLAlchemy is a Python library that allows us to work with databases using Python objects and SQL.

We use its ORM (Object Relational Mapper).

ORM allows us to represent database tables using Python classes.

Example:

```python
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    completed: Mapped[bool] = mapped_column(Boolean)
```

This represents the `tasks` database table.

Conceptually:

```text
Python class       → Database table
Python attribute   → Database column
Python object      → Database row
```

---

## 3. Engine

```python
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
```

The SQLAlchemy Engine is the central database connectivity manager.

It knows:

- which database to connect to
- which database dialect to use
- how to obtain database connections

The Engine also manages the connection pool.

---

## 4. `check_same_thread=False`

SQLite's Python driver normally restricts a database connection to the thread that created it.

We use:

```python
connect_args={"check_same_thread": False}
```

to disable that restriction.

This does **not** mean:

- SQLite creates multiple connections
- Sessions become thread-safe
- one Session should be shared between requests

We still use a separate SQLAlchemy Session for each request/unit of work.

---

## 5. `sessionmaker`

```python
SessionLocal = sessionmaker(bind=engine)
```

`SessionLocal` is a Session factory.

Calling:

```python
db = SessionLocal()
```

creates an actual SQLAlchemy `Session`.

The Session is used for database operations:

```python
db.add(...)
db.get(...)
db.delete(...)
db.commit()
db.refresh(...)
```

---

## 6. Database Session Dependency

We created:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

`yield` allows FastAPI to:

1. create the Session
2. give the Session to the route
3. wait for the route to finish
4. resume the dependency
5. close the Session

Routes use it with:

```python
db = Depends(get_db)
```

Flow:

```text
Request
   ↓
Depends(get_db)
   ↓
SessionLocal()
   ↓
yield db
   ↓
Route receives db
   ↓
Route finishes
   ↓
finally
   ↓
db.close()
```

`try/finally` is used for cleanup. `finally` runs even if an exception occurs.

---

## 7. SQLAlchemy Model vs Pydantic Schema

We have two different `Task` classes.

### Pydantic `Task`

Used for API validation and responses:

```python
from schemas import Task
```

### SQLAlchemy `Task`

Used for database operations:

```python
from models import Task as TaskModel
```

We use the alias because both classes are named `Task`.

Example:

```python
response_model=Task
```

means the Pydantic schema.

While:

```python
db.get(TaskModel, task_id)
```

means the SQLAlchemy ORM model.

---

## 8. Pydantic → ORM

The conversion from the incoming Pydantic object to an ORM object is done manually.

For example:

```python
db_task = TaskModel(
    title=task.title,
    completed=task.completed
)
```

Flow:

```text
Client JSON
    ↓
TaskRequest
    ↓
TaskModel
    ↓
Database
```

Pydantic and SQLAlchemy have different responsibilities, so we explicitly create the ORM object.

---

## 9. ORM → Pydantic Response

For responses, we can return the ORM object:

```python
return db_task
```

FastAPI/Pydantic handles the response serialization when the response model is configured appropriately.

Flow:

```text
Database
    ↓
SQLAlchemy ORM object
    ↓
FastAPI/Pydantic
    ↓
JSON response
```

---

# CRUD Operations

## 10. CREATE — POST `/tasks`

We use:

```python
db_task = TaskModel(
    title=task.title,
    completed=task.completed
)

db.add(db_task)
db.commit()
db.refresh(db_task)

return db_task
```

### `db.add()`

Adds the ORM object to the Session's pending work.

It does not permanently save the object yet.

### `db.commit()`

Commits the pending change to the database.

### `db.refresh()`

Reloads the object's current values from the database.

This is especially useful after inserting because the database generates the primary-key ID.

Before insertion:

```text
db_task.id → None
```

After the database generates the ID and the object is refreshed:

```text
db_task.id → 2
```

The important sequence is:

```text
db.add()
   ↓
db.commit()
   ↓
db.refresh()
```

---

## 11. READ ALL — GET `/tasks`

We use:

```python
return db.query(TaskModel).all()
```

This retrieves all rows from the `tasks` table as SQLAlchemy ORM objects.

---

## 12. READ ONE — GET `/tasks/{task_id}`

We use:

```python
db_task = db.get(TaskModel, task_id)
```

This retrieves a task by its primary key.

If the task does not exist:

```python
if db_task is None:
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
```

Then:

```python
return db_task
```

---

## 13. UPDATE — PUT `/tasks/{task_id}`

PUT replaces the complete task.

```python
db_task = db.get(TaskModel, task_id)

if db_task is None:
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

db_task.title = updated.title
db_task.completed = updated.completed

db.commit()
db.refresh(db_task)

return db_task
```

Both fields are updated because `TaskRequest` represents the complete task.

---

## 14. PARTIAL UPDATE — PATCH `/tasks/{task_id}`

PATCH updates only the fields supplied by the client.

```python
if updated.title is not None:
    db_task.title = updated.title

if updated.completed is not None:
    db_task.completed = updated.completed
```

Then:

```python
db.commit()
db.refresh(db_task)

return db_task
```

Example:

```json
{
  "title": "Learn SQLAlchemy"
}
```

Only `title` is changed.

---

## 15. DELETE — DELETE `/tasks/{task_id}`

We first retrieve the ORM object:

```python
db_task = db.get(TaskModel, task_id)
```

Then check whether it exists:

```python
if db_task is None:
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
```

Then:

```python
db.delete(db_task)
db.commit()

return {"message": "Task deleted"}
```

### `db.delete()`

Marks the ORM object for deletion in the Session.

### `db.commit()`

Actually commits the deletion to the database.

We don't need `refresh()` because we are not returning the deleted object.

---

# Important Session Operations

```text
db.add(object)
    → stage an object for insertion

db.get(Model, id)
    → retrieve an object by primary key

db.delete(object)
    → mark an object for deletion

db.commit()
    → persist pending changes to the database

db.refresh(object)
    → reload current database values into the object
```

---

# PUT vs PATCH

### PUT

Replaces the complete resource:

```python
db_task.title = updated.title
db_task.completed = updated.completed
```

### PATCH

Changes only supplied fields:

```python
if updated.title is not None:
    db_task.title = updated.title

if updated.completed is not None:
    db_task.completed = updated.completed
```

---

# `commit()` vs `refresh()`

These operations have different purposes.

### `commit()`

```python
db.commit()
```

Persists pending changes from the Session to the database.

Conceptually:

```text
Python/Session
      ↓
   commit()
      ↓
  Database
```

### `refresh()`

```python
db.refresh(db_task)
```

Reloads the current database values into the Python ORM object.

Conceptually:

```text
Database
    ↓
 refresh()
    ↓
Python ORM object
```

`refresh()` does not replace `commit()`.

---

# Primary Key Generation

When we create a new ORM object:

```python
db_task = TaskModel(
    title="sleep",
    completed=True
)
```

the ID is normally:

```python
db_task.id
# None
```

because the database has not inserted the row yet.

Then:

```python
db.add(db_task)
db.commit()
```

the database generates the primary-key ID.

For example:

```text
id = 2
```

After refreshing:

```python
db.refresh(db_task)

print(db_task.id)
# 2
```

So:

```text
TaskModel(...)
    ↓
id = None
    ↓
db.add()
    ↓
db.commit()
    ↓
database generates ID
    ↓
db.refresh()
    ↓
db_task.id = 2
```

---

# Final Database Flow

```text
                   FastAPI
                      ↓
                Route Handler
                      ↓
               Depends(get_db)
                      ↓
                  Session
                      ↓
                   Engine
                      ↓
              Connection Pool
                      ↓
                 DBAPI/SQLite
                      ↓
                 taskflow.db
```

---

# Final CRUD Pattern

```text
POST:
db.add() → db.commit() → db.refresh()

GET:
db.get() / db.query()

PUT:
modify all fields → db.commit() → db.refresh()

PATCH:
modify supplied fields → db.commit() → db.refresh()

DELETE:
db.delete() → db.commit()
```

---

# Project Cleanup

The old `storage.py` in-memory storage is no longer needed.

The database is now the source of truth.

Before:

```text
routes → storage.py → Python list
```

After:

```text
routes → SQLAlchemy Session → SQLite → taskflow.db
```

## The complete CRUD API is now database-backed.

## Module Status

- ✅ Module 1 — FastAPI Fundamentals
- ✅ Module 2 — CRUD API
- ✅ Module 3 — Project Structure & Code Organization
- ✅ Module 4 — replacing in memory storage with database
- 🚧 Module 5

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
