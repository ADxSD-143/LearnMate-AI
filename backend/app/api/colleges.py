from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.base import get_db
from app.schemas.college import CollegeCreate, CollegeOut
from app.services.college_service import (
    get_colleges,
    get_college_by_id,
    create_college,
    seed_default_colleges
)

router = APIRouter()

@router.get("/", response_model=List[CollegeOut])
def list_colleges(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_colleges(db, skip=skip, limit=limit)

@router.post("/", response_model=CollegeOut, status_code=status.HTTP_201_CREATED)
def add_college(data: CollegeCreate, db: Session = Depends(get_db)):
    try:
        return create_college(db, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"College '{data.name}' or domain '{data.email_domain}' already exists."
        )

@router.get("/{college_id}", response_model=CollegeOut)
def read_college(college_id: int, db: Session = Depends(get_db)):
    college = get_college_by_id(db, college_id)
    if not college:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="College not found")
    return college

@router.post("/seed", response_model=dict)
def seed_colleges(db: Session = Depends(get_db)):
    seed_default_colleges(db)
    return {"message": "Default colleges seeded successfully"}
