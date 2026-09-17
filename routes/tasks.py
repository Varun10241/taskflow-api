from fastapi import APIRouter,HTTPException,Depends
from schemas import TaskResponse, TaskRequest, TaskUpdate
from database import get_db
from models import Task
from sqlalchemy import select
router=APIRouter()

@router.get("/tasks",response_model=list[TaskResponse])
def read_tasks(db=Depends(get_db))-> list[TaskResponse]:
    return db.query(Task).all()

@router.get("/tasks/{task_id}",response_model=TaskResponse)
def read_task(task_id:int,db=Depends(get_db))-> TaskResponse:
    db_task=db.get(Task,task_id)
    if db_task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    return db_task

@router.put("/tasks/{task_id}",response_model=TaskResponse)
def update_task(task_id:int,updated:TaskRequest,db=Depends(get_db))->TaskResponse:
    db_task=db.get(Task,task_id)
    if db_task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    db_task.title=updated.title
    db_task.completed=updated.completed
    db.commit()
    db.refresh(db_task)
    return db_task

@router.patch("/tasks/{task_id}",response_model=TaskResponse)
def patch_task(task_id:int,updated:TaskUpdate,db=Depends(get_db))->TaskResponse:
    db_task=db.get(Task,task_id)
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
    db_task=db.get(Task,task_id)
    if db_task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    db.delete(db_task)
    db.commit()
    return{"message":"Task deleted"}

@router.get("/tasks/latest",response_model=list[TaskResponse])
def get_latest_tasks(limit:int,db=Depends(get_db))->list[TaskResponse]:
    statement=(select(Task).order_by(Task.id.desc()).limit(limit))
    result=db.execute(statement)
    return result.scalars().all()

@router.get("/tasks/completed", response_model=list[TaskResponse])
def get_completed_tasks(db=Depends(get_db)) -> list[TaskResponse]:

    statement = select(Task).where(
        Task.completed == True
        )

    result = db.execute(statement)

    return result.scalars().all()