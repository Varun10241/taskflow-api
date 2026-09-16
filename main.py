from fastapi import FastAPI
from routes.tasks import router
from database import Base,engine
import models
Base.metadata.create_all(engine)
app=FastAPI(title="TaskFlow API")
app.include_router(router)



