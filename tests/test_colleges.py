def test_create_and_list_colleges(client):
    # 1. Initially empty
    response = client.get("/api/v1/colleges/")
    assert response.status_code == 200
    assert response.json() == []

    # 2. Create a college
    college_data = {"name": "Indian Institute of Science", "email_domain": "iisc.ac.in"}
    create_res = client.post("/api/v1/colleges/", json=college_data)
    assert create_res.status_code == 201
    created = create_res.json()
    assert created["id"] is not None
    assert created["name"] == "Indian Institute of Science"
    assert created["email_domain"] == "iisc.ac.in"

    # 3. Retrieve by ID
    get_res = client.get(f"/api/v1/colleges/{created['id']}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Indian Institute of Science"

    # 4. Duplicate prevention
    dup_res = client.post("/api/v1/colleges/", json=college_data)
    assert dup_res.status_code == 409

def test_seed_colleges(client):
    seed_res = client.post("/api/v1/colleges/seed")
    assert seed_res.status_code == 200
    assert "seeded successfully" in seed_res.json()["message"]

    list_res = client.get("/api/v1/colleges/")
    assert list_res.status_code == 200
    colleges = list_res.json()
    assert len(colleges) >= 5
    names = [c["name"] for c in colleges]
    assert "KIIT University" in names
