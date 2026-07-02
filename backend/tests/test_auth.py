def test_register_and_login(client):
    register_resp = client.post(
        "/auth/register", json={"email": "jane@example.com", "password": "supersecret123"}
    )
    assert register_resp.status_code == 201
    assert register_resp.json()["email"] == "jane@example.com"

    duplicate_resp = client.post(
        "/auth/register", json={"email": "jane@example.com", "password": "anotherpass"}
    )
    assert duplicate_resp.status_code == 400

    login_resp = client.post(
        "/auth/login", data={"username": "jane@example.com", "password": "supersecret123"}
    )
    assert login_resp.status_code == 200
    body = login_resp.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"

    bad_login_resp = client.post(
        "/auth/login", data={"username": "jane@example.com", "password": "wrong-password"}
    )
    assert bad_login_resp.status_code == 401
