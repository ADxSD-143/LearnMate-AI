from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Student learning signals used by the current prediction scaffold.

    This is intentionally a simple rule-based baseline: it provides a consistent
    API contract while clearly separating the current scaffold from a production
    ML model pipeline.
    """

    study_hours: float = Field(..., ge=0)
    revision_hours: float = Field(..., ge=0)
    attendance: float = Field(..., ge=0, le=100)
    quiz_score: float = Field(..., ge=0, le=100)
    mock_test_score: float = Field(..., ge=0, le=100)
    assignments_completed: int = Field(..., ge=0)

    @property
    def features(self) -> dict[str, float | int]:
        return {
            "study_hours": self.study_hours,
            "revision_hours": self.revision_hours,
            "attendance": self.attendance,
            "quiz_score": self.quiz_score,
            "mock_test_score": self.mock_test_score,
            "assignments_completed": self.assignments_completed,
        }


class PredictionResponse(BaseModel):
    predicted_score: float
    recommendations: list[str]
