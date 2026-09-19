from pydantic import BaseModel,ConfigDict

class TaskRequest(BaseModel):
    title:str
    completed:bool

class TaskResponse(BaseModel):
    id:int
    title:str
    completed:bool
    model_config=ConfigDict(from_attributes=True)

class TaskUpdate(BaseModel):
    title:str | None = None
    completed:bool | None = None

class UserRequest(BaseModel):
    name:str
    password: str

class UserResponse(BaseModel):
    id:int
    name:str
    tasks:list[TaskResponse]
    model_config=ConfigDict(from_attributes=True)

class UserCreateResponse(BaseModel):
    id:int
    name:str

class LoginRequest(BaseModel):
    name: str
    password: str