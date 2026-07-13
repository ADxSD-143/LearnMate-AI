def preprocess_features(features: dict[str, float | int | str]) -> dict[str, float]:
    processed_features: dict[str, float] = {}
    for key, value in features.items():
        processed_features[key] = float(value)
    return processed_features
