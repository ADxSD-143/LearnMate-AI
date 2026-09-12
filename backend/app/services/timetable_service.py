from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import TimetableEntry, Subject
from app.schemas.timetable import TimetableCreate, TimetableUpdate
from app.services.subject_service import get_user_subject_by_id

def get_user_timetable(
    db: Session,
    user_id: int,
    day_of_week: Optional[str] = None
) -> List[TimetableEntry]:
    stmt = select(TimetableEntry).where(TimetableEntry.user_id == user_id)
    if day_of_week:
        stmt = stmt.where(TimetableEntry.day_of_week == day_of_week)
    stmt = stmt.order_by(TimetableEntry.day_of_week, TimetableEntry.start_time)
    return db.execute(stmt).scalars().all()

def get_user_timetable_entry_by_id(
    db: Session,
    user_id: int,
    entry_id: int
) -> Optional[TimetableEntry]:
    stmt = select(TimetableEntry).where(
        TimetableEntry.id == entry_id,
        TimetableEntry.user_id == user_id
    )
    return db.execute(stmt).scalar_one_or_none()

def create_timetable_entry(
    db: Session,
    user_id: int,
    data: TimetableCreate
) -> TimetableEntry:
    # Verify subject belongs to user
    subject = get_user_subject_by_id(db, user_id=user_id, subject_id=data.subject_id)
    if not subject:
        raise KeyError(f"Subject with id {data.subject_id} not found or access denied.")

    entry = TimetableEntry(
        user_id=user_id,
        subject_id=data.subject_id,
        day_of_week=data.day_of_week,
        start_time=data.start_time,
        end_time=data.end_time,
        room_number=data.room_number,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def update_timetable_entry(
    db: Session,
    user_id: int,
    entry_id: int,
    data: TimetableUpdate
) -> TimetableEntry:
    entry = get_user_timetable_entry_by_id(db, user_id=user_id, entry_id=entry_id)
    if not entry:
        raise KeyError(f"Timetable entry with id {entry_id} not found or access denied.")

    if data.day_of_week is not None:
        entry.day_of_week = data.day_of_week
    if data.start_time is not None:
        entry.start_time = data.start_time
    if data.end_time is not None:
        entry.end_time = data.end_time
    if data.room_number is not None:
        entry.room_number = data.room_number

    db.commit()
    db.refresh(entry)
    return entry

def delete_timetable_entry(
    db: Session,
    user_id: int,
    entry_id: int
) -> bool:
    entry = get_user_timetable_entry_by_id(db, user_id=user_id, entry_id=entry_id)
    if not entry:
        raise KeyError(f"Timetable entry with id {entry_id} not found or access denied.")

    db.delete(entry)
    db.commit()
    return True
