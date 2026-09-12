from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class SubjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class SubjectOut(SubjectBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
