from fastapi import APIRouter

from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.prediction_service import generate_prediction
from app.services.recommendation_service import build_recommendations

router = APIRouter()


@router.post("/", response_model=PredictionResponse)
def predict_performance(payload: PredictionRequest) -> PredictionResponse:
    predicted_score = generate_prediction(payload.features)
    recommendations = build_recommendations(predicted_score)
    return PredictionResponse(
        predicted_score=predicted_score,
        recommendations=recommendations,
    )
