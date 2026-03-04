from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

API_KEY = "supersecret"


def test_query_success():
    response = client.post(
        "/query",
        headers={"X-API-Key": API_KEY},
        json={"q": "¿Qué es LlamaIndex?"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "sources" in data
    assert "retrieval_params" in data