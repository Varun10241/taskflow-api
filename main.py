from fastapi import FastAPI
from routes.tasks import router as task_router
from routes.users import router as user_router
from database import Base,engine
import models
Base.metadata.create_all(engine)
app=FastAPI(title="TaskFlow API")
app.include_router(task_router)
app.include_router(user_router)


