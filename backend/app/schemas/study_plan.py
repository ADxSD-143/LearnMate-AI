from pydantic import BaseModel, Field


class StudyPlanItem(BaseModel):
    day: int
    topic: str
    duration_minutes: int
    focus: str


class StudyPlanResponse(BaseModel):
    plan: list[StudyPlanItem] = Field(default_factory=list)
    focus_areas: list[str] = Field(default_factory=list)
