from collections.abc import Generator
from sqlalchemy.orm import Session

from app.database.session import SessionLocal#This imports the factory that creates database sessions.


# Generator[YieldType, SendType, ReturnType] -> Yield ho raha Session, baaki dono None
def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()#Creates one SQLAlchemy Session.
    try:
        # 2. HAND-OFF: Session ko route function me inject karo aur execution pause karo
        yield db# 1. Yield yahan pause hota hai aur 'db' route function ko de deta hai
        #At this point, execution pauses. return hota to execute kar deta and db.close() run hi nahi hota session khula reh jata
    finally:
        # 3. CLEANUP: Route ka kaam khatam hone par connection automatically close kar do
        db.close()#Runs automatically after the request finishes, even if an exception occurs.