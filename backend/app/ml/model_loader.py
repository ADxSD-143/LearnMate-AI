from pathlib import Path

MODEL_DIR = Path("trained_models")


def get_model_path(model_name: str) -> Path:
    return MODEL_DIR / model_name
