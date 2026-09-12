from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.models.user import User
from app.schemas.attendance import (
    AttendanceRecordCreate,
    AttendanceRecordUpdate,
    AttendanceRecordOut,
    SubjectAttendanceStats,
    OverallAttendanceSummary,
)
from app.services.attendance_service import (
    record_attendance,
    get_user_attendance_logs,
    get_attendance_record_by_id,
    update_attendance_record,
    delete_attendance_record,
    calculate_subject_attendance,
    calculate_overall_attendance,
)
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=AttendanceRecordOut, status_code=status.HTTP_201_CREATED)
def mark_attendance(
    data: AttendanceRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return record_attendance(db, user_id=current_user.id, data=data)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/logs", response_model=List[AttendanceRecordOut])
def list_attendance_logs(
    subject_id: Optional[int] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_attendance_logs(
        db,
        user_id=current_user.id,
        subject_id=subject_id,
        date_from=date_from,
        date_to=date_to,
        skip=skip,
        limit=limit,
    )

@router.get("/summary", response_model=OverallAttendanceSummary)
def get_attendance_summary(
    target_percentage: float = Query(75.0, ge=1.0, le=100.0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return calculate_overall_attendance(db, user_id=current_user.id, target_percentage=target_percentage)

@router.get("/subject/{subject_id}", response_model=SubjectAttendanceStats)
def get_subject_attendance(
    subject_id: int,
    target_percentage: float = Query(75.0, ge=1.0, le=100.0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return calculate_subject_attendance(
            db,
            user_id=current_user.id,
            subject_id=subject_id,
            target_percentage=target_percentage,
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{record_id}", response_model=AttendanceRecordOut)
def edit_attendance_record(
    record_id: int,
    data: AttendanceRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_attendance_record(db, user_id=current_user.id, record_id=record_id, data=data)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_attendance_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        delete_attendance_record(db, user_id=current_user.id, record_id=record_id)
        return None
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
