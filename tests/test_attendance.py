import pytest
from datetime import date

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

def test_timetable_crud_and_isolation(client):
    headers_a = get_auth_headers(client, "student_tt_a", "tt_a@test.com")
    headers_b = get_auth_headers(client, "student_tt_b", "tt_b@test.com")

    # User A creates a subject
    subj_a = client.post("/api/v1/subjects/", json={"name": "Computer Networks"}, headers=headers_a).json()

    # User A creates a timetable slot
    tt_payload = {
        "subject_id": subj_a["id"],
        "day_of_week": "Monday",
        "start_time": "10:00",
        "end_time": "11:00",
        "room_number": "Room 301"
    }
    tt_res = client.post("/api/v1/timetable/", json=tt_payload, headers=headers_a)
    assert tt_res.status_code == 201
    tt_entry_id = tt_res.json()["id"]

    # User A can query timetable by day
    mon_tt = client.get("/api/v1/timetable/?day_of_week=Monday", headers=headers_a).json()
    assert len(mon_tt) == 1
    assert mon_tt[0]["room_number"] == "Room 301"

    # User B CANNOT see User A's timetable
    b_tt = client.get("/api/v1/timetable/?day_of_week=Monday", headers=headers_b).json()
    assert len(b_tt) == 0

    # User B CANNOT access User A's timetable entry directly -> 404
    b_get = client.get(f"/api/v1/timetable/{tt_entry_id}", headers=headers_b)
    assert b_get.status_code == 404

    # User B CANNOT delete User A's timetable entry -> 404
    b_del = client.delete(f"/api/v1/timetable/{tt_entry_id}", headers=headers_b)
    assert b_del.status_code == 404


def test_attendance_marking_and_bunk_calculator(client):
    headers = get_auth_headers(client, "student_att", "att@test.com")

    # 1. Create subject
    subj = client.post("/api/v1/subjects/", json={"name": "Software Engineering"}, headers=headers).json()
    subj_id = subj["id"]

    # 2. Initially with 0 classes conducted: percentage is 100%, 0 shortage
    initial_stats = client.get(f"/api/v1/attendance/subject/{subj_id}", headers=headers).json()
    assert initial_stats["total_conducted"] == 0
    assert initial_stats["percentage"] == 100.0
    assert initial_stats["is_shortage"] is False
    assert initial_stats["bunks_available"] == 0

    # 3. Mark 4 Present sessions
    for day in range(1, 5):
        res = client.post("/api/v1/attendance/", json={
            "subject_id": subj_id,
            "date": f"2026-03-0{day}",
            "status": "Present"
        }, headers=headers)
        assert res.status_code == 201

    # Now: 4 attended / 4 conducted = 100.0%
    # With 75% target, 4 / (4 + 1) = 80.0% >= 75%, so 1 safe bunk available!
    stats_4p = client.get(f"/api/v1/attendance/subject/{subj_id}", headers=headers).json()
    assert stats_4p["total_conducted"] == 4
    assert stats_4p["total_attended"] == 4
    assert stats_4p["percentage"] == 100.0
    assert stats_4p["bunks_available"] == 1
    assert stats_4p["classes_needed_to_reach_target"] == 0

    # 4. Now student bunks 1 class (Absent)
    client.post("/api/v1/attendance/", json={
        "subject_id": subj_id,
        "date": "2026-03-05",
        "status": "Absent"
    }, headers=headers)

    # 4 attended / 5 conducted = 80.0%
    # Next bunk would drop to 4/6 = 66.7% < 75%, so 0 safe bunks available!
    stats_5 = client.get(f"/api/v1/attendance/subject/{subj_id}", headers=headers).json()
    assert stats_5["total_conducted"] == 5
    assert stats_5["total_attended"] == 4
    assert stats_5["percentage"] == 80.0
    assert stats_5["bunks_available"] == 0
    assert stats_5["is_shortage"] is False

    # 5. Now student bunks a second class (Absent) -> drops into shortage!
    client.post("/api/v1/attendance/", json={
        "subject_id": subj_id,
        "date": "2026-03-06",
        "status": "Absent"
    }, headers=headers)

    # 4 attended / 6 conducted = 66.67%
    # Catch-up needed: (4 + c)/(6 + c) >= 0.75 => c = 2 classes!
    stats_6 = client.get(f"/api/v1/attendance/subject/{subj_id}", headers=headers).json()
    assert stats_6["total_conducted"] == 6
    assert stats_6["total_attended"] == 4
    assert stats_6["percentage"] == 66.67
    assert stats_6["is_shortage"] is True
    assert stats_6["classes_needed_to_reach_target"] == 2

    # 6. Mark a 'Cancelled' class (e.g. college holiday)
    client.post("/api/v1/attendance/", json={
        "subject_id": subj_id,
        "date": "2026-03-07",
        "status": "Cancelled",
        "notes": "College sports day"
    }, headers=headers)

    # Total conducted MUST NOT increase for Cancelled sessions
    stats_canc = client.get(f"/api/v1/attendance/subject/{subj_id}", headers=headers).json()
    assert stats_canc["total_conducted"] == 6
    assert stats_canc["total_cancelled"] == 1
    assert stats_canc["percentage"] == 66.67


def test_cross_user_attendance_security(client):
    headers_alice = get_auth_headers(client, "alice_att", "alice_att@test.com")
    headers_bob = get_auth_headers(client, "bob_att", "bob_att@test.com")

    # Alice creates subject & logs attendance
    subj_alice = client.post("/api/v1/subjects/", json={"name": "Cloud Computing"}, headers=headers_alice).json()
    att_res = client.post("/api/v1/attendance/", json={
        "subject_id": subj_alice["id"],
        "date": "2026-03-10",
        "status": "Present"
    }, headers=headers_alice)
    rec_id = att_res.json()["id"]

    # Bob attempts to log attendance for Alice's subject -> 404
    bob_mark = client.post("/api/v1/attendance/", json={
        "subject_id": subj_alice["id"],
        "date": "2026-03-10",
        "status": "Present"
    }, headers=headers_bob)
    assert bob_mark.status_code == 404

    # Bob attempts to edit Alice's attendance record -> 404
    bob_edit = client.put(f"/api/v1/attendance/{rec_id}", json={"status": "Absent"}, headers=headers_bob)
    assert bob_edit.status_code == 404

    # Bob attempts to delete Alice's attendance record -> 404
    bob_del = client.delete(f"/api/v1/attendance/{rec_id}", headers=headers_bob)
    assert bob_del.status_code == 404


def test_timetable_rejects_invalid_ranges_and_overlaps(client):
    headers = get_auth_headers(client, "student_tt_validation", "tt_validation@test.com")
    subject = client.post(
        "/api/v1/subjects/",
        json={"name": "Operating Systems"},
        headers=headers,
    ).json()

    invalid = client.post(
        "/api/v1/timetable/",
        json={
            "subject_id": subject["id"],
            "day_of_week": "Tuesday",
            "start_time": "11:00",
            "end_time": "10:00",
        },
        headers=headers,
    )
    assert invalid.status_code == 400

    first = client.post(
        "/api/v1/timetable/",
        json={
            "subject_id": subject["id"],
            "day_of_week": "Tuesday",
            "start_time": "10:00",
            "end_time": "11:00",
        },
        headers=headers,
    )
    assert first.status_code == 201

    overlap = client.post(
        "/api/v1/timetable/",
        json={
            "subject_id": subject["id"],
            "day_of_week": "Tuesday",
            "start_time": "10:30",
            "end_time": "11:30",
        },
        headers=headers,
    )
    assert overlap.status_code == 400
