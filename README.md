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

---

# Module 5 — SQLAlchemy Relationships & Advanced Queries

## Overview

In Module 5, TaskFlow was extended from a simple task database into a relational application.

We learned:

- One-to-many relationships
- Foreign keys
- SQLAlchemy `relationship()`
- `back_populates`
- Creating related records
- Navigating relationships
- Nested API responses
- Cascade behavior
- Database constraints
- Filtering queries
- Ordering and limiting
- Advanced SQLAlchemy queries
- `scalars()`, `all()`, and `scalar_one_or_none()`
- Lazy loading
- Eager loading
- `selectinload()`
- N+1 query problem
- API organization and cleanup

---

# 1. One-to-Many Relationship

TaskFlow has a one-to-many relationship:

    User
     ├── Task
     ├── Task
     └── Task

One User can have many Tasks.

Each Task belongs to one User.

    User → one-to-many → Task
    Task → many-to-one → User

---

# 2. Foreign Keys

A foreign key connects a row in one table to a row in another table.

In the `Task` model:

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

This creates the relationship:

    tasks.user_id → users.id

Example:

    users
    +----+----------+
    | id | name     |
    +----+----------+
    | 1  | Varunsai |
    +----+----------+

    tasks
    +----+---------+---------+
    | id | title   | user_id |
    +----+---------+---------+
    | 1  | Eating  | 1       |
    | 2  | Study   | 1       |
    +----+---------+---------+

Both tasks belong to User 1.

---

# 3. SQLAlchemy `relationship()`

The foreign key connects the database tables.

`relationship()` connects the related SQLAlchemy objects.

Task model:

    user: Mapped["User"] = relationship(
        back_populates="tasks"
    )

User model:

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

Now SQLAlchemy understands:

    User.tasks
    Task.user

---

# 4. `back_populates`

`back_populates` connects both sides of the relationship.

    # User
    tasks = relationship(back_populates="user")

    # Task
    user = relationship(back_populates="tasks")

This creates a two-way relationship:

    User.tasks
         ↕
    Task.user

For example:

    user.tasks

returns the user's tasks.

And:

    task.user

returns the task's user.

---

# 5. Creating Related Records

TaskFlow creates tasks through their user.

Endpoint:

    POST /users/{user_id}/tasks

First, find the user:

    db_user = db.get(User, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )

Create the task:

    db_task = Task(
        title=task.title,
        completed=task.completed
    )

Attach it to the user's task collection:

    db_user.tasks.append(db_task)

SQLAlchemy handles the relationship and foreign key.

We do not need to manually set:

    db_task.user_id = user_id

when using the relationship.

---

# 6. Navigating Relationships

User → Tasks:

    db_user.tasks

Task → User:

    db_task.user

Relationship navigation:

    User.tasks
        ↓
      Tasks

    Task.user
        ↓
       User

---

# 7. Nested API Responses

Because a User has Tasks, the User response schema can contain nested tasks.

    class User(BaseModel):
        id: int
        name: str
        tasks: list[Task]

        model_config = ConfigDict(
            from_attributes=True
        )

Example response:

    {
      "id": 1,
      "name": "Varunsai",
      "tasks": [
        {
          "id": 1,
          "title": "Eating",
          "completed": false
        },
        {
          "id": 2,
          "title": "Study",
          "completed": true
        }
      ]
    }

This is called a nested response.

---

# 8. `from_attributes=True`

For ORM-backed response schemas:

    model_config = ConfigDict(
        from_attributes=True
    )

This allows Pydantic to read values directly from SQLAlchemy model attributes.

For example:

    Task.model_validate(db_task)

can read:

    db_task.id
    db_task.title
    db_task.completed

Request schemas do not need `from_attributes=True`.

---

# 9. Cascade Behavior

The User relationship contains:

    cascade="all, delete-orphan"

The important behavior for TaskFlow is:

    Delete User
         ↓
    Delete user's Tasks

Example:

    User 5
     ├── Task 5
     └── Task 6

    Delete User 5

         ↓

    User 5 deleted
    Task 5 deleted
    Task 6 deleted

