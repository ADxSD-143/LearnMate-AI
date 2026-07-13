def build_recommendations(predicted_score: float) -> list[str]:
    if predicted_score >= 80:
        return ["Maintain your current study schedule.", "Start revision with mock tests."]
    if predicted_score >= 60:
        return ["Increase practice time on weak topics.", "Use short revision blocks every day."]
    return ["Review fundamentals first.", "Work with a guided study plan and track daily progress."]
