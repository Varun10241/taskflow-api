from pydantic import BaseModel,ConfigDict

class TaskRequest(BaseModel):
    title:str
    completed:bool

class Task(BaseModel):
    id:int
    title:str
    completed:bool
    model_config=ConfigDict(from_attributes=True)

class TaskUpdate(BaseModel):
    title:str | None = None
    completed:bool | None = None

class UserRequest(BaseModel):
    name:str

class User(BaseModel):
    id:int
    name:str
    tasks:list[Task]
    model_config=ConfigDict(from_attributes=True)