This behavior was tested through the API.

The cascade is configured on:

    User.tasks

because User is the parent.

We do not want:

    Delete Task
         ↓
    Delete User

Deleting a Task should not delete its parent User.

---

# 10. `delete-orphan`

`delete-orphan` handles child objects that are removed from an ownership relationship.

The idea is:

    Parent owns Child

If the child becomes an orphan, SQLAlchemy can delete it.

Syntax:

    cascade="all, delete-orphan"

---

# 11. Database Constraints

Database constraints protect data integrity.

## Primary Key

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

A primary key uniquely identifies a row.

Example:

    Task 1
    Task 2
    Task 3

Each task has its own ID.

## Foreign Key

    ForeignKey("users.id")

Connects a Task to a User:

    tasks.user_id → users.id

## Unique

    name: Mapped[str] = mapped_column(
        String,
        unique=True
    )

Prevents duplicate values.

For TaskFlow, two users cannot have the same name.

## Nullable

    nullable=False

means the database column cannot contain `NULL`.

Example:

    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

---

# 12. Filtering Queries

`where()` adds filtering conditions.

Example:

    statement = select(Task).where(
        Task.completed == True
    )

This means:

    Give me tasks where completed is True.

TaskFlow provides:

    GET /tasks/completed

---

# 13. Combining Conditions

Multiple conditions passed to `where()` are combined using `AND`.

Example:

    statement = select(Task).where(
        Task.user_id == 3,
        Task.completed == False
    )

This means:

    user_id = 3
    AND
    completed = false

SQLAlchemy also provides:

    and_()
    or_()

for more complex conditions.

---

# 14. Ordering Results

`order_by()` controls the order of returned rows.

Example:

    Task.id.desc()

means:

    highest ID → lowest ID

Example:

    statement = (
        select(Task)
        .order_by(Task.id.desc())
    )

---

# 15. Limiting Results

`limit()` controls how many rows are returned.

Example:

    statement = (
        select(Task)
        .order_by(Task.id.desc())
        .limit(3)
    )

This means:

    Sort by ID descending
            ↓
    Return only 3 tasks

TaskFlow provides:

    GET /tasks/latest?limit=3

Note:

`id.desc()` gives the highest IDs first. It is only a proxy for "latest" when IDs correlate with creation order.

---

# 16. `select()`

SQLAlchemy's `select()` builds a database query.

Example:

    statement = select(Task)

This describes what we want to retrieve.

It does not execute the query yet.

---

# 17. `db.execute()`

After creating a statement:

    statement = select(Task)

we execute it:

    result = db.execute(statement)

The flow is:

    select()
       ↓
    Build SQL statement
       ↓
    db.execute()
       ↓
    Execute query
       ↓
    result

---

# 18. `scalars()`

When selecting one main value or ORM object:

    statement = select(Task)

we commonly use:

    result.scalars().all()

Example:

    statement = select(Task)

    result = db.execute(statement)

    tasks = result.scalars().all()

`scalars()` extracts the first selected value from each result row.

---

# 19. `all()`

When selecting multiple columns:

    statement = select(
        Task.title,
        Task.completed
    )

the result contains SQLAlchemy `Row` objects.

We can use:

    result.all()

Example:

    result = db.execute(statement)

    rows = result.all()

The rows contain the selected values.

---

# 20. `scalar_one_or_none()`

Use this when the query should return zero or one result.

Example:

    result = db.execute(statement)

    db_user = result.scalar_one_or_none()

Possible results:

    User found
        ↓
    User object

    User not found
        ↓
    None

If multiple results are returned when only one was expected, `scalar_one_or_none()` raises an error.

---

# 21. Choosing the Result Method

## Query returns many ORM objects

    select(Task)

Use:

    result.scalars().all()

Possible result:

    []

or:

    [task1, task2, task3]

## Query returns zero or one object

    select(User).where(User.id == user_id)

Use:

    result.scalar_one_or_none()

## Query selects multiple columns

    select(Task.title, Task.completed)

Use:

    result.all()

---

# 22. SQLAlchemy to SQL

