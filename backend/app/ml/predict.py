def predict_performance(features: dict[str, float]) -> float:
    """Baseline feature-mean predictor used for the initial ML scaffold.

    This intentionally represents a simple rule-based/statistical baseline and not
    a production ML model. It provides a deterministic API contract while the
    project evolves toward real model pipelines with data collection and validation.
    """
    if not features:
        return 0.0

    numeric_values = [float(value) for value in features.values()]
    score = sum(numeric_values) / len(numeric_values)
    return round(score, 2)
