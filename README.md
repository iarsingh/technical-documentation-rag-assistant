# Technical Documentation RAG Assistant

Level: 6 — Beginner RAG

Skills: Python, local retrieval, a refusal

Answer only from a tiny local corpus. A question with too little overlap is refused.

```bash
pip install -r requirements.txt
pytest -q
```

This is a local laptop proof. It does not call a hosted model and it does not apply production changes.

## Ops plane

Workspaces, tenant isolation, job approval, and audit live under `/v1`. Production apply is refused. See `docs/ARCHITECTURE.md`.
