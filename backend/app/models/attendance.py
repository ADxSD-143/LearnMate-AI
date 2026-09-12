from datetime import datetime, timezone, date
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.session import Base

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    timetable_entry_id = Column(Integer, ForeignKey("timetable_entries.id", ondelete="SET NULL"), nullable=True, index=True)
    date = Column(Date, nullable=False, default=date.today)
    status = Column(String(20), nullable=False) # Present, Absent, Cancelled
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="attendance_records")
    subject = relationship("Subject", back_populates="attendance_records")
    timetable_entry = relationship("TimetableEntry", back_populates="attendance_records")
