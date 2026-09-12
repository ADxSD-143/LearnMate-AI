from typing import Optional, List
from datetime import date as dt_date, datetime
from pydantic import BaseModel, ConfigDict, Field

class AttendanceRecordBase(BaseModel):
    subject_id: int
    timetable_entry_id: Optional[int] = None
    date: dt_date = Field(default_factory=dt_date.today)
    status: str = Field(..., pattern="^(Present|Absent|Cancelled)$")
    notes: Optional[str] = None

class AttendanceRecordCreate(AttendanceRecordBase):
    pass

class AttendanceRecordUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(Present|Absent|Cancelled)$")
    notes: Optional[str] = None

class AttendanceRecordOut(AttendanceRecordBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class SubjectAttendanceStats(BaseModel):
    subject_id: int
    subject_name: str
    total_conducted: int
    total_attended: int
    total_absent: int
    total_cancelled: int
    percentage: float
    target_percentage: float = 75.0
    is_shortage: bool
    bunks_available: int
    classes_needed_to_reach_target: int

class OverallAttendanceSummary(BaseModel):
    total_classes_conducted: int
    total_classes_attended: int
    overall_percentage: float
    subjects_stats: List[SubjectAttendanceStats]
