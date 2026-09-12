from pydantic import BaseModel, Field


class RecommendationSummary(BaseModel):
    recommendations: list[str] = Field(default_factory=list)
    weak_topics: list[dict] = Field(default_factory=list)
    overall_attendance: float = 0.0


class RecommendationOut(RecommendationSummary):
    user_id: int
