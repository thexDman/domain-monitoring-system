def test_health_endpoint(client):
    res = client.get("/health")

    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "ok"
