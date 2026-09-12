from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.quiz import QuizAttempt, QuizQuestion
from app.models.topic import Topic
from app.models.subject import Subject
from app.schemas.quiz import QuizAttemptSubmit, QuizQuestionCreate


def get_user_topic_by_id(db: Session, user_id: int, topic_id: int) -> Optional[Topic]:
    stmt = (
        select(Topic)
        .join(Subject, Topic.subject_id == Subject.id)
        .where(Topic.id == topic_id, Subject.user_id == user_id)
    )
    return db.execute(stmt).scalar_one_or_none()


def get_user_quiz_questions(db: Session, user_id: int, topic_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[QuizQuestion]:
    stmt = select(QuizQuestion).where(QuizQuestion.user_id == user_id)
    if topic_id is not None:
        stmt = stmt.where(QuizQuestion.topic_id == topic_id)
    stmt = stmt.order_by(QuizQuestion.created_at.desc()).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def create_quiz_question(db: Session, user_id: int, data: QuizQuestionCreate) -> QuizQuestion:
    topic = get_user_topic_by_id(db, user_id=user_id, topic_id=data.topic_id)
    if not topic:
        raise KeyError(f"Topic with id {data.topic_id} not found or access denied.")

    question = QuizQuestion(
        user_id=user_id,
        topic_id=data.topic_id,
        question_text=data.question_text.strip(),
        option_a=data.option_a.strip(),
        option_b=data.option_b.strip(),
        option_c=data.option_c.strip(),
        option_d=data.option_d.strip(),
        correct_option=data.correct_option.strip().upper(),
        difficulty=data.difficulty,
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def submit_quiz_attempt(db: Session, user_id: int, payload: QuizAttemptSubmit) -> QuizAttempt:
    topic = get_user_topic_by_id(db, user_id=user_id, topic_id=payload.topic_id)
    if not topic:
        raise KeyError(f"Topic with id {payload.topic_id} not found or access denied.")

    try:
        question_ids = [int(key) for key in payload.answers.keys()]
    except (TypeError, ValueError) as exc:
        raise ValueError("Quiz answer keys must be numeric question IDs.") from exc

    if any(question_id <= 0 for question_id in question_ids):
        raise ValueError("Quiz answer keys must be positive question IDs.")

    questions = db.execute(
        select(QuizQuestion).where(QuizQuestion.user_id == user_id, QuizQuestion.topic_id == payload.topic_id, QuizQuestion.id.in_(question_ids))
    ).scalars().all()
    if not questions:
        raise ValueError("No valid quiz questions were provided for this topic.")

    valid_question_ids = {question.id for question in questions}
    if set(question_ids) != valid_question_ids:
        raise ValueError("Answers must contain exactly the questions from this topic that belong to you.")

    total = len(questions)
    correct = 0
    answer_map = {question.id: question.correct_option for question in questions}
    for question_id, selected_option in payload.answers.items():
        if answer_map.get(int(question_id)) == selected_option:
            correct += 1

    percentage = round((correct / total) * 100, 2) if total else 0.0
    attempt = QuizAttempt(
        user_id=user_id,
        topic_id=payload.topic_id,
        questions_total=total,
        questions_correct=correct,
        percentage=percentage,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


def get_user_quiz_attempts(db: Session, user_id: int, topic_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[QuizAttempt]:
    stmt = select(QuizAttempt).where(QuizAttempt.user_id == user_id)
    if topic_id is not None:
        stmt = stmt.where(QuizAttempt.topic_id == topic_id)
    stmt = stmt.order_by(QuizAttempt.submitted_at.desc()).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def get_user_weak_topics(db: Session, user_id: int) -> List[dict]:
    stmt = (
        select(QuizAttempt.topic_id, Topic.name, QuizAttempt.percentage)
        .join(Topic, QuizAttempt.topic_id == Topic.id)
        .where(QuizAttempt.user_id == user_id)
    )
    rows = db.execute(stmt).all()
    grouped: dict[int, dict] = {}
    for topic_id, topic_name, percentage in rows:
        if topic_id not in grouped:
            grouped[topic_id] = {"topic_id": topic_id, "topic_name": topic_name, "scores": [], "attempts": 0}
        grouped[topic_id]["scores"].append(float(percentage))
        grouped[topic_id]["attempts"] += 1

    weak_topics = []
    for info in grouped.values():
        avg = sum(info["scores"]) / len(info["scores"]) if info["scores"] else 0.0
        status = "Weak" if avg < 60 else "Needs work" if avg < 75 else "Strong"
        weak_topics.append({
            "topic_id": info["topic_id"],
            "topic_name": info["topic_name"],
            "average_score": round(avg, 2),
            "attempts": info["attempts"],
            "status": status,
        })

    return sorted(weak_topics, key=lambda item: (item["average_score"], item["attempts"]))
