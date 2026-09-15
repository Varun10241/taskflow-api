from fastapi import APIRouter,HTTPException
from schemas import Task, TaskRequest, TaskUpdate
import storage
router=APIRouter()

@router.get("/tasks",response_model=list[Task])
def read_tasks()-> list[Task]:
    return storage.tasks

@router.get("/tasks/{task_id}",response_model=Task)
def read_task(task_id:int)-> Task:
    for t in storage.tasks:
        if(t.id==task_id):
            return t;
    raise HTTPException(status_code=404, detail="Task not found")

@router.post("/tasks",response_model=Task)
def create_task(task:TaskRequest) -> Task:
    
    new_id=storage.curr_id+1
    storage.curr_id+=1
    new_task=Task(
        id=new_id,
        title=task.title,
        completed=task.completed
    )
    storage.tasks.append(new_task)
    return new_task

@router.put("/tasks/{task_id}",response_model=Task)
def update_task(task_id:int,updated:TaskRequest)->Task:
    for t in storage.tasks:
        if t.id == task_id:
            t.title=updated.title
            t.completed=updated.completed
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@router.patch("/tasks/{task_id}",response_model=Task)
def patch_task(task_id:int,updated:TaskUpdate)->Task:
    for t in storage.tasks:
        if t.id == task_id:
            if updated.title is not None:
                t.title=updated.title
            if updated.completed is not None:
                t.completed=updated.completed
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/tasks/{task_id}")
def delete_task(task_id:int)->dict[str,str]:
    for t in storage.tasks:
        if t.id == task_id:
            storage.tasks.remove(t)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
