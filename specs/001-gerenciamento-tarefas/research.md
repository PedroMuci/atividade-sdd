# Research: Gerenciamento de Tarefas

## Decision

Use a simple FastAPI + SQLAlchemy + SQLite application with server-rendered Jinja2 templates and a small static JavaScript layer for browser interaction.

## Rationale

This architecture matches the academic scope, keeps implementation and maintenance simple, and satisfies the project requirements for task CRUD, persistence, and a browser-based UI without requiring authentication or extra infrastructure.

## Alternatives considered

- Full SPA with React: rejected because it introduces unnecessary complexity for a small project and exceeds the requested simplicity constraints.
- PostgreSQL or MySQL: rejected because SQLite is simpler, sufficient for the activity, and matches the requirement to persist data on the server.
- Separate microservice structure: rejected because it adds operational complexity and is explicitly disallowed by the project constraints.
- LocalStorage-only persistence: rejected because the requirement says persistence should survive restarts and the additional server-side requirement favors SQLite.

## Findings

- FastAPI is a lightweight Python web framework well-suited for CRUD interfaces and simple HTML-based pages.
- Jinja2 is appropriate for rendering server-driven pages without introducing a heavy frontend framework.
- SQLAlchemy offers a clean ORM layer for SQLite while keeping the application easy to understand.
- GitHub Actions can enforce installation, Pytest execution, quality analysis, Docker build, and deploy gating with environment secrets.
- SonarQube Cloud is compatible with a GitHub-based pipeline and supports the security and quality checks required by the constitution.
