from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.base import get_db
from app.schemas.branch import BranchCreate, BranchOut
from app.services.branch_service import (
    get_branches,
    get_branch_by_id,
    create_branch,
    seed_default_branches
)

router = APIRouter()

@router.get("/", response_model=List[BranchOut])
def list_branches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_branches(db, skip=skip, limit=limit)

@router.post("/", response_model=BranchOut, status_code=status.HTTP_201_CREATED)
def add_branch(data: BranchCreate, db: Session = Depends(get_db)):
    try:
        return create_branch(db, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Branch with name '{data.name}' or code '{data.code}' already exists."
        )

@router.get("/{branch_id}", response_model=BranchOut)
def read_branch(branch_id: int, db: Session = Depends(get_db)):
    branch = get_branch_by_id(db, branch_id)
    if not branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    return branch

@router.post("/seed", response_model=dict)
def seed_branches(db: Session = Depends(get_db)):
    seed_default_branches(db)
    return {"message": "Default branches seeded successfully"}
