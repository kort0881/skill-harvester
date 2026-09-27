---
name: "app-platform-router"
description: "Routes DigitalOcean App Platform requests to specialized sub‑skills, enabling AI assistants to orchestrate multi‑phase workflows while keeping credentials safe."
---

# Overview
This skill acts as a router for DigitalOcean App Platform tasks. Based on a user’s intent it selects one or more specialized sub‑skills (designer, migration, deployment, etc.) and defines the artifact hand‑off between them.

## Prerequisites
- `doctl` ≥ 1.82.0
- Python 3.9+ with the `do-app-sandbox` package (`pip install do-app-sandbox`)
- Access to the repository containing the sub‑skills (`app-platform-skills/skills/*`)
- Optional: `uv` for Python package management, Docker for devcontainers

## Input / Output
- **Input**: a free‑form user request string (e.g., "I want to migrate my Heroku app")
- **Output**: the name of the primary skill to invoke and, if applicable, an ordered list of additional skills to chain.

## Routing Decision Tree
```
User Request
   │
   ├─ Development? → devcontainers
   ├─ Designing / Creating? → designer / migration / planner
   ├─ Shipping code? → deployment
   ├─ Something broken? → troubleshooting
   ├─ Need isolated execution? → sandbox
   ├─ Configuring data? → postgres / managed-db-services / spaces
   └─ AI inference needed? → ai-services
```
The tree is implemented as a simple rule‑based matcher using the **Trigger Phrases Reference** table below.

## Trigger Phrases Reference
| Skill | Trigger phrases |
|-------|-----------------|
| devcontainers | "local dev", "docker compose", "run locally", "devcontainer" |
| designer | "design my app", "create app spec", "new application", "architect" |
| migration | "migrate", "convert", "move from Heroku", "move from AWS", "heroku.yml" |
| planner | "create a plan", "staged approach", "plan deployment" |
| deployment | "deploy", "ship", "release", "GitHub Actions" |
| troubleshooting | "broken", "failing", "debug", "502", "error" |
| sandbox | "sandbox", "isolated environment", "run untrusted code" |
| postgres | "postgres", "postgresql", "schema isolation" |
| managed-db-services | "mysql", "mongodb", "kafka", "opensearch" |
| spaces | "object storage", "S3", "Spaces" |
| ai-services | "gradient", "inference", "LLM endpoint" |

## Workflow Chaining Examples
1. **Greenfield app** – `devcontainers → designer → planner → deployment`
2. **Heroku migration** – `migration → planner → deployment`
3. **Add Kafka** – `managed-db-services → update .do/app.yaml → deployment`
4. **Troubleshoot 502** – `troubleshooting` (stand‑alone)

## Artifact Contracts
| Artifact | Filename | Produced by | Consumed by |
|----------|----------|-------------|------------|
| App Spec | `.do/app.yaml` | designer, migration | deployment, planner |
| Deploy workflow | `.github/workflows/deploy.yml` | deployment, planner | GitHub Actions |
| Dev environment | `.devcontainer/devcontainer.json` | devcontainers | VS Code |
| SQL scripts | `db-*.sql` | postgres | User (manual) |
| CORS config | `spaces-cors.json` | spaces | DO Console |

When a skill finishes it should announce the artifact(s) created and suggest the next skill if applicable.

## Credential Handling Philosophy
1. **Prefer GitHub Secrets** – the agent never sees the secret value.
2. **Use App Platform bindable variables** for DO managed databases.
3. **Local .env** only for temporary testing.
4. **External services** follow the same pattern as #1 or #3.

## Implementation Sketch (pseudo‑code)
```python
def route(request: str) -> List[str]:
    # lower‑case and tokenise request
    tokens = request.lower().split()
    # ordered list of (skill, trigger list)
    triggers = [
        ("devcontainers", ["local dev", "docker compose", "devcontainer"]),
        ("designer", ["design my app", "new application", "architect"]),
        ("migration", ["migrate", "heroku", "aws"]),
        ("planner", ["create a plan", "staged approach"]),
        ("deployment", ["deploy", "release", "github actions"]),
        ("troubleshooting", ["broken", "502", "debug"]),
        ("sandbox", ["sandbox", "isolated environment"]),
        ("postgres", ["postgres", "postgresql"]),
        ("managed-db-services", ["mysql", "mongodb", "kafka"]),
        ("spaces", ["s3", "object storage"]),
        ("ai-services", ["inference", "llm endpoint"]),
    ]
    for skill, phrases in triggers:
        if any(p in request.lower() for p in phrases):
            return [skill]
    return []
```
The AI assistant can extend this list with chaining logic based on the **Workflow Types** table in the original document.

## Escalation
If the request does not match any known trigger, ask the user for clarification or fall back to the official App Platform documentation: https://docs.digitalocean.com/products/app-platform/
