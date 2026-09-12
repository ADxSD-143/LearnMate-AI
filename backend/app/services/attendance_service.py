import math
from typing import List, Optional
from datetime import date
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models import AttendanceRecord, Subject, TimetableEntry
from app.schemas.attendance import (
    AttendanceRecordCreate,
    AttendanceRecordUpdate,
    SubjectAttendanceStats,
    OverallAttendanceSummary,
)
from app.services.subject_service import get_user_subject_by_id, get_user_subjects
from app.services.timetable_service import get_user_timetable_entry_by_id

def record_attendance(
    db: Session,
    user_id: int,
    data: AttendanceRecordCreate
) -> AttendanceRecord:
    # 1. Verify subject ownership
    subject = get_user_subject_by_id(db, user_id=user_id, subject_id=data.subject_id)
    if not subject:
        raise KeyError(f"Subject with id {data.subject_id} not found or access denied.")

    # 2. If timetable_entry_id is provided, verify it belongs to user & subject
    if data.timetable_entry_id is not None:
        tt_entry = get_user_timetable_entry_by_id(db, user_id=user_id, entry_id=data.timetable_entry_id)
        if not tt_entry or tt_entry.subject_id != data.subject_id:
            raise KeyError(f"Timetable entry with id {data.timetable_entry_id} is invalid for this subject.")

    record = AttendanceRecord(
        user_id=user_id,
        subject_id=data.subject_id,
        timetable_entry_id=data.timetable_entry_id,
        date=data.date,
        status=data.status,
        notes=data.notes,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_user_attendance_logs(
    db: Session,
    user_id: int,
    subject_id: Optional[int] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    skip: int = 0,
    limit: int = 100
) -> List[AttendanceRecord]:
    stmt = select(AttendanceRecord).where(AttendanceRecord.user_id == user_id)
    if subject_id is not None:
        stmt = stmt.where(AttendanceRecord.subject_id == subject_id)
    if date_from is not None:
        stmt = stmt.where(AttendanceRecord.date >= date_from)
    if date_to is not None:
        stmt = stmt.where(AttendanceRecord.date <= date_to)

    stmt = stmt.order_by(AttendanceRecord.date.desc()).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()

def get_attendance_record_by_id(
    db: Session,
    user_id: int,
    record_id: int
) -> Optional[AttendanceRecord]:
    stmt = select(AttendanceRecord).where(
        AttendanceRecord.id == record_id,
        AttendanceRecord.user_id == user_id
    )
    return db.execute(stmt).scalar_one_or_none()

def update_attendance_record(
    db: Session,
    user_id: int,
    record_id: int,
    data: AttendanceRecordUpdate
) -> AttendanceRecord:
    record = get_attendance_record_by_id(db, user_id=user_id, record_id=record_id)
    if not record:
        raise KeyError(f"Attendance record with id {record_id} not found or access denied.")

    if data.status is not None:
        record.status = data.status
    if data.notes is not None:
        record.notes = data.notes

    db.commit()
    db.refresh(record)
    return record

def delete_attendance_record(
    db: Session,
    user_id: int,
    record_id: int
) -> bool:
    record = get_attendance_record_by_id(db, user_id=user_id, record_id=record_id)
    if not record:
        raise KeyError(f"Attendance record with id {record_id} not found or access denied.")

    db.delete(record)
    db.commit()
    return True

def calculate_subject_attendance(
    db: Session,
    user_id: int,
    subject_id: int,
    target_percentage: float = 75.0
) -> SubjectAttendanceStats:
    subject = get_user_subject_by_id(db, user_id=user_id, subject_id=subject_id)
    if not subject:
        raise KeyError(f"Subject with id {subject_id} not found or access denied.")

    records = db.execute(
        select(AttendanceRecord).where(
            AttendanceRecord.user_id == user_id,
            AttendanceRecord.subject_id == subject_id
        )
    ).scalars().all()

    attended = sum(1 for r in records if r.status == "Present")
    absent = sum(1 for r in records if r.status == "Absent")
    cancelled = sum(1 for r in records if r.status == "Cancelled")
    conducted = attended + absent

    target_rate = target_percentage / 100.0

    if conducted == 0:
        pct = 100.0
        is_shortage = False
        bunks_available = 0
        classes_needed = 0
    else:
        pct = round((attended / conducted) * 100, 2)
        is_shortage = pct < target_percentage

        if is_shortage:
            # Classes needed to reach target_rate:
            # (attended + c) / (conducted + c) >= target_rate
            # c = ceil((target_rate * conducted - attended) / (1 - target_rate))
            diff = (target_rate * conducted) - attended
            classes_needed = max(0, math.ceil(diff / (1.0 - target_rate)))
            bunks_available = 0
        else:
            # Bunks available without dropping below target_rate:
            # attended / (conducted + b) >= target_rate
            # b = floor(attended / target_rate - conducted)
            b = math.floor(attended / target_rate - conducted)
            bunks_available = max(0, int(b))
            classes_needed = 0

    return SubjectAttendanceStats(
        subject_id=subject.id,
        subject_name=subject.name,
        total_conducted=conducted,
        total_attended=attended,
        total_absent=absent,
        total_cancelled=cancelled,
        percentage=pct,
        target_percentage=target_percentage,
        is_shortage=is_shortage,
        bunks_available=bunks_available,
        classes_needed_to_reach_target=classes_needed,
    )

def calculate_overall_attendance(
    db: Session,
    user_id: int,
    target_percentage: float = 75.0
) -> OverallAttendanceSummary:
    subjects = get_user_subjects(db, user_id=user_id)
    subjects_stats = [
        calculate_subject_attendance(db, user_id=user_id, subject_id=s.id, target_percentage=target_percentage)
        for s in subjects
    ]

    total_conducted = sum(s.total_conducted for s in subjects_stats)
    total_attended = sum(s.total_attended for s in subjects_stats)

    overall_pct = round((total_attended / total_conducted) * 100, 2) if total_conducted > 0 else 100.0

    return OverallAttendanceSummary(
        total_classes_conducted=total_conducted,
        total_classes_attended=total_attended,
        overall_percentage=overall_pct,
        subjects_stats=subjects_stats,
    )
