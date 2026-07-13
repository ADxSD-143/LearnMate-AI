from pydantic import BaseModel
"""Pydantic ek library hai jo data validation karti hai.

Jaise ML me hum data clean karte the, 
waise hi API me Pydantic ensure karta hai ki input sahi format me aaye."""

class PredictionRequest(BaseModel):
    study_hours: float
    revision_hours: float
    attendance: float
    quiz_score: float
    mock_test_score: float
    assignments_completed: int
