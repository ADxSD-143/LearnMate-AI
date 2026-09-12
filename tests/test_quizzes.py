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


def test_quiz_questions_and_weak_topic_tracking(client):
    headers = get_auth_headers(client, "quiz_student", "quiz_student@test.com")

    subj = client.post("/api/v1/subjects/", json={"name": "Machine Learning"}, headers=headers).json()
    topic = client.post("/api/v1/topics/", json={"name": "Decision Trees", "subject_id": subj["id"]}, headers=headers).json()

    q1 = client.post(
        "/api/v1/quizzes/questions",
        json={
            "topic_id": topic["id"],
            "question_text": "A decision tree splits data using what?",
            "option_a": "A random value",
            "option_b": "Feature thresholds",
            "option_c": "Neural weights",
            "option_d": "Hash buckets",
            "correct_option": "B",
            "difficulty": "Medium",
        },
        headers=headers,
    )
    assert q1.status_code == 201

    q2 = client.post(
        "/api/v1/quizzes/questions",
        json={
            "topic_id": topic["id"],
            "question_text": "Decision trees are best suited for what kind of task?",
            "option_a": "Only clustering",
            "option_b": "Classification and regression",
            "option_c": "Only image generation",
            "option_d": "Only anomaly detection",
            "correct_option": "B",
            "difficulty": "Easy",
        },
        headers=headers,
    )
    assert q2.status_code == 201

    attempt = client.post(
        "/api/v1/quizzes/attempts",
        json={
            "topic_id": topic["id"],
            "answers": {str(q1.json()["id"]): "A", str(q2.json()["id"]): "B"},
        },
        headers=headers,
    )
    assert attempt.status_code == 201
    body = attempt.json()
    assert body["questions_total"] == 2
    assert body["questions_correct"] == 1
    assert body["percentage"] == 50.0

    weak = client.get("/api/v1/quizzes/weak-topics", headers=headers).json()
    assert len(weak) == 1
    assert weak[0]["status"] in {"Weak", "Needs work"}


def test_cross_user_quiz_isolation(client):
    headers_a = get_auth_headers(client, "alice_quiz", "alice_quiz@test.com")
    headers_b = get_auth_headers(client, "bob_quiz", "bob_quiz@test.com")

    subj = client.post("/api/v1/subjects/", json={"name": "DBMS"}, headers=headers_a).json()
    topic = client.post("/api/v1/topics/", json={"name": "Normalization", "subject_id": subj["id"]}, headers=headers_a).json()

    q = client.post(
        "/api/v1/quizzes/questions",
        json={
            "topic_id": topic["id"],
            "question_text": "What is normalization?",
            "option_a": "A data organization technique",
            "option_b": "A sort algorithm",
            "option_c": "A network protocol",
            "option_d": "A compiler step",
            "correct_option": "A",
        },
        headers=headers_a,
    )
    assert q.status_code == 201

    bob_attempt = client.post(
        "/api/v1/quizzes/attempts",
        json={
            "topic_id": topic["id"],
            "answers": {str(q.json()["id"]): "B"},
        },
        headers=headers_b,
    )
    assert bob_attempt.status_code == 404
