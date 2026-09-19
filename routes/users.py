from fastapi import APIRouter,Depends,HTTPException
from schemas import UserRequest,UserResponse,UserCreateResponse,LoginRequest
from database import get_db
from models import User
from sqlalchemy import select
from security import pwd_hash,create_access_token,get_current_user
router=APIRouter()


@router.get("/users/me",response_model=UserResponse)
def read_current_user(current_user:User=Depends(get_current_user)):
    return current_user

@router.post("/users",response_model=UserCreateResponse)
def create_user(user:UserRequest,db=Depends(get_db))->UserCreateResponse:
    password_hash=pwd_hash.hash(user.password)
    db_user=User(
        name=user.name,
        password_hash=password_hash
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login(credentials:LoginRequest,db=Depends(get_db))->dict[str,str]:
    statement=(
        select(User)
        .where(User.name==credentials.name)
    )
    result=db.execute(statement)
    db_user=result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=401,detail="invalid credentials")
    if pwd_hash.verify(credentials.password,db_user.password_hash):
        access_token=create_access_token(db_user.id)
        return{
            "access_token":access_token,
            "token_type":"bearer"
        }
    else:
        raise HTTPException(status_code=401,detail="invalid credentials")


@router.delete("/users/me",response_model=dict[str,str])
def delete_user(db=Depends(get_db),current_user:User=Depends(get_current_user))->dict[str,str]:
    
    db.delete(current_user)
    db.commit()
    return {"message":"user deleted"}

