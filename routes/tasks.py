from fastapi import APIRouter,HTTPException,Depends
from schemas import Task, TaskRequest, TaskUpdate
from database import get_db
from models import Task as TaskModel
router=APIRouter()

@router.get("/tasks",response_model=list[Task])
def read_tasks(db=Depends(get_db))-> list[Task]:
    return db.query(TaskModel).all()

@router.get("/tasks/{task_id}",response_model=Task)
def read_task(task_id:int,db=Depends(get_db))-> Task:
    db_task=db.get(TaskModel,task_id)
    if db_task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    return db_task

@router.post("/tasks",response_model=Task)
def create_task(task:TaskRequest,db=Depends(get_db)) -> Task:
    
   db_task=TaskModel(
       title=task.title,
       completed=task.completed
   )
   db.add(db_task)
   db.commit()
   db.refresh(db_task)
   return db_task

@router.put("/tasks/{task_id}",response_model=Task)
def update_task(task_id:int,updated:TaskRequest,db=Depends(get_db))->Task:
    db_task=db.get(TaskModel,task_id)
    if db_task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    db_task.title=updated.title
    db_task.completed=updated.completed
    db.commit()
    db.refresh(db_task)
    return db_task

@router.patch("/tasks/{task_id}",response_model=Task)
def patch_task(task_id:int,updated:TaskUpdate,db=Depends(get_db))->Task:
    db_task=db.get(TaskModel,task_id)
    if db_task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    if updated.title is not None:
        db_task.title=updated.title
    if updated.completed is not None:
        db_task.completed=updated.completed
    db.commit()
    db.refresh(db_task)
    return db_task
@router.delete("/tasks/{task_id}")
def delete_task(task_id:int,db=Depends(get_db))->dict[str,str]:
    db_task=db.get(TaskModel,task_id)
    if db_task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    db.delete(db_task)
    db.commit()
    return{"message":"Task deleted"}
