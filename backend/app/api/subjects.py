from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.schemas.subject import SubjectCreate
from app.services.subject_service import create_subject

router = APIRouter()

@router.get("/")
def test():
    return {"message": "Subject API Working"}

@router.post("/")
def add_subject(
    data: SubjectCreate,
    db: Session = Depends(get_db)
):
    return create_subject(db, data)