from unittest.mock import patch


def _auth_headers(client):
    client.post("/auth/register", json={"email": "aitest@example.com", "password": "supersecret123"})
    resp = client.post("/auth/login", data={"username": "aitest@example.com", "password": "supersecret123"})
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}


def test_analyze_requires_both_fields(client):
    headers = _auth_headers(client)
    resp = client.post(
        "/ai/analyze", json={"resume_text": "", "job_description": "something"}, headers=headers
    )
    assert resp.status_code == 400


@patch("app.routes.ai.analyze_resume")
def test_analyze_returns_report(mock_analyze, client):
    mock_analyze.return_value = {
        "verdict": "Partial Match",
        "summary": "Solid technical background, missing direct finance experience.",
        "missingSkills": ["Quantitative finance"],
        "suggestedKeywords": ["portfolio optimization"],
        "interviewTopics": ["Statistics fundamentals"],
    }
    headers = _auth_headers(client)
    resp = client.post(
        "/ai/analyze",
        json={
            "resume_text": "Experienced software engineer with a CS background...",
            "job_description": "Looking for a quant researcher with strong stats skills...",
        },
        headers=headers,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["verdict"] == "Partial Match"
    assert "Quantitative finance" in body["missingSkills"]
    mock_analyze.assert_called_once()


@patch("app.routes.ai.analyze_resume")
def test_analyze_saves_report_to_linked_application(mock_analyze, client):
    mock_analyze.return_value = {
        "verdict": "Strong Match",
        "summary": "Great fit overall.",
        "missingSkills": [],
        "suggestedKeywords": ["Python"],
        "interviewTopics": ["System design"],
    }
    headers = _auth_headers(client)
    create_resp = client.post(
        "/applications", json={"company": "Test Co", "role": "Backend Engineer"}, headers=headers
    )
    app_id = create_resp.json()["id"]

    client.post(
        "/ai/analyze",
        json={
            "resume_text": "Backend engineer, 5 years Python...",
            "job_description": "Backend role requiring Python...",
            "application_id": app_id,
        },
        headers=headers,
    )

    get_resp = client.get(f"/applications/{app_id}", headers=headers)
    assert get_resp.json()["last_analysis"]["verdict"] == "Strong Match"
