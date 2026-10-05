# Technical Documentation Rag Assistant: interview questions and answers

Answers describe this repository's current implementation. Suggested production changes are explicitly labeled as future work.

## 1. Is this an LLM or vector-search RAG implementation?

No. It ranks two in-code passages using lexical term overlap and returns the entire best passage. There are no embeddings, vector database, language model, or external document ingestion calls.

Source: [src/technicaldoc/answer.py](src/technicaldoc/answer.py).

## 2. How is overlap computed?

`words` extracts lowercase alphanumeric tokens into a set and removes a fixed stop-word set. Overlap is the size of the intersection between query terms and passage terms, so repeated words do not increase it.

Source: [src/technicaldoc/answer.py](src/technicaldoc/answer.py).

## 3. When does it refuse to answer?

When the best passage has overlap below `MIN_OVERLAP`, currently 2, the response sets `answered: false`, supplies a refusal string, and sets the citation to null.

Source: [src/technicaldoc/answer.py](src/technicaldoc/answer.py).

## 4. How is the optional source filter applied?

An explicit source restricts the corpus to passages with that exact source name. If none remain, `InputError` becomes HTTP 422. This is source selection, not user authorization.

Source: [src/technicaldoc/answer.py](src/technicaldoc/answer.py).

## 5. How are ties ordered?

Results sort by descending overlap and then ascending source name. This produces deterministic ranking, but alphabetical precedence is not evidence of higher relevance.

Source: [src/technicaldoc/answer.py](src/technicaldoc/answer.py).

## 6. What is returned for a successful answer?

The response contains `answered: true`, the best passage text, its source filename as `citation`, and the ranked passage records. It does not generate a new synthesized answer.

Source: [src/technicaldoc/answer.py](src/technicaldoc/answer.py).

## 7. Does the threshold guarantee grounded correctness?

No. Two shared words can still be irrelevant, and a correct paraphrase can have low overlap. Evaluate answerable and unanswerable queries rather than treating overlap as semantic confidence.

Source: [src/technicaldoc/answer.py](src/technicaldoc/answer.py).

## 8. How would you evolve retrieval?

Add controlled document ingestion and source identifiers, evaluate lexical retrieval first, then compare dense or hybrid retrieval and reranking. Preserve a refusal path and test citation fidelity.

Source: [src/technicaldoc/answer.py](src/technicaldoc/answer.py).

## 9. How are the domain API and ops plane connected?

The app registers the ops router under `/v1`, alongside the domain endpoint. Creating or approving a job updates ops records; it does not call the domain function. There is no background worker or job executor.

Source: [src/technicaldoc/main.py](src/technicaldoc/main.py).

## 10. Does X-Tenant-Id authenticate a user?

No. It is a caller-supplied header defaulting to `default`. Workspace and job reads filter by that value, but a caller can choose another value. Real identity and authorization would need to precede this lab tenant selector.

Source: [src/technicaldoc/ops.py](src/technicaldoc/ops.py).

## 11. What survives a process restart?

Nothing in the ops dictionaries or audit list is persisted. Multiple server workers would also have separate state. Durable storage, transactions, and a shared job queue are future changes.

Source: [src/technicaldoc/ops.py](src/technicaldoc/ops.py).

## 12. What happens when a production job is approved?

Targets exactly equal to `prod` or `production` create a `pending_approval` job and approval returns HTTP 403. Other target strings are queued. Approval of a lab job changes its status only; it does not execute a workload.

Source: [src/technicaldoc/ops.py](src/technicaldoc/ops.py).

## 13. Are audit and metrics equally tenant-scoped?

Audit results filter events by the tenant and its workspace/job identifiers. `/v1/metrics` returns process-wide counters without tenant filtering, so it is not a tenant-specific dashboard. Domain requests are not automatically audited.

Source: [src/technicaldoc/ops.py](src/technicaldoc/ops.py).

## 14. What would you prioritize before a customer deployment?

Define authenticated identities and permission checks, durable state, typed domain inputs, bounded requests, concurrency behavior, and observable execution semantics. Use the existing tests as a baseline, then test failure and access boundaries rather than claiming the lab is production-ready.

Source: [src/technicaldoc/ops.py](src/technicaldoc/ops.py).
