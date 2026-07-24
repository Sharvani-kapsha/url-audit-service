from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "URL Audit Service is running!"

def test_invalid_url():
    response = client.post(
        "/audit",
        json={"url": "not-a-url"}
    )

    assert response.status_code == 422

def test_valid_url():
    response = client.post(
        "/audit",
        json={"url": "https://google.com"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "title" in data
    assert "status_code" in datapyt