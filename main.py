from fastapi import FastAPI
from src.routers.tasks_routers import router as task_router
from src.routers.auth_routers import router as auth_router

app = FastAPI()


app.include_router(task_router)
app.include_router(auth_router)