from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Topic, Subject
from app.schemas.topic import TopicCreate, TopicUpdate
from app.services.subject_service import get_user_subject_by_id

def get_subject_topics(db: Session, user_id: int, subject_id: int) -> List[Topic]:
    """Retrieve all topics under a subject, verifying that the subject belongs to user_id."""
    subject = get_user_subject_by_id(db, user_id=user_id, subject_id=subject_id)
    if not subject:
        raise KeyError(f"Subject with id {subject_id} not found or access denied.")

    stmt = select(Topic).where(Topic.subject_id == subject_id)
    return db.execute(stmt).scalars().all()

def get_user_topic_by_id(db: Session, user_id: int, topic_id: int) -> Optional[Topic]:
    """Retrieve a topic by ID, ensuring the parent subject belongs to the current user."""
    stmt = (
        select(Topic)
        .join(Subject, Topic.subject_id == Subject.id)
        .where(Topic.id == topic_id, Subject.user_id == user_id)
    )
    return db.execute(stmt).scalar_one_or_none()

def create_topic(db: Session, user_id: int, data: TopicCreate) -> Topic:
    """Create a topic under a subject, enforcing ownership and uniqueness."""
    subject = get_user_subject_by_id(db, user_id=user_id, subject_id=data.subject_id)
    if not subject:
        raise KeyError(f"Subject with id {data.subject_id} not found or access denied.")

    clean_name = data.name.strip()
    # Check duplicate topic in subject
    existing_stmt = select(Topic).where(
        Topic.subject_id == data.subject_id,
        Topic.name.ilike(clean_name)
    )
    if db.execute(existing_stmt).scalar_one_or_none():
        raise ValueError(f"Topic '{clean_name}' already exists in this subject.")

    topic = Topic(name=clean_name, subject_id=data.subject_id)
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic

def update_topic(db: Session, user_id: int, topic_id: int, data: TopicUpdate) -> Topic:
    """Update topic name with ownership and uniqueness checks."""
    topic = get_user_topic_by_id(db, user_id=user_id, topic_id=topic_id)
    if not topic:
        raise KeyError(f"Topic with id {topic_id} not found or access denied.")

    if data.name is not None:
        clean_name = data.name.strip()
        existing_stmt = select(Topic).where(
            Topic.subject_id == topic.subject_id,
            Topic.name.ilike(clean_name)
        )
        existing = db.execute(existing_stmt).scalar_one_or_none()
        if existing and existing.id != topic_id:
            raise ValueError(f"Topic '{clean_name}' already exists in this subject.")
        topic.name = clean_name

    db.commit()
    db.refresh(topic)
    return topic

def delete_topic(db: Session, user_id: int, topic_id: int) -> bool:
    """Delete topic cascadingly, ensuring ownership."""
    topic = get_user_topic_by_id(db, user_id=user_id, topic_id=topic_id)
    if not topic:
        raise KeyError(f"Topic with id {topic_id} not found or access denied.")

    db.delete(topic)
    db.commit()
    return True
