from typing import Any

from sqlalchemy.orm import Session

from app.services.attendance_service import calculate_overall_attendance
from app.services.quiz_service import get_user_weak_topics
from app.services.subject_service import get_user_subjects


def build_recommendations(predicted_score: float) -> list[str]:
    if predicted_score >= 80:
        return ["Maintain your current study schedule.", "Start revision with mock tests."]
    if predicted_score >= 60:
        return ["Increase practice time on weak topics.", "Use short revision blocks every day."]
    return ["Review fundamentals first.", "Work with a guided study plan and track daily progress."]


def build_learning_profile(db: Session, user_id: int) -> dict[str, Any]:
    subjects = get_user_subjects(db, user_id=user_id)
    weak_topics = get_user_weak_topics(db, user_id=user_id)
    attendance = calculate_overall_attendance(db, user_id=user_id, target_percentage=75.0)

    return {
        "subject_count": len(subjects),
        "weak_topics": weak_topics,
        "overall_attendance": attendance.overall_percentage,
        "total_class_sessions": attendance.total_classes_conducted,
        "subject_names": [subject.name for subject in subjects],
    }


def build_personalized_recommendations(db: Session, user_id: int) -> list[str]:
    profile = build_learning_profile(db, user_id=user_id)
    suggestions: list[str] = []

    if profile["overall_attendance"] < 75:
        suggestions.append("Your attendance is below target. Prioritize attending the next classes in your weakest subject area.")
    else:
        suggestions.append("Your attendance is healthy. Keep the current consistency and add extra revision to weak topics.")

    if profile["weak_topics"]:
        weakest = profile["weak_topics"][0]
        suggestions.append(f"Focus extra revision on {weakest['topic_name']} before your next quiz or test cycle.")
    else:
        suggestions.append("You have no weak topics flagged yet. Keep practicing and attempt a few more quizzes to sharpen the profile.")

    if profile["subject_count"] == 0:
        suggestions.append("Create your first subject and start tracking study progress so recommendations become more precise.")
    else:
        suggestions.append("Review the most critical subject first and schedule a short focused practice block each day.")

    return suggestions


def generate_study_plan(db: Session, user_id: int) -> list[dict[str, Any]]:
    profile = build_learning_profile(db, user_id=user_id)
    weak_topics = profile["weak_topics"]
    if not weak_topics:
        focus_topics = ["General revision", "Concept recall", "Practice quiz review"]
    else:
        focus_topics = [entry["topic_name"] for entry in weak_topics[:3]]

    plan: list[dict[str, Any]] = []
    durations = [45, 60, 90]
    for idx, topic in enumerate(focus_topics):
        plan.append({
            "day": idx + 1,
            "topic": topic,
            "duration_minutes": durations[idx % len(durations)],
            "focus": "Practice active recall and solve targeted questions." if idx % 2 == 0 else "Review notes and complete concise revision drills.",
        })

    if len(plan) < 3:
        filler_topics = ["Weak area revision", "Quick recap", "Mock test practice"]
        for filler in filler_topics:
            if len(plan) >= 3:
                break
            plan.append({
                "day": len(plan) + 1,
                "topic": filler,
                "duration_minutes": 45,
                "focus": "Keep the study block short and consistent to build retention.",
            })

    return plan
