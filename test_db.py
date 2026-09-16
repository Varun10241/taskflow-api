from database import SessionLocal
from models import Task

db = SessionLocal()

task=db.get(Task,1)

print(task.id)
print(task.title)
print(task.completed)

db.close()
