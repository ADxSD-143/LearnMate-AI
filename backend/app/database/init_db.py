from app.database.session import Base, engine

from app.models.subject import Subject
from app.models.topic import Topic
from app.models.task import Task
from app.models.college import College
from app.models.branch import Branch
from app.models.user import User
from app.models.document import Document, DocumentChunk
from app.models.quiz import QuizQuestion, QuizAttempt

def init_db():
    Base.metadata.create_all(bind=engine)
