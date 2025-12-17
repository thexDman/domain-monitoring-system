import io
import uuid
import pytest

TEST_USERNAME = "Selenium_Tester_12345"

pytestmark = pytest.mark.order(4)

def make_domain():
    return f"bulk-{uuid.uuid4().hex[:8]}.com"

def test_bulk_upload_success(client):
    domains = [make_domain(), make_domain()]

    file_content = "\n".join(domains)
    file = (io.BytesIO(file_content.encode()), "domains.txt")

    res = client.post(
        "/api/domains/bulk",
        data={"file": file},
        headers={"X-Username": TEST_USERNAME},
        content_type="multipart/form-data"
    )

    assert res.status_code == 200
    data = res.get_json()
    assert data["ok"] is True
    assert len(data["summary"]["added"]) == 2

def test_bulk_upload_with_invalid_domains(client):
    valid = make_domain()
    invalid = "invalid domain"

    file_content = f"{valid}\n{invalid}"
    file = (io.BytesIO(file_content.encode()), "domains.txt")

    res = client.post(
        "/api/domains/bulk",
        data={"file": file},
        headers={"X-Username": TEST_USERNAME},
        content_type="multipart/form-data"
    )

    assert res.status_code == 200
    data = res.get_json()

    assert valid in data["summary"]["added"]
    assert len(data["summary"]["invalid"]) == 1

def test_bulk_upload_missing_file(client):
    res = client.post(
        "/api/domains/bulk",
        headers={"X-Username": TEST_USERNAME}
    )

    assert res.status_code == 400
    data = res.get_json()
    assert data["ok"] is False

def test_bulk_upload_wrong_file_type(client):
    file = (io.BytesIO(b"test"), "domains.pdf")

    res = client.post(
        "/api/domains/bulk",
        data={"file": file},
        headers={"X-Username": TEST_USERNAME},
        content_type="multipart/form-data"
    )

    assert res.status_code == 400