SQLAlchemy Python expressions are translated into SQL.

Example:

    statement = (
        select(Task.id, Task.title)
        .where(Task.user_id == 3)
        .order_by(Task.id.desc())
        .limit(3)
    )

Conceptually similar SQL:

    SELECT tasks.id, tasks.title
    FROM tasks
    WHERE tasks.user_id = 3
    ORDER BY tasks.id DESC
    LIMIT 3;

The Python code describes the query, and SQLAlchemy generates the SQL.

---

# 23. Lazy Loading

With a relationship:

    db_user = db.get(User, user_id)

the User is loaded first.

When we later access:

    db_user.tasks

SQLAlchemy can load the related tasks at that point.

This is lazy loading.

Conceptually:

    Load User
        ↓
    Later access user.tasks
        ↓
    Load Tasks

---

# 24. Eager Loading

Eager loading loads related data as part of the query strategy.

TaskFlow uses:

    from sqlalchemy.orm import selectinload

Example:

    statement = (
        select(User)
        .options(selectinload(User.tasks))
        .where(User.id == user_id)
    )

Now the tasks are loaded eagerly.

---

# 25. `selectinload()`

`selectinload()` generally uses a separate query to load related records in batches.

For multiple users, instead of repeatedly querying tasks:

    Query Users

    Query Tasks for User 1
    Query Tasks for User 2
    Query Tasks for User 3

`selectinload()` can batch the task loading:

    Query Users

    Query Tasks
    WHERE user_id IN (1, 2, 3)

This helps avoid the N+1 query problem.

---

# 26. N+1 Query Problem

Suppose we load 3 users and then access each user's tasks separately.

A lazy-loading pattern can result in approximately:

    1 query → users

    3 queries → tasks for each user

    Total = 4 queries

With `selectinload()`:

    1 query → users

    1 query → all related tasks

    Total = 2 queries

The exact number of queries depends on the loading strategy and query.

---

# 27. Final TaskFlow Models

    class Task(Base):
        __tablename__ = "tasks"

        id: Mapped[int] = mapped_column(
            primary_key=True
        )

        title: Mapped[str] = mapped_column(
            String
        )

        completed: Mapped[bool] = mapped_column(
            Boolean
        )

        user_id: Mapped[int] = mapped_column(
            ForeignKey("users.id")
        )

        user: Mapped["User"] = relationship(
            back_populates="tasks"
        )


    class User(Base):
        __tablename__ = "users"

        id: Mapped[int] = mapped_column(
            primary_key=True
        )

        name: Mapped[str] = mapped_column(
            String,
            unique=True,
            nullable=False
        )

        tasks: Mapped[list["Task"]] = relationship(
            back_populates="user",
            cascade="all, delete-orphan"
        )

---

# 28. Final TaskFlow Schemas

    from pydantic import BaseModel, ConfigDict


    class TaskRequest(BaseModel):
        title: str
        completed: bool


    class Task(BaseModel):
        id: int
        title: str
        completed: bool

        model_config = ConfigDict(
            from_attributes=True
        )


    class TaskUpdate(BaseModel):
        title: str | None = None
        completed: bool | None = None


    class UserRequest(BaseModel):
        name: str


    class User(BaseModel):
        id: int
        name: str
        tasks: list[Task]

        model_config = ConfigDict(
            from_attributes=True
        )

---

# 29. Final API

## User Endpoints

    POST   /users
    POST   /users/{user_id}/tasks

    GET    /users/{user_id}
    GET    /users/{user_id}/tasks

    DELETE /users/{user_id}

## Task Endpoints

    GET    /tasks
    GET    /tasks/{task_id}

    PUT    /tasks/{task_id}
    PATCH  /tasks/{task_id}
    DELETE /tasks/{task_id}

    GET    /tasks/latest
    GET    /tasks/completed

The old standalone endpoint:

    POST /tasks

was removed because Tasks now belong to Users.

Task creation is done through:

    POST /users/{user_id}/tasks

---

# 30. Task ID vs User ID

A Task has both:

    task_id
    user_id

