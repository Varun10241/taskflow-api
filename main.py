from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
app=FastAPI(title="TaskFlow API")

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

tasks=[]
curr_id=0
@app.get("/tasks",response_model=list[Task])
def read_tasks()-> list[Task]:
    return tasks

@app.get("/tasks/{task_id}",response_model=Task)
def read_task(task_id:int)-> Task:
    for t in tasks:
        if(t.id==task_id):
            return t;
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks",response_model=Task)
def create_task(task:TaskRequest) -> Task:
    global curr_id
    new_id=curr_id+1
    curr_id+=1
    new_task=Task(
        id=new_id,
        title=task.title,
        completed=task.completed
    )
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}",response_model=Task)
def update_task(task_id:int,updated:TaskRequest)->Task:
    for t in tasks:
        if t.id == task_id:
            t.title=updated.title
            t.completed=updated.completed
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/tasks/{task_id}",response_model=Task)
def patch_task(task_id:int,updated:TaskUpdate)->Task:
    for t in tasks:
        if t.id == task_id:
            if updated.title is not None:
                t.title=updated.title
            if updated.completed is not None:
                t.completed=updated.completed
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id:int)->dict[str,str]:
    for t in tasks:
        if t.id == task_id:
            tasks.remove(t)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
