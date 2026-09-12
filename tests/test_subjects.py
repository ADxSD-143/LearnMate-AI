import pytest

def get_auth_headers(client, username: str, email: str):
    # Register and login helper
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

def test_subject_multi_user_isolation(client):
    headers_a = get_auth_headers(client, "student_a", "student_a@test.com")
    headers_b = get_auth_headers(client, "student_b", "student_b@test.com")

    # 1. User A creates 'Operating Systems'
    res_a = client.post("/api/v1/subjects/", json={"name": "Operating Systems"}, headers=headers_a)
    assert res_a.status_code == 201
    subj_a_id = res_a.json()["id"]

    # 2. User B can ALSO create 'Operating Systems' (multi-user composite uniqueness: UNIQUE(user_id, name))
    res_b = client.post("/api/v1/subjects/", json={"name": "Operating Systems"}, headers=headers_b)
    assert res_b.status_code == 201
    subj_b_id = res_b.json()["id"]
    assert subj_a_id != subj_b_id

    # 3. User A CANNOT create 'Operating Systems' twice
    dup_res = client.post("/api/v1/subjects/", json={"name": "Operating Systems"}, headers=headers_a)
    assert dup_res.status_code == 400
    assert "already exists" in dup_res.json()["detail"]

    # 4. User A list subjects only shows User A's subject
    list_a = client.get("/api/v1/subjects/", headers=headers_a).json()
    assert len(list_a) == 1
    assert list_a[0]["id"] == subj_a_id

    # 5. User A CANNOT access User B's subject by ID (returns 404)
    cross_access = client.get(f"/api/v1/subjects/{subj_b_id}", headers=headers_a)
    assert cross_access.status_code == 404

    # 6. User A CANNOT delete User B's subject
    cross_delete = client.delete(f"/api/v1/subjects/{subj_b_id}", headers=headers_a)
    assert cross_delete.status_code == 404

def test_topics_and_tasks_academic_hierarchy(client):
    headers = get_auth_headers(client, "rahul_dev", "rahul_dev@kiit.ac.in")

    # 1. Create Subject
    subj_res = client.post("/api/v1/subjects/", json={"name": "Data Structures & Algorithms"}, headers=headers)
    assert subj_res.status_code == 201
    subject_id = subj_res.json()["id"]

    # 2. Create Topics under Subject
    topic1_res = client.post("/api/v1/topics/", json={"name": "Binary Search Trees", "subject_id": subject_id}, headers=headers)
    assert topic1_res.status_code == 201
    topic1_id = topic1_res.json()["id"]

    topic2_res = client.post("/api/v1/topics/", json={"name": "Dynamic Programming", "subject_id": subject_id}, headers=headers)
    assert topic2_res.status_code == 201
    topic2_id = topic2_res.json()["id"]

    # 3. Duplicate Topic in same Subject is rejected
    dup_topic = client.post("/api/v1/topics/", json={"name": "Binary Search Trees", "subject_id": subject_id}, headers=headers)
    assert dup_topic.status_code == 400

    # 4. List Topics under Subject
    topics_list = client.get(f"/api/v1/topics/?subject_id={subject_id}", headers=headers).json()
    assert len(topics_list) == 2

    # 5. Create Tasks under Topic
    task1_res = client.post("/api/v1/tasks/", json={
        "topic_id": topic1_id,
        "title": "Solve Lowest Common Ancestor on LeetCode",
        "description": "Problem #236 with O(N) time complexity",
        "priority": "High",
        "status": "Pending"
    }, headers=headers)
    assert task1_res.status_code == 201
    task1_id = task1_res.json()["id"]

    task2_res = client.post("/api/v1/tasks/", json={
        "topic_id": topic1_id,
        "title": "Implement AVL Tree Rotations",
        "priority": "Medium",
        "status": "In Progress"
    }, headers=headers)
    assert task2_res.status_code == 201
    task2_id = task2_res.json()["id"]

    # 6. Update Task Status & Priority
    update_res = client.put(f"/api/v1/tasks/{task1_id}", json={
        "status": "Completed"
    }, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "Completed"

    # 7. Query tasks with filters
    completed_tasks = client.get("/api/v1/tasks/?status=Completed", headers=headers).json()
    assert len(completed_tasks) == 1
    assert completed_tasks[0]["id"] == task1_id

    # 8. Cascading Deletion: Deleting Subject deletes its Topics and Tasks
    del_subj = client.delete(f"/api/v1/subjects/{subject_id}", headers=headers)
    assert del_subj.status_code == 204

    # Verify Topic and Task are cascaded
    get_topic = client.get(f"/api/v1/topics/{topic1_id}", headers=headers)
    assert get_topic.status_code == 404

    get_task = client.get(f"/api/v1/tasks/{task1_id}", headers=headers)
    assert get_task.status_code == 404

def test_cross_user_academic_security(client):
    headers_owner = get_auth_headers(client, "alice_owner", "alice@test.com")
    headers_intruder = get_auth_headers(client, "bob_intruder", "bob@test.com")

    # Alice creates subject, topic, task
    subj_res = client.post("/api/v1/subjects/", json={"name": "Compiler Design"}, headers=headers_owner)
    alice_subj_id = subj_res.json()["id"]

    topic_res = client.post("/api/v1/topics/", json={"name": "Lexical Analysis", "subject_id": alice_subj_id}, headers=headers_owner)
    alice_topic_id = topic_res.json()["id"]

    task_res = client.post("/api/v1/tasks/", json={"topic_id": alice_topic_id, "title": "Write Flex Lexer"}, headers=headers_owner)
    alice_task_id = task_res.json()["id"]

    # Bob attempts to add a topic under Alice's subject -> 404
    bob_add_topic = client.post("/api/v1/topics/", json={"name": "Parsing", "subject_id": alice_subj_id}, headers=headers_intruder)
    assert bob_add_topic.status_code == 404

    # Bob attempts to add a task under Alice's topic -> 404
    bob_add_task = client.post("/api/v1/tasks/", json={"topic_id": alice_topic_id, "title": "Malicious Task"}, headers=headers_intruder)
    assert bob_add_task.status_code == 404

    # Bob attempts to read Alice's task -> 404
    bob_read_task = client.get(f"/api/v1/tasks/{alice_task_id}", headers=headers_intruder)
    assert bob_read_task.status_code == 404

    # Bob attempts to update Alice's task -> 404
    bob_edit_task = client.put(f"/api/v1/tasks/{alice_task_id}", json={"status": "Completed"}, headers=headers_intruder)
    assert bob_edit_task.status_code == 404

    # Bob attempts to delete Alice's task -> 404
    bob_del_task = client.delete(f"/api/v1/tasks/{alice_task_id}", headers=headers_intruder)
    assert bob_del_task.status_code == 404