They have different purposes.

## `task_id`

Identifies a specific task.

    PATCH /tasks/5

means:

    Modify Task 5.

## `user_id`

Identifies the owner.

    GET /users/3/tasks

means:

    Get Tasks belonging to User 3.

The database knows which user owns a task through:

    tasks.user_id → users.id

Later, authentication and authorization can verify whether the current user is allowed to modify a particular task.

---

# 31. Important Concepts to Remember

    ForeignKey
        ↓
    Connects database tables

    relationship()
        ↓
    Connects SQLAlchemy objects

    back_populates
        ↓
    Connects both sides of a relationship

    cascade
        ↓
    Propagates operations between related objects

    where()
        ↓
    Filters results

    order_by()
        ↓
    Sorts results

    limit()
        ↓
    Limits results

    select()
        ↓
    Builds a query

    execute()
        ↓
    Runs the query

    scalars().all()
        ↓
    Returns many single selected values/objects

    all()
        ↓
    Returns SQLAlchemy Row objects for multiple selected columns

    scalar_one_or_none()
        ↓
    Returns zero or one result

    selectinload()
        ↓
    Eagerly loads relationships efficiently

---

# Module 5 Complete

TaskFlow now has a proper relational database design:

    User
      │
      │ one-to-many
      ↓
    Task

The project now supports:

- Relational database modeling
- User → Task relationships
- Foreign keys
- SQLAlchemy relationships
- Nested responses
- Cascade deletion
- Database constraints
- Filtering
- Ordering
- Limiting
- Advanced SQLAlchemy queries
- Lazy loading
- Eager loading
- `selectinload()`
- Full Task CRUD
- User and User-Task operations

Module 5 is complete.

---

# Module 6 — Authentication & Authorization

## 1. Authentication vs Authorization

### Authentication

Authentication answers:

> Who is the user?

Example: verifying a user's username and password during login.

### Authorization

Authorization answers:

> What is the authenticated user allowed to do?

Example: User 1 should not be able to update User 2's task.

---

## 2. Password Hashing

Passwords should never be stored directly in the database.

Instead:

    Plain password
          ↓
    Password hashing
          ↓
    Password hash
          ↓
    Database

We used `pwdlib`:

    from pwdlib import PasswordHash

    pwd_hash = PasswordHash.recommended()

Hashing a password:

    password_hash = pwd_hash.hash(user.password)

Verifying a password:

    pwd_hash.verify(
        credentials.password,
        db_user.password_hash
    )

Password hashes are not decrypted back into the original password. The password-hashing library verifies the supplied password against the stored hash.

---

## 3. User Registration

`POST /users` creates a new user.

The password is hashed before storing the user:

    password_hash = pwd_hash.hash(user.password)

    db_user = User(
        name=user.name,
        password_hash=password_hash
    )

The API does not expose the password hash.

Response schema:

    class UserCreateResponse(BaseModel):
        id: int
        name: str

---

## 4. Login

Login endpoint:

    POST /login

Request:

    {
      "name": "Varun",
      "password": "password"
    }

The server:

1.  Finds the user by name.
2.  Verifies the supplied password against the stored password hash.
3.  Creates a JWT if the credentials are valid.
4.  Returns the access token.

    if pwd_hash.verify(credentials.password, db_user.password_hash):
    access_token = create_access_token(db_user.id)

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

Invalid credentials return:

    401 Unauthorized

---

## 5. JWT

We use JSON Web Tokens for authentication.

A JWT contains three parts:

    Header.Payload.Signature

### Header

Contains information such as the signing algorithm:

    {
      "alg": "HS256",
      "typ": "JWT"
    }

### Payload

Our token contains:

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=30)
    }

Important claims:

- `sub` — identifies the user
- `iat` — issued-at time
- `exp` — expiration time

The user ID is stored as a string in `sub`:

    "sub": str(user_id)

and converted back to an integer after decoding:

    user_id = int(payload["sub"])

### Signature

The signature is generated using the secret key and HS256.

JWTs are not encrypted. Their payload can be read.

The signature provides integrity and authenticity, not confidentiality.

