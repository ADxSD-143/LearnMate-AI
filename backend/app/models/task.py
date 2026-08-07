from sqlalchemy import Column, ForeignKey, Integer, String

from app.database.session import Base
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    title = Column(String, nullable=False)

    topic = relationship(
        "Topic",
        back_populates="tasks"
    )