def test_prediction_api_returns_prediction_and_recommendations(client):
    payload = {
        "study_hours": 12,
        "revision_hours": 8,
        "attendance": 85,
        "quiz_score": 78,
        "mock_test_score": 80,
        "assignments_completed": 5,
    }

    res = client.post("/api/v1/predict/", json=payload)
    assert res.status_code == 200
    body = res.json()
    assert "predicted_score" in body
    assert "recommendations" in body
    assert isinstance(body["predicted_score"], float)
    assert len(body["recommendations"]) >= 2


def test_prediction_api_rejects_invalid_values(client):
    bad_payload = {
        "study_hours": -1,
        "revision_hours": 5,
        "attendance": 90,
        "quiz_score": 70,
        "mock_test_score": 75,
        "assignments_completed": 4,
    }

    res = client.post("/api/v1/predict/", json=bad_payload)
    assert res.status_code == 422
