from fastapi import FastAPI

from app.api.subjects import router as subject_router
from app.database.init_db import init_db

app = FastAPI()

init_db()
@app.get("/")
def home():
    return {"message": "Welcome to LearnMate AI 🚀"}


app.include_router(
    subject_router,
    prefix="/subjects",
    tags=["Subjects"]
)

