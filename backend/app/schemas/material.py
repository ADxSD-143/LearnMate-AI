from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DocumentOut(BaseModel):
    id: int
    user_id: int
    title: str
    original_filename: str
    stored_filename: str
    content_type: Optional[str] = None
    file_size_bytes: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentQuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


class DocumentQuestionResponse(BaseModel):
    question: str
    answer: str
    document_id: int
    relevant_chunks: list[str]


class StudyToolRequest(BaseModel):
    artifact_type: str = "summary"
    max_items: int = 5


class StudyToolResponse(BaseModel):
    document_id: int
    artifact_type: str
    title: str
    content: str
    items: list[str]
