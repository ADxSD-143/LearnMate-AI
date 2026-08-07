from app.database.session import Base, engine

from app.models.subject import Subject
from app.models.topic import Topic
from app.models.task import Task


def init_db():
    Base.metadata.create_all(bind=engine)