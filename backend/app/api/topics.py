from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.models.user import User
from app.schemas.topic import TopicCreate, TopicUpdate, TopicOut
from app.services.topic_service import (
    get_subject_topics,
    get_user_topic_by_id,
    create_topic,
    update_topic,
    delete_topic,
)
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TopicOut])
def list_topics(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_subject_topics(db, user_id=current_user.id, subject_id=subject_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=TopicOut, status_code=status.HTTP_201_CREATED)
def add_topic(
    data: TopicCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_topic(db, user_id=current_user.id, data=data)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{topic_id}", response_model=TopicOut)
def read_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    topic = get_user_topic_by_id(db, user_id=current_user.id, topic_id=topic_id)
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    return topic

@router.put("/{topic_id}", response_model=TopicOut)
def edit_topic(
    topic_id: int,
    data: TopicUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_topic(db, user_id=current_user.id, topic_id=topic_id, data=data)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        delete_topic(db, user_id=current_user.id, topic_id=topic_id)
        return None
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
