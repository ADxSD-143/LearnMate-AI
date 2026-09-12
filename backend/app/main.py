from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database.init_db import init_db
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.colleges import router as colleges_router
from app.api.branches import router as branches_router
from app.api.subjects import router as subject_router
from app.api.topics import router as topic_router
from app.api.tasks import router as task_router
from app.api.timetable import router as timetable_router
from app.api.attendance import router as attendance_router
from app.api.health import router as health_router
from app.api.predict import router as prediction_router
from app.api.materials import router as materials_router
from app.api.quizzes import router as quizzes_router

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered personalized learning and academic management ecosystem.",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables
init_db()

@app.get("/")
def home():
    return {
        "app": settings.APP_NAME,
        "message": "Welcome to LearnMate AI 🚀",
        "docs": "/docs"
    }

# Register API Routers
app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(auth_router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Authentication"])
app.include_router(users_router, prefix=f"{settings.API_V1_PREFIX}/users", tags=["Users"])
app.include_router(colleges_router, prefix=f"{settings.API_V1_PREFIX}/colleges", tags=["Colleges"])
app.include_router(branches_router, prefix=f"{settings.API_V1_PREFIX}/branches", tags=["Branches"])
app.include_router(subject_router, prefix=f"{settings.API_V1_PREFIX}/subjects", tags=["Subjects"])
app.include_router(topic_router, prefix=f"{settings.API_V1_PREFIX}/topics", tags=["Topics"])
app.include_router(task_router, prefix=f"{settings.API_V1_PREFIX}/tasks", tags=["Tasks"])
app.include_router(timetable_router, prefix=f"{settings.API_V1_PREFIX}/timetable", tags=["Timetable"])
app.include_router(attendance_router, prefix=f"{settings.API_V1_PREFIX}/attendance", tags=["Attendance"])
app.include_router(prediction_router, prefix=f"{settings.API_V1_PREFIX}/predict", tags=["Prediction"])
app.include_router(materials_router, prefix=f"{settings.API_V1_PREFIX}/materials", tags=["Materials"])
app.include_router(quizzes_router, prefix=f"{settings.API_V1_PREFIX}/quizzes", tags=["Quizzes"])
