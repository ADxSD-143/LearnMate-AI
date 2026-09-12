from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Task, Topic, Subject
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.topic_service import get_user_topic_by_id

def get_user_tasks(
    db: Session,
    user_id: int,
    topic_id: Optional[int] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Task]:
    """Retrieve tasks belonging to user, with optional filtering by topic, status, or priority."""
    stmt = (
        select(Task)
        .join(Topic, Task.topic_id == Topic.id)
        .join(Subject, Topic.subject_id == Subject.id)
        .where(Subject.user_id == user_id)
    )

    if topic_id is not None:
        stmt = stmt.where(Task.topic_id == topic_id)
    if status is not None:
        stmt = stmt.where(Task.status == status)
    if priority is not None:
        stmt = stmt.where(Task.priority == priority)

    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()

def get_user_task_by_id(db: Session, user_id: int, task_id: int) -> Optional[Task]:
    """Retrieve a specific task by ID, validating full relational ownership up to User."""
    stmt = (
        select(Task)
        .join(Topic, Task.topic_id == Topic.id)
        .join(Subject, Topic.subject_id == Subject.id)
        .where(Task.id == task_id, Subject.user_id == user_id)
    )
    return db.execute(stmt).scalar_one_or_none()

def create_task(db: Session, user_id: int, data: TaskCreate) -> Task:
    """Create a task under a topic, validating that the topic belongs to the authenticated user."""
    topic = get_user_topic_by_id(db, user_id=user_id, topic_id=data.topic_id)
    if not topic:
        raise KeyError(f"Topic with id {data.topic_id} not found or access denied.")

    task = Task(
        topic_id=data.topic_id,
        title=data.title.strip(),
        description=data.description,
        priority=data.priority,
        status=data.status,
        deadline=data.deadline,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task(db: Session, user_id: int, task_id: int, data: TaskUpdate) -> Task:
    """Update task details, validating ownership."""
    task = get_user_task_by_id(db, user_id=user_id, task_id=task_id)
    if not task:
        raise KeyError(f"Task with id {task_id} not found or access denied.")

    if data.title is not None:
        task.title = data.title.strip()
    if data.description is not None:
        task.description = data.description
    if data.priority is not None:
        task.priority = data.priority
    if data.status is not None:
        task.status = data.status
    if data.deadline is not None:
        task.deadline = data.deadline

    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, user_id: int, task_id: int) -> bool:
    """Delete task, validating ownership."""
    task = get_user_task_by_id(db, user_id=user_id, task_id=task_id)
    if not task:
        raise KeyError(f"Task with id {task_id} not found or access denied.")

    db.delete(task)
    db.commit()
    return True
