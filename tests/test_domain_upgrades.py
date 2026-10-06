import pytest
from fastapi.testclient import TestClient
from technicaldoc.main import app

client = TestClient(app)


def test_retrieval_reports_matched_terms_and_coverage():
    r = client.post("/ask", json={"question": "readiness probes gate traffic"}).json()
    assert r["answered"] is True
    best = r["passages"][0]
    assert best["matched_terms"] == ["gate", "probes", "readiness", "traffic"]
    assert best["query_coverage"] == 1.0


@pytest.mark.parametrize("source", [[], {}, 42])
def test_source_must_be_a_string(source):
    assert client.post("/ask", json={"question": "readiness probes", "source": source}).status_code == 422


def test_oversized_query_is_rejected():
    assert client.post("/ask", json={"question": "x" * 2001}).status_code == 422
