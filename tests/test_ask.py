from fastapi.testclient import TestClient
from technicaldoc.main import app

client = TestClient(app)


def test_answers_and_refuses():
    hit = client.post("/ask", json={"question": 'How do readiness probes gate traffic?'}).json()
    assert hit["answered"] is True
    assert hit["citation"] == "probes.md"
    miss = client.post("/ask", json={"question": 'orbital mechanics homework'}).json()
    assert miss["answered"] is False


def test_empty_is_refused():
    assert client.post("/ask", json={"question": " "}).status_code == 422
