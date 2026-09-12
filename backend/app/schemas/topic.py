from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class TopicBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)

class TopicCreate(TopicBase):
    subject_id: int

class TopicUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)

class TopicOut(TopicBase):
    id: int
    subject_id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
