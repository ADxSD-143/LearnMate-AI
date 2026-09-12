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


def test_material_upload_and_grounded_query(client):
    headers = get_auth_headers(client, "rag_student", "rag_student@test.com")

    content = b"Random forest builds many decision trees and reduces variance. Logistic regression models probabilities. Support vector machines maximize class margins."
    res = client.post(
        "/api/v1/materials/upload",
        files={"file": ("ml_notes.txt", content, "text/plain")},
        data={"title": "ML Notes"},
        headers=headers,
    )
    assert res.status_code == 201, res.text
    body = res.json()
    assert body["status"] == "READY"
    assert body["title"] == "ML Notes"

    list_res = client.get("/api/v1/materials/", headers=headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    ask_res = client.post(
        f"/api/v1/materials/{body['id']}/ask",
        json={"question": "What does random forest do?"},
        headers=headers,
    )
    assert ask_res.status_code == 200, ask_res.text
    answer = ask_res.json()["answer"].lower()
    assert "random forest" in answer or "decision trees" in answer

    generate_res = client.post(
        f"/api/v1/materials/{body['id']}/generate",
        json={"artifact_type": "summary", "max_items": 3},
        headers=headers,
    )
    assert generate_res.status_code == 200, generate_res.text
    generated = generate_res.json()
    assert generated["artifact_type"] == "summary"
    assert generated["content"]


def test_material_access_is_user_isolated(client):
    headers_a = get_auth_headers(client, "alice_material", "alice_material@test.com")
    headers_b = get_auth_headers(client, "bob_material", "bob_material@test.com")

    upload = client.post(
        "/api/v1/materials/upload",
        files={"file": ("notes.txt", b"This document is about reinforcement learning.", "text/plain")},
        data={"title": "RL notes"},
        headers=headers_a,
    )
    doc_id = upload.json()["id"]

    bob_get = client.get(f"/api/v1/materials/{doc_id}", headers=headers_b)
    assert bob_get.status_code == 404

    bob_ask = client.post(
        f"/api/v1/materials/{doc_id}/ask",
        json={"question": "What is this about?"},
        headers=headers_b,
    )
    assert bob_ask.status_code == 404
