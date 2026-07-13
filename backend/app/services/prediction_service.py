from app.ml.predict import predict_performance
from app.ml.preprocess import preprocess_features


def generate_prediction(features: dict[str, float | int | str]) -> float:
    prepared_features = preprocess_features(features)
    return predict_performance(prepared_features)
