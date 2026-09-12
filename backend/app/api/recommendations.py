from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.base import get_db
from app.models.user import User
from app.schemas.recommendation import RecommendationSummary
from app.services.recommendation_service import build_learning_profile, build_personalized_recommendations

router = APIRouter()


@router.get("/", response_model=RecommendationSummary)
def get_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = build_learning_profile(db, user_id=current_user.id)
    return RecommendationSummary(
        recommendations=build_personalized_recommendations(db, user_id=current_user.id),
        weak_topics=profile["weak_topics"],
        overall_attendance=profile["overall_attendance"],
    )
