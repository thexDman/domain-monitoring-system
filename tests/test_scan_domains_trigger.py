from unittest.mock import patch

def test_scan_domains_success(client):
    with client.session_transaction() as sess:
        sess["username"] = "testuser"

    with patch("app.backend_post") as mock_post:
        mock_post.return_value = (
            {"ok": True, "updated": 3},
            200
        )

        res = client.post("/scan_domains")

        assert res.status_code == 200
        assert res.get_json()["ok"] is True
