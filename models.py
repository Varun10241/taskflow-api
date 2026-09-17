from sqlalchemy import Boolean,String,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship
from database import Base
class Task(Base):
    __tablename__="tasks"
    id:Mapped[int]=mapped_column(primary_key=True)
    title:Mapped[str]=mapped_column(String)
    completed:Mapped[bool]=mapped_column(Boolean)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"))
    user:Mapped["User"]=relationship(back_populates="tasks")

class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String,unique=True,nullable=False)
    tasks:Mapped[list["Task"]]=relationship(back_populates="user",cascade="all, delete-orphan")
