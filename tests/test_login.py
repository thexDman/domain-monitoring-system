import pytest
pytestmark = pytest.mark.order(2)

def test_login_success(client):
    res = client.post(
        "/api/login",
        json={
            "username": "Selenium_Tester_12345",
            "password": "St87654321"
        }
    )

    assert res.status_code == 200

    data = res.get_json()
    assert data["ok"] is True
    assert data["username"] == "Selenium_Tester_12345"


def test_login_failure_wrong_password(client):
    res = client.post(
        "/api/login",
        json={
            "username": "Selenium_Tester_12345",
            "password": "WRONGPASS"
        }
    )

    assert res.status_code == 401

    data = res.get_json()
    assert data["ok"] is False
