from datetime import datetime

from pydantic import BaseModel
class Task(BaseModel):
    title: str
    completed: bool = False
    priority: str
    deadline: str | None = None



