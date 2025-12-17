from unittest.mock import patch

def test_login_success(client):
    with patch("app.backend_post") as mock_post:
        mock_post.return_value = (
            {"ok": True, "username": "testuser"},
            200
        )

        res = client.post(
            "/login",
            json={"username": "testuser", "password": "pass"}
        )

        assert res.status_code == 200
        assert res.get_json()["ok"] is True


def test_login_failure(client):
    with patch("backend_client.backend_post") as mock_post:
        mock_post.return_value = (
            {"ok": False, "error": "Invalid credentials"},
            401
        )

        res = client.post(
            "/login",
            json={"username": "bad", "password": "bad"}
        )

        assert res.status_code == 401
        assert "error" in res.get_json()


def test_logout_clears_session(client):
    with client.session_transaction() as sess:
        sess["username"] = "testuser"

    res = client.get("/logout")
    assert res.status_code == 302

    with client.session_transaction() as sess:
        assert "username" not in sess
