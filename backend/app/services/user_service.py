from typing import List, Optional
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.college import College
from app.models.branch import Branch
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    stmt = select(User).where(User.id == user_id)
    return db.execute(stmt).scalar_one_or_none()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email.lower().strip())
    return db.execute(stmt).scalar_one_or_none()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    stmt = select(User).where(User.username == username.strip())
    return db.execute(stmt).scalar_one_or_none()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    stmt = select(User).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()

def create_user(db: Session, data: UserCreate) -> User:
    email_clean = data.email.lower().strip()
    username_clean = data.username.strip()

    # 1. Uniqueness checks
    if get_user_by_email(db, email_clean):
        raise ValueError(f"Email '{email_clean}' is already registered.")

    if get_user_by_username(db, username_clean):
        raise ValueError(f"Username '{username_clean}' is already taken.")

    # 2. Referential integrity validation
    if data.college_id is not None:
        college = db.execute(select(College).where(College.id == data.college_id)).scalar_one_or_none()
        if not college:
            raise ValueError(f"College with id {data.college_id} does not exist.")

    if data.branch_id is not None:
        branch = db.execute(select(Branch).where(Branch.id == data.branch_id)).scalar_one_or_none()
        if not branch:
            raise ValueError(f"Branch with id {data.branch_id} does not exist.")

    # 3. Secure password hashing
    hashed_pwd = get_password_hash(data.password)

    # 4. Persistence
    user = User(
        username=username_clean,
        email=email_clean,
        password_hash=hashed_pwd,
        college_id=data.college_id,
        branch_id=data.branch_id,
        semester=data.semester,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, login_identifier: str, password: str) -> Optional[User]:
    identifier = login_identifier.strip()
    stmt = select(User).where(
        or_(User.username == identifier, User.email == identifier.lower())
    )
    user = db.execute(stmt).scalar_one_or_none()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
