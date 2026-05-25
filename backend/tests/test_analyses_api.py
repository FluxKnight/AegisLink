def test_create_analysis(client):
    response = client.post(
        "/api/v1/analyses",
        json={"url": "http://192.168.1.1/login/verify"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] >= 1
    assert data["risk_score"] >= 0
    assert data["risk_level"] in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
    assert isinstance(data["findings"], list)
    assert data["explanation"]
    assert isinstance(data["recommendations"], list)


def test_list_analyses(client):
    client.post("/api/v1/analyses", json={"url": "https://example.com"})
    client.post(
        "/api/v1/analyses",
        json={"url": "http://192.168.1.1/login/verify-account"},
    )

    response = client.get("/api/v1/analyses?limit=10&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2
    assert len(data["items"]) >= 2
    assert data["limit"] == 10
    assert data["offset"] == 0


def test_get_analysis_detail(client):
    created = client.post(
        "/api/v1/analyses",
        json={"url": "https://bit.ly/example-login"},
    ).json()
    response = client.get(f"/api/v1/analyses/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_report_endpoint(client):
    created = client.post(
        "/api/v1/analyses",
        json={"url": "https://paypal-login.verify.example.xyz/reset"},
    ).json()
    response = client.get(f"/api/v1/reports/analyses/{created['id']}")
    assert response.status_code == 200
    body = response.json()
    assert body["analysis_id"] == created["id"]
    assert "# AegisLink Security Report" in body["report_markdown"]