---

## 6. Secret Key

The JWT secret key is stored in `.env`:

    SECRET_KEY=...

`.env` is added to `.gitignore`:

    .env

We load it using:

    from dotenv import load_dotenv
    import os

    load_dotenv()

    SECRET_KEY = os.getenv("SECRET_KEY")

The secret key should never be committed to Git.

---

## 7. Creating an Access Token

We created:

    def create_access_token(user_id: int) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + timedelta(minutes=30)
        }

        token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm="HS256"
        )

        return token

`exp` limits how long the token remains valid.

PyJWT automatically checks the expiration when decoding the token.

---

## 8. Decoding and Validating JWT

We created:

    def decode_access_token(token: str):
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return payload

Invalid or expired tokens cause JWT validation errors.

We catch those errors and return:

    401 Unauthorized

---

## 9. OAuth2PasswordBearer

FastAPI provides:

    from fastapi.security import OAuth2PasswordBearer

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

It extracts the bearer token from:

    Authorization: Bearer <JWT>

Important:

`OAuth2PasswordBearer` extracts the token. It does not itself verify the JWT.

JWT verification happens inside our `decode_access_token()` function.

---

## 10. get_current_user() Dependency

We created a reusable authentication dependency:

    def get_current_user(
        token: str = Depends(oauth2_scheme),
        db=Depends(get_db)
    ):
        try:
            payload = decode_access_token(token)
            user_id = int(payload["sub"])
        except (jwt.InvalidTokenError, KeyError, ValueError):
            raise HTTPException(
                status_code=401,
                detail="invalid authentication credentials"
            )

        db_user = db.get(User, user_id)

        if db_user is None:
            raise HTTPException(
                status_code=401,
                detail="user not found"
            )

        return db_user

The flow is:

    Authorization header
            ↓
    oauth2_scheme
            ↓
    JWT token
            ↓
    decode_access_token()
            ↓
    user_id
            ↓
    database lookup
            ↓
    User object
            ↓
    endpoint

---

## 11. Protected Endpoints

An endpoint becomes authenticated by using:

    current_user: User = Depends(get_current_user)

For example:

    @router.get("/tasks/{task_id}", response_model=TaskResponse)
    def read_task(
        task_id: int,
        db=Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        ...

If the request has no valid JWT, authentication fails before the endpoint executes.

---

## 12. /users/me

`/users/me` represents the currently authenticated user.

Get the current user:

    @router.get("/users/me", response_model=UserResponse)
    def read_current_user(
        current_user: User = Depends(get_current_user)
    ):
        return current_user

Delete the current user:

    @router.delete("/users/me", response_model=dict[str, str])
    def delete_user(
        db=Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> dict[str, str]:

        db.delete(current_user)
        db.commit()

        return {"message": "user deleted"}

The client does not need to provide a user ID because the JWT identifies the user.

---

## 13. 401 vs 403

### 401 Unauthorized

The request is not successfully authenticated.

Examples:

- No token
- Invalid token
- Expired token
- Invalid username/password

Example:

    raise HTTPException(
        status_code=401,
        detail="invalid authentication credentials"
    )

### 403 Forbidden

The user is authenticated but is not allowed to access the requested resource.

Example:

    if db_task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="forbidden"
        )

---

## 14. Task Ownership

For individual task operations, we check that the authenticated user owns the task:

    if db_task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="forbidden"
        )

This protects:

    GET    /tasks/{task_id}
    PUT    /tasks/{task_id}
    PATCH  /tasks/{task_id}
    DELETE /tasks/{task_id}

---

## 15. Filtering Tasks by Authenticated User

For collection endpoints, we filter directly in the database query.

Example:

    statement = (
        select(Task)
        .where(Task.user_id == current_user.id)
    )

This means the database only returns tasks belonging to the authenticated user.

### Latest tasks

    statement = (
        select(Task)
        .where(Task.user_id == current_user.id)
        .order_by(Task.id.desc())
        .limit(limit)
    )

### Completed tasks

    statement = select(Task).where(
        Task.user_id == current_user.id,
        Task.completed == True
    )

