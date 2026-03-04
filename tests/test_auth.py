from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_query_requires_api_key():
    response = client.post(
        "/query",
        json={"q": "¿Qué es LlamaIndex?"}
    )
    assert response.status_code in [401, 422]