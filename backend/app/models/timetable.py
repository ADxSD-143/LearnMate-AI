from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.session import Base

class TimetableEntry(Base):
    __tablename__ = "timetable_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    day_of_week = Column(String(15), nullable=False) # e.g. Monday, Tuesday
    start_time = Column(String(10), nullable=False)   # e.g. 10:00
    end_time = Column(String(10), nullable=False)     # e.g. 11:00
    room_number = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="timetable_entries")
    subject = relationship("Subject", back_populates="timetable_entries")
    attendance_records = relationship("AttendanceRecord", back_populates="timetable_entry")
