from app.models.college import College
from app.models.branch import Branch
from app.models.user import User
from app.models.subject import Subject
from app.models.topic import Topic
from app.models.task import Task
from app.models.timetable import TimetableEntry
from app.models.attendance import AttendanceRecord
from app.models.document import Document, DocumentChunk
from app.models.quiz import QuizQuestion, QuizAttempt

__all__ = [
    "College",
    "Branch",
    "User",
    "Subject",
    "Topic",
    "Task",
    "TimetableEntry",
    "AttendanceRecord",
    "Document",
    "DocumentChunk",
    "QuizQuestion",
    "QuizAttempt",
]
