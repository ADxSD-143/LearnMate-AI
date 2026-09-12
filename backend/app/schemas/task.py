from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: str = Field("Medium", pattern="^(Low|Medium|High)$")
    status: str = Field("Pending", pattern="^(Pending|In Progress|Completed)$")
    deadline: Optional[datetime] = None

class TaskCreate(TaskBase):
    topic_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[str] = Field(None, pattern="^(Low|Medium|High)$")
    status: Optional[str] = Field(None, pattern="^(Pending|In Progress|Completed)$")
    deadline: Optional[datetime] = None

class TaskOut(TaskBase):
    id: int
    topic_id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
