from pydantic import BaseModel, ConfigDict, Field

class BranchBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full branch name, e.g. Computer Science Engineering")
    code: str = Field(..., min_length=2, max_length=20, description="Branch code, e.g. CSE")

class BranchCreate(BranchBase):
    pass

class BranchOut(BranchBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
