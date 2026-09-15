from fastapi import FastAPI,HTTPException
from routes.tasks import router
app=FastAPI(title="TaskFlow API")
app.include_router(router)



