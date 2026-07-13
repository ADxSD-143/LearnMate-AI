def predict_performance(features: dict[str, float]) -> float:
    if not features:
        return 0.0

    numeric_values = [float(value) for value in features.values()]
    score = sum(numeric_values) / len(numeric_values)
    return round(score, 2)
