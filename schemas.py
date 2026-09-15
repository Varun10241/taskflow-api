from pydantic import BaseModel

class TaskRequest(BaseModel):
    title:str
    completed:bool

class Task(BaseModel):
    id:int
    title:str
    completed:bool

class TaskUpdate(BaseModel):
    title:str | None = None
    completed:bool | None = None