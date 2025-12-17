import uuid
import pytest

TEST_USERNAME = "Selenium_Tester_12345"

pytestmark = pytest.mark.order(3)

def random_domain():
    return f"test-{uuid.uuid4().hex[:8]}.com"

def test_list_domains_authorized(client):
    res = client.get(
        "/api/domains",
        headers={"X-Username": TEST_USERNAME}
    )

    assert res.status_code == 200
    data = res.get_json()
    assert data["ok"] is True
    assert isinstance(data["domains"], list)


def test_add_domain_success(client):
    domain = random_domain()

    res = client.post(
        "/api/domains",
        json={"domain": domain},
        headers={"X-Username": TEST_USERNAME}
    )

    assert res.status_code == 201
    data = res.get_json()
    assert data["ok"] is True
    assert data["domain"] == domain


def test_add_domain_duplicate(client):
    domain = random_domain()

    client.post(
        "/api/domains",
        json={"domain": domain},
        headers={"X-Username": TEST_USERNAME}
    )

    res = client.post(
        "/api/domains",
        json={"domain": domain},
        headers={"X-Username": TEST_USERNAME}
    )

    assert res.status_code == 409
    data = res.get_json()
    assert data["ok"] is False


def test_remove_domain(client):
    domain = random_domain()

    client.post(
        "/api/domains",
        json={"domain": domain},
        headers={"X-Username": TEST_USERNAME}
    )

    res = client.delete(
        "/api/domains",
        json={"domains": [domain]},
        headers={"X-Username": TEST_USERNAME}
    )

    assert res.status_code == 200
    data = res.get_json()
    assert data["ok"] is True

def test_add_domain_invalid_formats(client):
    for invalid_domain in [
        "http:///example.com",
        "example",
        "exa mple.com",
        "example!.com",
        ".com",
        "example..com"
    ]:
        res = client.post(
            "/api/domains",
            json={"domain": invalid_domain},
            headers={"X-Username": TEST_USERNAME}
        )

        assert res.status_code == 400
        data = res.get_json()
        assert data["ok"] is False
        assert "Invalid domain" in data["error"]

def test_add_domain_missing_field(client):
    res = client.post(
        "/api/domains",
        json={},
        headers={"X-Username": TEST_USERNAME}
    )

    assert res.status_code == 400
    data = res.get_json()
    assert data["ok"] is False

def test_domains_unauthorized(client):
    res = client.get("/api/domains")

    assert res.status_code == 401
    data = res.get_json()
    assert data["ok"] is False
