from unittest.mock import patch

def test_add_domain_requires_login(client):
    res = client.post("/add_domain", json={"domain": "example.com"})
    assert res.status_code == 401

def test_add_domain_success(client):
    with client.session_transaction() as sess:
        sess["username"] = "testuser"

    with patch("app.backend_post") as mock_post:
        mock_post.return_value = (
            {"ok": True, "domain": "example.com"},
            201
        )

        res = client.post("/add_domain", json={"domain": "example.com"})

        assert res.status_code == 201
        assert res.get_json()["ok"] is True

def test_remove_domains_success(client):
    with client.session_transaction() as sess:
        sess["username"] = "testuser"

    with patch("app.backend_delete") as mock_delete:
        mock_delete.return_value = (
            {"ok": True},
            200
        )

        res = client.post("/remove_domains", json={"domains": ["example.com"]})

        assert res.status_code == 200
        assert res.get_json()["ok"] is True
