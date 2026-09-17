from fastapi import APIRouter,Depends,HTTPException
from schemas import UserRequest,TaskRequest,Task as TaskResponse,User as UserResponse
from database import get_db
from models import User,Task
from sqlalchemy import select
from sqlalchemy.orm import selectinload
router=APIRouter()
@router.post("/users")
def create_user(user:UserRequest,db=Depends(get_db)):
    db_user=User(
        name=user.name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/users/{user_id}/tasks",response_model=TaskResponse)
def create_user_task(user_id:int,task:TaskRequest,db=Depends(get_db))->TaskResponse:
    db_user=db.get(User,user_id)
    if db_user is None:
        raise HTTPException(status_code=404,detail="user not found")
    db_task=Task(
        title=task.title,
        completed=task.completed
    )
    db_user.tasks.append(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/users/{user_id}",response_model=UserResponse)
def read_user(user_id:int,db=Depends(get_db)):
    db_user=db.get(User,user_id)
    if db_user is None:
        raise HTTPException(status_code=404,detail="user not found")
    return db_user

@router.get("/users/{user_id}/tasks",response_model=list[TaskResponse])
def read_user_tasks(user_id:int,db=Depends(get_db))->list[TaskResponse]:
    statement=(select(User)
    .options(selectinload(User.tasks))
    .where(User.id==user_id)
    )
    result=db.execute(statement)
    db_user=result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404,detail="user not found")
    return db_user.tasks

@router.delete("/users/{user_id}",response_model=dict[str,str])
def delete_user(user_id:int,db=Depends(get_db))->dict[str,str]:
    db_user=db.get(User,user_id)
    if db_user is None:
        raise HTTPException(status_code=404,detail="user not found")
    db.delete(db_user)
    db.commit()
    return {"message":"user deleted"}