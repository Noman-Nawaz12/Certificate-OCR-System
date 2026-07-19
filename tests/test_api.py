from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_home_page_loads():
    response = client.get("/")
    assert response.status_code == 200


def test_extract_rejects_bad_file_type():
    response = client.post(
        "/extract",
        files={"file": ("test.txt", b"hello world", "text/plain")}
    )
    assert response.status_code == 400
