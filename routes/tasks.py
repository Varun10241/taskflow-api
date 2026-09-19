from fastapi import APIRouter,HTTPException,Depends
from schemas import TaskResponse, TaskRequest, TaskUpdate
from database import get_db
from models import Task,User
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from security import get_current_user
router=APIRouter()

@router.get("/tasks",response_model=list[TaskResponse])
def read_tasks(current_user:User=Depends(get_current_user))-> list[TaskResponse]:
    return current_user.tasks

@router.get("/tasks/{task_id}",response_model=TaskResponse)
def read_task(task_id:int,db=Depends(get_db),current_user:User=Depends(get_current_user))-> TaskResponse:
    db_task=db.get(Task,task_id)
    if db_task is None:
        raise HTTPException(status_code=404,detail="task not found")
    if db_task.user_id!=current_user.id:
        raise HTTPException(status_code=403,detail="forbidden")
    return db_task

@router.post("/tasks",response_model=TaskResponse)
def create_task(task:TaskRequest,db=Depends(get_db),current_user:User=Depends(get_current_user))->TaskResponse:
    db_task=Task(
         title=task.title,
         completed=task.completed
    )
    current_user.tasks.append(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
     
@router.put("/tasks/{task_id}",response_model=TaskResponse)
def update_task(task_id:int,updated:TaskRequest,db=Depends(get_db),current_user:User=Depends(get_current_user))->TaskResponse:
    db_task=db.get(Task,task_id)
    if db_task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    if current_user.id !=db_task.user_id:
        raise HTTPException(status_code=403,detail="forbidden")
    db_task.title=updated.title
    db_task.completed=updated.completed
    db.commit()
    db.refresh(db_task)
    return db_task

@router.patch("/tasks/{task_id}",response_model=TaskResponse)
def patch_task(task_id:int,updated:TaskUpdate,db=Depends(get_db),current_user:User=Depends(get_current_user))->TaskResponse:
    db_task=db.get(Task,task_id)
    if db_task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    if current_user.id !=db_task.user_id:
            raise HTTPException(status_code=403,detail="forbidden")
    if updated.title is not None:
        db_task.title=updated.title
    if updated.completed is not None:
        db_task.completed=updated.completed
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id:int,db=Depends(get_db),current_user:User=Depends(get_current_user))->dict[str,str]:
    db_task=db.get(Task,task_id)
    if db_task is None:
        raise HTTPException(status_code=404,detail="Task not found")
    if current_user.id !=db_task.user_id:
                raise HTTPException(status_code=403,detail="forbidden")
    db.delete(db_task)
    db.commit()
    return{"message":"Task deleted"}

@router.get("/tasks/latest",response_model=list[TaskResponse])
def get_latest_tasks(limit:int,db=Depends(get_db),current_user:User=Depends(get_current_user))->list[TaskResponse]:
    statement=(select(Task)
               .where(Task.user_id==current_user.id)
               .order_by(Task.id.desc()).limit(limit))
    result=db.execute(statement)
    return result.scalars().all()

@router.get("/tasks/completed", response_model=list[TaskResponse])
def get_completed_tasks(db=Depends(get_db),current_user:User=Depends(get_current_user)) -> list[TaskResponse]:

    statement = select(Task).where(
        Task.user_id==current_user.id,
        Task.completed == True
        )

    result = db.execute(statement)

    return result.scalars().all()