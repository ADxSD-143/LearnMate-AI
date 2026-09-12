def test_user_registration_and_referential_integrity(client):
    # 1. Seed colleges and branches
    client.post("/api/v1/colleges/seed")
    client.post("/api/v1/branches/seed")

    colleges = client.get("/api/v1/colleges/").json()
    branches = client.get("/api/v1/branches/").json()
    target_college = colleges[0]
    target_branch = branches[0]

    # 2. Register user successfully
    user_payload = {
        "username": "rahul_sharma",
        "email": "rahul@kiit.ac.in",
        "password": "SecurePassword123",
        "semester": 4,
        "college_id": target_college["id"],
        "branch_id": target_branch["id"],
    }
    reg_res = client.post("/api/v1/users/", json=user_payload)
    assert reg_res.status_code == 201
    user_data = reg_res.json()
    assert user_data["username"] == "rahul_sharma"
    assert user_data["email"] == "rahul@kiit.ac.in"
    assert user_data["semester"] == 4
    # Security verification: password / password_hash MUST NOT be exposed in output
    assert "password" not in user_data
    assert "password_hash" not in user_data
    assert user_data["college"]["id"] == target_college["id"]
    assert user_data["branch"]["id"] == target_branch["id"]

    # 3. Duplicate email prevention
    dup_email_payload = {
        "username": "rahul_unique",
        "email": "rahul@kiit.ac.in",
        "password": "AnotherPassword123",
        "semester": 4,
    }
    dup_res = client.post("/api/v1/users/", json=dup_email_payload)
    assert dup_res.status_code == 400
    assert "already registered" in dup_res.json()["detail"]

    # 4. Duplicate username prevention
    dup_user_payload = {
        "username": "rahul_sharma",
        "email": "different@kiit.ac.in",
        "password": "AnotherPassword123",
        "semester": 4,
    }
    dup_user_res = client.post("/api/v1/users/", json=dup_user_payload)
    assert dup_user_res.status_code == 400
    assert "already taken" in dup_user_res.json()["detail"]

    # 5. Invalid Foreign Key validation (College)
    bad_col_payload = {
        "username": "new_student",
        "email": "new@student.com",
        "password": "Password123",
        "semester": 1,
        "college_id": 99999,
    }
    bad_col_res = client.post("/api/v1/users/", json=bad_col_payload)
    assert bad_col_res.status_code == 400
    assert "College with id 99999 does not exist" in bad_col_res.json()["detail"]

    # 6. Invalid Foreign Key validation (Branch)
    bad_br_payload = {
        "username": "new_student2",
        "email": "new2@student.com",
        "password": "Password123",
        "semester": 1,
        "branch_id": 88888,
    }
    bad_br_res = client.post("/api/v1/users/", json=bad_br_payload)
    assert bad_br_res.status_code == 400
    assert "Branch with id 88888 does not exist" in bad_br_res.json()["detail"]


def test_authentication_and_protected_profile(client):
    # 1. Register a user
    user_payload = {
        "username": "test_learner",
        "email": "learner@learnmate.ai",
        "password": "LearnerSecret123",
        "semester": 3,
    }
    reg_res = client.post("/api/v1/users/", json=user_payload)
    assert reg_res.status_code == 201

    # 2. Login with incorrect password -> 401
    bad_login = client.post(
        "/api/v1/auth/login",
        data={"username": "test_learner", "password": "WrongPassword"}
    )
    assert bad_login.status_code == 401

    # 3. Login with correct password using username -> 200 + JWT
    login_user = client.post(
        "/api/v1/auth/login",
        data={"username": "test_learner", "password": "LearnerSecret123"}
    )
    assert login_user.status_code == 200
    token_data = login_user.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    access_token = token_data["access_token"]

    # 4. Login with email instead of username -> 200 + JWT
    login_email = client.post(
        "/api/v1/auth/login",
        data={"username": "learner@learnmate.ai", "password": "LearnerSecret123"}
    )
    assert login_email.status_code == 200

    # 5. Access /api/v1/users/me WITHOUT token -> 401
    unauth_res = client.get("/api/v1/users/me")
    assert unauth_res.status_code == 401

    # 6. Access /api/v1/users/me with INVALID token -> 401
    bad_token_res = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid.jwt.token"}
    )
    assert bad_token_res.status_code == 401

    # 7. Access /api/v1/users/me with VALID Bearer token -> 200 + User Profile
    auth_res = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert auth_res.status_code == 200
    profile = auth_res.json()
    assert profile["username"] == "test_learner"
    assert profile["email"] == "learner@learnmate.ai"
    assert profile["semester"] == 3
