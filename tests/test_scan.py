import io
import uuid
import pytest

TEST_USERNAME = "Selenium_Tester_12345"

pytestmark = pytest.mark.order(5)


def random_domain():
    return f"scan-{uuid.uuid4().hex[:8]}.com"

def test_scan_domains_success(client):
    domain = random_domain()

    # Ensure domain exists
    client.post(
        "/api/domains",
        json={"domain": domain},
        headers={"X-Username": TEST_USERNAME}
    )

    res = client.post(
        "/api/scan",
        headers={"X-Username": TEST_USERNAME}
    )

    assert res.status_code == 200

    data = res.get_json()
    assert data["ok"] is True
    assert isinstance(data["updated"], int)


def test_scan_domains_unauthorized(client):
    res = client.post("/api/scan")

    assert res.status_code == 401
    data = res.get_json()
    assert data["ok"] is False


