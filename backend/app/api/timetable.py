from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.models.user import User
from app.schemas.timetable import TimetableCreate, TimetableUpdate, TimetableOut
from app.services.timetable_service import (
    get_user_timetable,
    get_user_timetable_entry_by_id,
    create_timetable_entry,
    update_timetable_entry,
    delete_timetable_entry,
)
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TimetableOut])
def list_timetable(
    day_of_week: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_timetable(db, user_id=current_user.id, day_of_week=day_of_week)

@router.post("/", response_model=TimetableOut, status_code=status.HTTP_201_CREATED)
def add_timetable_entry(
    data: TimetableCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_timetable_entry(db, user_id=current_user.id, data=data)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{entry_id}", response_model=TimetableOut)
def read_timetable_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = get_user_timetable_entry_by_id(db, user_id=current_user.id, entry_id=entry_id)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timetable entry not found")
    return entry

@router.put("/{entry_id}", response_model=TimetableOut)
def edit_timetable_entry(
    entry_id: int,
    data: TimetableUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_timetable_entry(db, user_id=current_user.id, entry_id=entry_id, data=data)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timetable entry not found")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_timetable_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        delete_timetable_entry(db, user_id=current_user.id, entry_id=entry_id)
        return None
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timetable entry not found")
