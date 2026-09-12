from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class TimetableBase(BaseModel):
    subject_id: int
    day_of_week: str = Field(..., pattern="^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)$")
    start_time: str = Field(..., pattern="^([01]?[0-9]|2[0-3]):[0-5][0-9]$", description="HH:MM in 24-hr format")
    end_time: str = Field(..., pattern="^([01]?[0-9]|2[0-3]):[0-5][0-9]$", description="HH:MM in 24-hr format")
    room_number: Optional[str] = Field(None, max_length=50)

class TimetableCreate(TimetableBase):
    pass

class TimetableUpdate(BaseModel):
    day_of_week: Optional[str] = Field(None, pattern="^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)$")
    start_time: Optional[str] = Field(None, pattern="^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
    end_time: Optional[str] = Field(None, pattern="^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
    room_number: Optional[str] = Field(None, max_length=50)

class TimetableOut(TimetableBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
