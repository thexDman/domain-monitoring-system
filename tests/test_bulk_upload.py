from unittest.mock import patch
import io

def test_bulk_upload_requires_login(client):
    res = client.post("/bulk_domains")
    assert res.status_code == 401

def test_bulk_upload_success(client):
    with client.session_transaction() as sess:
        sess["username"] = "testuser"

    with patch("app.backend_post") as mock_post:
        mock_post.return_value = (
            {"ok": True, "summary": {"added": ["a.com"]}},
            200
        )

        data = {
            "file": (io.BytesIO(b"a.com\nb.com"), "domains.txt")
        }

        res = client.post("/bulk_domains", data=data)

        assert res.status_code == 200
        assert res.get_json()["ok"] is True
