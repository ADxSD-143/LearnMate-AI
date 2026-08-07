from datetime import datetime

from pydantic import BaseModel
class TaskCreate(BaseModel):
    subject: str
    topic: str
    title: str
    priority: str
    deadline: str | None = None