from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.base import get_db
from app.models.user import User
from app.schemas.study_plan import StudyPlanResponse
from app.services.recommendation_service import generate_study_plan

router = APIRouter()


@router.get("/", response_model=StudyPlanResponse)
def get_study_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plan_items = generate_study_plan(db, user_id=current_user.id)
    return StudyPlanResponse(
        plan=plan_items,
        focus_areas=[item["topic"] for item in plan_items],
    )
