from database import SessionLocal
from models import User, Task

db = SessionLocal()

user = User(name="Cascade Test")

task = Task(
    title="Task to be deleted",
    completed=False
)

user.tasks.append(task)

db.add(user)
db.commit()

print("User ID:", user.id)
print("Task ID:", task.id)
db.delete(user)
db.commit()
print("User deleted")
remaining_task = db.get(Task, task.id)

print("Task after user deletion:", remaining_task)

db.close()