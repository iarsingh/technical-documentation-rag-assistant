# Technical Documentation Rag Assistant: process flows

## Domain request

Endpoint: `POST /ask`. Input: question + optional source. The processing stages below summarize [answer.py](../src/technicaldoc/answer.py); they are local function behavior, not externally executed tools.

```mermaid
flowchart TD
  A["POST /ask"] --> B{"Non-empty string question?"}
  B -->|"No"| E["HTTP 422"]
  B -->|"Yes"| S["Filter corpus if source supplied"]
  S -->|"Unknown source"| E
  S --> T["Extract unique terms; remove stop words"]
  T --> R["Rank overlap descending; source name ascending"]
  R --> G{"Best overlap at least 2?"}
  G -->|"Yes"| Y["Return passage text and source citation"]
  G -->|"No"| N["Return refusal; null citation"]
```

Refusal responses, where implemented, are normal domain results rather than successful execution of a requested write. Detailed edge cases are covered in [INTERVIEW_QA.md](../INTERVIEW_QA.md).

## Workspace and job approval

```mermaid
flowchart TD
  C["Create tenant-scoped workspace"] --> J["Submit job: workspace + payload + target"]
  J --> V{"Workspace belongs to selected tenant?"}
  V -->|"No"| E["HTTP 404"]
  V -->|"Yes"| P{"Target is prod or production?"}
  P -->|"Yes"| Q["pending_approval"]
  P -->|"No"| L["queued"]
  Q --> A["Approval request"]
  A --> X["HTTP 403: production apply disabled"]
  L --> B["Approval request"]
  B --> K["approved: status update only"]
  K --> S["No executor / no production apply"]
```

Approval first checks job ownership using the selected tenant. Status changes and audit records remain in memory. The approval endpoint does not enforce a full transition state machine: repeated lab approval is possible. The domain request flow and this job-record flow are independent. Source: [ops.py](../src/technicaldoc/ops.py).
