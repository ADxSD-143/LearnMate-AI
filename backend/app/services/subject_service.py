from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Subject
from app.schemas.subject import SubjectCreate, SubjectUpdate

def get_user_subjects(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Subject]:
    """Retrieve all subjects owned by the specified user."""
    stmt = select(Subject).where(Subject.user_id == user_id).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()

def get_user_subject_by_id(db: Session, user_id: int, subject_id: int) -> Optional[Subject]:
    """Retrieve a specific subject by ID, enforcing user ownership."""
    stmt = select(Subject).where(Subject.id == subject_id, Subject.user_id == user_id)
    return db.execute(stmt).scalar_one_or_none()

def get_user_subject_by_name(db: Session, user_id: int, name: str) -> Optional[Subject]:
    """Check if the user already has a subject with the given name (case-insensitive)."""
    stmt = select(Subject).where(Subject.user_id == user_id, Subject.name.ilike(name.strip()))
    return db.execute(stmt).scalar_one_or_none()

def create_user_subject(db: Session, user_id: int, data: SubjectCreate) -> Subject:
    """Create a new subject under the user's account with composite uniqueness validation."""
    clean_name = data.name.strip()
    existing = get_user_subject_by_name(db, user_id=user_id, name=clean_name)
    if existing:
        raise ValueError(f"Subject '{clean_name}' already exists for this user.")

    subject = Subject(name=clean_name, user_id=user_id)
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject

def update_user_subject(db: Session, user_id: int, subject_id: int, data: SubjectUpdate) -> Subject:
    """Update subject name, validating ownership and unique constraint."""
    subject = get_user_subject_by_id(db, user_id=user_id, subject_id=subject_id)
    if not subject:
        raise KeyError(f"Subject with id {subject_id} not found.")

    if data.name is not None:
        clean_name = data.name.strip()
        existing = get_user_subject_by_name(db, user_id=user_id, name=clean_name)
        if existing and existing.id != subject_id:
            raise ValueError(f"Subject '{clean_name}' already exists for this user.")
        subject.name = clean_name

    db.commit()
    db.refresh(subject)
    return subject

def delete_user_subject(db: Session, user_id: int, subject_id: int) -> bool:
    """Delete subject and its associated topics and tasks cascadingly, enforcing ownership."""
    subject = get_user_subject_by_id(db, user_id=user_id, subject_id=subject_id)
    if not subject:
        raise KeyError(f"Subject with id {subject_id} not found.")

    db.delete(subject)
    db.commit()
    return True
