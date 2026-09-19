from pwdlib import PasswordHash
from dotenv import load_dotenv
import os
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException
from database import get_db
from models import User
from datetime import datetime,timedelta,timezone

load_dotenv()

pwd_hash=PasswordHash.recommended()

SECRET_KEY=os.getenv("SECRET_KEY")

def create_access_token(user_id:int)->str:
    now=datetime.now(timezone.utc)
    payload={
        "sub":str(user_id),
        "iat":now,
        "exp":now+timedelta(minutes=30)
    }
    token=jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )
    return token

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def decode_access_token(token:str):
    payload=jwt.decode(
        token,
        SECRET_KEY,
        algorithms="HS256"
        )
    return payload

def get_current_user(token:str=Depends(oauth2_scheme),db=Depends(get_db)):
    
    try:
        payload=decode_access_token(token)
        user_id=int(payload["sub"])
    except(jwt.InvalidTokenError,KeyError,ValueError):
        raise HTTPException(status_code=401,detail="invalid authentication credentials")
    db_user=db.get(User,user_id)
    if db_user is None:
        raise HTTPException(status_code=404,detail="user not found")
    return db_user