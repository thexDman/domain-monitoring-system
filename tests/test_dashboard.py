from unittest.mock import patch


def test_dashboard_requires_login(client):
    res = client.get("/dashboard")
    assert res.status_code == 302
    assert "/login" in res.location

def test_dashboard_loads_page(client):
    with client.session_transaction() as sess:
        sess["username"] = "testuser"

    with patch("app.backend_get") as mock_get:
        mock_get.return_value = (
            {"ok": True, "domains": ["example.com"]},
            200
        )

        res = client.get("/dashboard")

        assert res.status_code == 200
        assert b"Hello testuser!" in res.data

def test_dashboard_backend_unauthorized_logs_out(client):
    with client.session_transaction() as sess:
        sess["username"] = "testuser"

    with patch("app.backend_get") as mock_get:
        mock_get.return_value = (
            {"ok": False, "error": "Unauthorized"},
            401
        )

        res = client.get("/dashboard", follow_redirects=False)

        assert res.status_code == 302
        assert res.headers["Location"].endswith("/login")
