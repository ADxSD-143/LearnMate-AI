from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import College
from app.schemas.college import CollegeCreate

def get_colleges(db: Session, skip: int = 0, limit: int = 100) -> List[College]:
    stmt = select(College).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()

def get_college_by_id(db: Session, college_id: int) -> Optional[College]:
    stmt = select(College).where(College.id == college_id)
    return db.execute(stmt).scalar_one_or_none()

def get_college_by_name(db: Session, name: str) -> Optional[College]:
    stmt = select(College).where(College.name.ilike(name))
    return db.execute(stmt).scalar_one_or_none()

def create_college(db: Session, data: CollegeCreate) -> College:
    college = College(name=data.name.strip(), email_domain=data.email_domain.strip().lower() if data.email_domain else None)
    db.add(college)
    db.commit()
    db.refresh(college)
    return college

def seed_default_colleges(db: Session) -> None:
    default_colleges = [
        {"name": "KIIT University", "email_domain": "kiit.ac.in"},
        {"name": "Delhi Technological University", "email_domain": "dtu.ac.in"},
        {"name": "Vellore Institute of Technology", "email_domain": "vit.ac.in"},
        {"name": "Indian Institute of Technology Bombay", "email_domain": "iitb.ac.in"},
        {"name": "Birla Institute of Technology and Science", "email_domain": "bits-pilani.ac.in"},
    ]
    for col_data in default_colleges:
        existing = get_college_by_name(db, col_data["name"])
        if not existing:
            college = College(name=col_data["name"], email_domain=col_data["email_domain"])
            db.add(college)
    db.commit()
