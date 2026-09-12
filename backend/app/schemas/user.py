from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.schemas.college import CollegeOut
from app.schemas.branch import BranchOut

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    email: EmailStr
    semester: int = Field(..., ge=1, le=12, description="Current semester (1-12)")
    college_id: Optional[int] = None
    branch_id: Optional[int] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)

class UserOut(UserBase):
    id: int
    college: Optional[CollegeOut] = None
    branch: Optional[BranchOut] = None

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
