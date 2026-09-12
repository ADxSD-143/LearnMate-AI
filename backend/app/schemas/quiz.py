from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class QuizQuestionBase(BaseModel):
    topic_id: int
    question_text: str = Field(..., min_length=1, max_length=500)
    option_a: str = Field(..., min_length=1, max_length=255)
    option_b: str = Field(..., min_length=1, max_length=255)
    option_c: str = Field(..., min_length=1, max_length=255)
    option_d: str = Field(..., min_length=1, max_length=255)
    correct_option: str = Field(..., pattern="^[ABCD]$")
    difficulty: str = Field("Medium", pattern="^(Easy|Medium|Hard)$")


class QuizQuestionCreate(QuizQuestionBase):
    pass


class QuizQuestionOut(QuizQuestionBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class QuizAttemptSubmit(BaseModel):
    topic_id: int
    answers: dict[str, str] = Field(..., description="Map of question_id as string to selected option A-D")


class QuizAttemptOut(BaseModel):
    id: int
    user_id: int
    topic_id: int
    questions_total: int
    questions_correct: int
    percentage: float
    submitted_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WeakTopicOut(BaseModel):
    topic_id: int
    topic_name: str
    average_score: float
    attempts: int
    status: str
