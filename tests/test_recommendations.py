def get_auth_headers(client, username: str, email: str):
    reg_res = client.post("/api/v1/users/", json={
        "username": username,
        "email": email,
        "password": "Password123",
        "semester": 4,
    })
    assert reg_res.status_code == 201

    login_res = client.post("/api/v1/auth/login", data={
        "username": username,
        "password": "Password123",
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_recommendations_endpoint_returns_personalized_guidance(client):
    headers = get_auth_headers(client, "reco_student", "reco_student@test.com")

    subject = client.post("/api/v1/subjects/", json={"name": "Algorithms"}, headers=headers).json()
    topic = client.post("/api/v1/topics/", json={"name": "Dynamic Programming", "subject_id": subject["id"]}, headers=headers).json()

    q1 = client.post(
        "/api/v1/quizzes/questions",
        json={
            "topic_id": topic["id"],
            "question_text": "Dynamic programming avoids recomputation by using what?",
            "option_a": "Memoization",
            "option_b": "Sorting",
            "option_c": "Hashing",
            "option_d": "Encoding",
            "correct_option": "A",
            "difficulty": "Medium",
        },
        headers=headers,
    )
    assert q1.status_code == 201

    q2 = client.post(
        "/api/v1/quizzes/questions",
        json={
            "topic_id": topic["id"],
            "question_text": "What does a DP solution typically trade memory for?",
            "option_a": "CPU cycles",
            "option_b": "Network latency",
            "option_c": "Disk space",
            "option_d": "Code length",
            "correct_option": "A",
            "difficulty": "Medium",
        },
        headers=headers,
    )
    assert q2.status_code == 201

    attempt = client.post(
        "/api/v1/quizzes/attempts",
        json={
            "topic_id": topic["id"],
            "answers": {str(q1.json()["id"]): "B", str(q2.json()["id"]): "B"},
        },
        headers=headers,
    )
    assert attempt.status_code == 201

    res = client.get("/api/v1/recommendations/", headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert "recommendations" in body
    assert len(body["recommendations"]) >= 2
    assert body["overall_attendance"] >= 0


def test_study_plan_endpoint_returns_daily_plan(client):
    headers = get_auth_headers(client, "study_plan_student", "study_plan_student@test.com")
    subject = client.post("/api/v1/subjects/", json={"name": "Physics"}, headers=headers).json()
    topic = client.post("/api/v1/topics/", json={"name": "Kinematics", "subject_id": subject["id"]}, headers=headers).json()

    q1 = client.post(
        "/api/v1/quizzes/questions",
        json={
            "topic_id": topic["id"],
            "question_text": "Velocity is a vector quantity because it includes what?",
            "option_a": "Mass",
            "option_b": "Direction",
            "option_c": "Volume",
            "option_d": "Color",
            "correct_option": "B",
            "difficulty": "Easy",
        },
        headers=headers,
    )
    assert q1.status_code == 201

    client.post(
        "/api/v1/quizzes/attempts",
        json={
            "topic_id": topic["id"],
            "answers": {str(q1.json()["id"]): "A"},
        },
        headers=headers,
    )

    res = client.get("/api/v1/study-plans/", headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert "plan" in body
    assert len(body["plan"]) >= 3
    assert "focus_areas" in body
