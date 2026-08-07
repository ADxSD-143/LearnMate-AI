from sqlalchemy.orm import Session
from app.schemas.subject import SubjectCreate
from app.models.subject import Subject



def create_subject(db: Session, data: SubjectCreate):
    subject = Subject(name=data.name)  # Create Python object

    db.add(subject)  # Track it in Session

    db.commit()  # INSERT into PostgreSQL

    db.refresh(subject)  # Load generated values

    return subject