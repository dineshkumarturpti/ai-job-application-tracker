def _auth_headers(client, email="apptest@example.com", password="supersecret123"):
    client.post("/auth/register", json={"email": email, "password": password})
    resp = client.post("/auth/login", data={"username": email, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_list_update_delete_application(client):
    headers = _auth_headers(client)

    create_resp = client.post(
        "/applications",
        json={
            "company": "Aquatic Capital",
            "role": "Quant Researcher",
            "status": "saved",
            "job_description": "Looking for a quant researcher...",
        },
        headers=headers,
    )
    assert create_resp.status_code == 201
    app_data = create_resp.json()
    app_id = app_data["id"]
    assert app_data["status"] == "saved"

    list_resp = client.get("/applications", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    update_resp = client.put(f"/applications/{app_id}", json={"status": "applied"}, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "applied"

    filtered_resp = client.get("/applications", params={"status": "applied"}, headers=headers)
    assert len(filtered_resp.json()) == 1

    missed_filter_resp = client.get("/applications", params={"status": "offer"}, headers=headers)
    assert len(missed_filter_resp.json()) == 0

    delete_resp = client.delete(f"/applications/{app_id}", headers=headers)
    assert delete_resp.status_code == 204

    empty_resp = client.get("/applications", headers=headers)
    assert empty_resp.json() == []


def test_application_requires_auth(client):
    resp = client.get("/applications")
    assert resp.status_code == 401


def test_users_cannot_see_each_others_applications(client):
    headers_a = _auth_headers(client, email="a@example.com")
    headers_b = _auth_headers(client, email="b@example.com")

    client.post(
        "/applications",
        json={"company": "A Co", "role": "Engineer"},
        headers=headers_a,
    )

    resp_b = client.get("/applications", headers=headers_b)
    assert resp_b.json() == []

    resp_a = client.get("/applications", headers=headers_a)
    assert len(resp_a.json()) == 1
