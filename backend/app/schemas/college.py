from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class CollegeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150, description="Canonical college name")
    email_domain: Optional[str] = Field(None, max_length=100, description="Official college email domain, e.g. kiit.ac.in")

class CollegeCreate(CollegeBase):
    pass

class CollegeOut(CollegeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
