from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.models.user import User
from app.schemas.subject import SubjectCreate, SubjectUpdate, SubjectOut
from app.services.subject_service import (
    get_user_subjects,
    get_user_subject_by_id,
    create_user_subject,
    update_user_subject,
    delete_user_subject,
)
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[SubjectOut])
def list_subjects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_subjects(db, user_id=current_user.id, skip=skip, limit=limit)

@router.post("/", response_model=SubjectOut, status_code=status.HTTP_201_CREATED)
def add_subject(
    data: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_user_subject(db, user_id=current_user.id, data=data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{subject_id}", response_model=SubjectOut)
def read_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    subject = get_user_subject_by_id(db, user_id=current_user.id, subject_id=subject_id)
    if not subject:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
    return subject

@router.put("/{subject_id}", response_model=SubjectOut)
def edit_subject(
    subject_id: int,
    data: SubjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_user_subject(db, user_id=current_user.id, subject_id=subject_id, data=data)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        delete_user_subject(db, user_id=current_user.id, subject_id=subject_id)
        return None
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
