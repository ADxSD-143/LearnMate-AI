from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.base import get_db
from app.models.user import User
from app.schemas.quiz import QuizAttemptOut, QuizAttemptSubmit, QuizQuestionCreate, QuizQuestionOut, WeakTopicOut
from app.services.quiz_service import (
    create_quiz_question,
    get_user_quiz_attempts,
    get_user_quiz_questions,
    get_user_weak_topics,
    submit_quiz_attempt,
)

router = APIRouter()


@router.post("/questions", response_model=QuizQuestionOut, status_code=status.HTTP_201_CREATED)
def add_quiz_question(
    data: QuizQuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_quiz_question(db, user_id=current_user.id, data=data)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/questions", response_model=List[QuizQuestionOut])
def list_quiz_questions(
    topic_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_quiz_questions(db, user_id=current_user.id, topic_id=topic_id, skip=skip, limit=limit)


@router.post("/attempts", response_model=QuizAttemptOut, status_code=status.HTTP_201_CREATED)
def submit_attempt(
    data: QuizAttemptSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return submit_quiz_attempt(db, user_id=current_user.id, payload=data)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/attempts", response_model=List[QuizAttemptOut])
def list_attempts(
    topic_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_quiz_attempts(db, user_id=current_user.id, topic_id=topic_id, skip=skip, limit=limit)


@router.get("/weak-topics", response_model=List[WeakTopicOut])
def list_weak_topics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_weak_topics(db, user_id=current_user.id)