---

## 16. Creating Tasks with the Authenticated User

Previously we had:

    POST /users/{user_id}/tasks

We changed this to:

    POST /tasks

The client does not specify the owner.

    @router.post("/tasks", response_model=TaskResponse)
    def create_task(
        task: TaskRequest,
        db=Depends(get_db),
        current_user: User = Depends(get_current_user)
    ) -> TaskResponse:

        db_task = Task(
            title=task.title,
            completed=task.completed
        )

        current_user.tasks.append(db_task)

        db.commit()
        db.refresh(db_task)

        return db_task

The relationship associates the new task with the authenticated user:

    current_user.tasks.append(db_task)

The authenticated user determines ownership.

---

## 17. Final Task API

    POST   /tasks
    GET    /tasks
    GET    /tasks/{task_id}
    GET    /tasks/latest
    GET    /tasks/completed
    PUT    /tasks/{task_id}
    PATCH  /tasks/{task_id}
    DELETE /tasks/{task_id}

Task endpoints use authentication and ownership where appropriate.

---

## 18. Final User API

    POST   /users
    POST   /login
    GET    /users/me
    DELETE /users/me

We removed these endpoints because they are unnecessary for our current private task-manager design:

    GET  /users/{user_id}
    GET  /users/{user_id}/tasks
    POST /users/{user_id}/tasks
    DELETE /users/{user_id}

The authenticated user's identity comes from the JWT.

---

## 19. SQLAlchemy Query Building

A complex query does not require multiple database queries just because it has multiple conditions.

We can build one statement:

    statement = (
        select(Task.title, Task.completed)
        .where(
            Task.user_id == current_user.id,
            Task.completed == True
        )
        .order_by(Task.id.desc())
        .limit(5)
    )

The database is queried when we execute it:

    result = db.execute(statement)

Conceptually:

    select()
       ↓
    where()
       ↓
    order_by()
       ↓
    limit()
       ↓
    execute()
       ↓
    ONE database query

However, `get_current_user()` itself performs a database lookup to verify that the user exists.

Therefore, an authenticated endpoint can involve:

    Query 1 → authenticate/find current user
    Query 2 → execute the actual business query

If an endpoint only needs the user ID, a future optimization would be a dependency that validates the JWT and returns the user ID without querying the User table.

---

## 20. Complete Authentication Flow

    REGISTER
       ↓
    POST /users
       ↓
    Hash password
       ↓
    Store user in database


    LOGIN
       ↓
    POST /login
       ↓
    Verify password
       ↓
    Create JWT
       ↓
    Return access token


    PROTECTED REQUEST
       ↓
    Authorization: Bearer JWT
       ↓
    oauth2_scheme
       ↓
    get_current_user()
       ↓
    Decode and verify JWT
       ↓
    Get user ID
       ↓
    Find user
       ↓
    current_user
       ↓
    Endpoint
       ↓
    Authorization / ownership check
       ↓
    Response

---

## Module 6 Key Takeaways

- Authentication = **Who are you?**
- Authorization = **What are you allowed to do?**
- Never store plain-text passwords.
- Password hashes are verified, not decrypted.
- JWTs are signed, not encrypted.
- `exp` controls token expiration.
- JWT secrets should be stored outside the source code.
- `OAuth2PasswordBearer` extracts the bearer token.
- `get_current_user()` centralizes authentication logic.
- `401` means authentication failed.
- `403` means authentication succeeded but access is forbidden.
- Task ownership is enforced using the authenticated user's ID.
- Collection endpoints can filter data at the database level.
- `/users/me` identifies the currently authenticated user.
- The JWT can identify the owner, so clients do not need to send `user_id` for their own resources.

## Module Status

- ✅ Module 1 — FastAPI Fundamentals
- ✅ Module 2 — CRUD API
- ✅ Module 3 — Project Structure & Code Organization
- ✅ Module 4 — replacing in memory storage with database
- ✅ Module 5 - advanced database design and operations
- ✅ Module 6 - Authentication,JWT and Authorization
- 🚧 Module 7

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
