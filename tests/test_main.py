from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

def test_health_check_endpoint():
    """اختبار GET / health check."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@patch("src.routers.query_router.rag_service.answer_ticket")
def test_query_endpoint_success(mock_answer_ticket):
    """اختبار POST /api/v1/query."""
    mock_answer_ticket.return_value = {
        "ticket": "النت فاصل", "response": "تمام", "sources_count": 2,
        "execution_time_seconds": 0.3, "prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15
    }
    response = client.post("/api/v1/query", json={"ticket": "النت فاصل"})
    assert response.status_code == 200
    assert response.json()["sources_count"] == 2