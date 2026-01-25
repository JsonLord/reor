from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from backend.main import app
from backend.database import get_db

mock_db = MagicMock()
app.dependency_overrides[get_db] = lambda: mock_db

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_embedding():
    with patch("backend.llm.get_embedding") as mock_get_embedding:
        mock_get_embedding.return_value = [0.1, 0.2, 0.3]
        response = client.post("/api/embeddings", json={"text": "test"})
        assert response.status_code == 200
        assert response.json() == {"embedding": [0.1, 0.2, 0.3]}

def test_answer_query():
    with patch("backend.llm.answer_question") as mock_answer_question:
        mock_db.search.return_value = "context"
        mock_answer_question.return_value = "answer"
        response = client.post("/api/query", json={"question": "question"})
        assert response.status_code == 200
        assert response.json() == {"answer": "answer"}

def test_search():
    mock_db.search.return_value = ["result1", "result2"]
    response = client.get("/api/search?query=test")
    assert response.status_code == 200
    assert response.json() == {"results": ["result1", "result2"]}
