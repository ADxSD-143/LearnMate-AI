from fastapi import APIRouter

from app.schemas.user import UserCreate, UserLogin

router = APIRouter()


@router.post("/register")
def register_user(user: UserCreate) -> dict[str, str]:
    return {"message": f"User '{user.email}' registered successfully."}


@router.post("/login")
def login_user(user: UserLogin) -> dict[str, str]:
    return {"message": f"User '{user.email}' logged in successfully."}
