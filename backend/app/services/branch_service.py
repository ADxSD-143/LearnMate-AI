from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Branch
from app.schemas.branch import BranchCreate

def get_branches(db: Session, skip: int = 0, limit: int = 100) -> List[Branch]:
    stmt = select(Branch).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()

def get_branch_by_id(db: Session, branch_id: int) -> Optional[Branch]:
    stmt = select(Branch).where(Branch.id == branch_id)
    return db.execute(stmt).scalar_one_or_none()

def get_branch_by_code(db: Session, code: str) -> Optional[Branch]:
    stmt = select(Branch).where(Branch.code.ilike(code))
    return db.execute(stmt).scalar_one_or_none()

def create_branch(db: Session, data: BranchCreate) -> Branch:
    branch = Branch(name=data.name.strip(), code=data.code.strip().upper())
    db.add(branch)
    db.commit()
    db.refresh(branch)
    return branch

def seed_default_branches(db: Session) -> None:
    canonical_branches = [
        {"name": "Computer Science Engineering", "code": "CSE"},
        {"name": "Civil Engineering", "code": "CE"},
        {"name": "Mechanical Engineering", "code": "ME"},
        {"name": "Electrical Engineering", "code": "EE"},
        {"name": "Chemical Engineering", "code": "CHE"},
        {"name": "Electronics & Communication", "code": "ECE"},
        {"name": "Information Technology", "code": "IT"},
    ]
    for b in canonical_branches:
        existing = get_branch_by_code(db, b["code"])
        if not existing:
            branch = Branch(name=b["name"], code=b["code"])
            db.add(branch)
    db.commit()
