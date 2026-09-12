def test_create_and_list_branches(client):
    # 1. Initially empty
    response = client.get("/api/v1/branches/")
    assert response.status_code == 200
    assert response.json() == []

    # 2. Create a branch
    branch_data = {"name": "Artificial Intelligence and Data Science", "code": "AI&DS"}
    create_res = client.post("/api/v1/branches/", json=branch_data)
    assert create_res.status_code == 201
    created = create_res.json()
    assert created["id"] is not None
    assert created["name"] == "Artificial Intelligence and Data Science"
    assert created["code"] == "AI&DS"

    # 3. Retrieve by ID
    get_res = client.get(f"/api/v1/branches/{created['id']}")
    assert get_res.status_code == 200
    assert get_res.json()["code"] == "AI&DS"

    # 4. Duplicate prevention
    dup_res = client.post("/api/v1/branches/", json=branch_data)
    assert dup_res.status_code == 409

def test_seed_branches(client):
    seed_res = client.post("/api/v1/branches/seed")
    assert seed_res.status_code == 200
    assert "seeded successfully" in seed_res.json()["message"]

    list_res = client.get("/api/v1/branches/")
    assert list_res.status_code == 200
    branches = list_res.json()
    codes = [b["code"] for b in branches]
    assert "CSE" in codes
    assert "ECE" in codes
    assert "ME" in codes
