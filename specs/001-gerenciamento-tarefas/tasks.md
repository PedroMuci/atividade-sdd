---

description: "Task list for the task management application"
---

# Tasks: Gerenciamento de Tarefas

**Input**: Design documents from `/specs/001-gerenciamento-tarefas/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/task-api.md, quickstart.md

**Tests**: Included because the Constitution requires automated, repeatable tests for the main functionality and the plan defines Pytest with the FastAPI test client.

**Organization**: Tasks are grouped by user story to enable independent implementation and validation.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize the Python web application and the local/container execution files.

- [X] T001 [P] Create the Python dependency manifest with Python 3.11-compatible FastAPI, Jinja2, SQLAlchemy, Pytest, HTTPX, and Uvicorn dependencies in `requirements.txt`
- [X] T002 [P] Create the application container image with Python 3.11, dependency installation, `/app/data` setup, and Uvicorn startup in `Dockerfile`
- [X] T003 [P] Configure the local and production-equivalent service, `DATABASE_URL=sqlite:////app/data/tasks.db`, and named volume `task_data:/app/data` in `docker-compose.yml`
- [X] T004 [P] Create the planned package, route, service, validator, template, static, and test directories with package markers in `app/__init__.py` and `app/routes/__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement shared persistence, validation, error handling, and test configuration required by all stories.

**Checkpoint**: The application foundation can create a database session, validate Task data, and expose a testable FastAPI application before story-specific work begins.

- [X] T005 [P] Implement environment-based SQLite engine, session factory, and table initialization with the default database path in `app/database.py`
- [X] T006 [P] Implement the SQLAlchemy Task entity with `id` as an auto-generated primary key, required trimmed non-empty `title`, optional `description`, status enum values `Pendente`, `Em andamento`, and `Concluída`, defaulting to `Pendente` when omitted, and generated `created_at` and `updated_at` fields in `app/models.py`
- [X] T007 [P] Implement request and response schemas for Task creation, update, and serialization, including optional description, the three allowed status values, and `Pendente` as the default when status is omitted, in `app/schemas.py`
- [X] T008 [P] Implement shared validation rules in `app/validators/task_validators.py`: title must be present and non-blank after trimming, title maximum 200 characters, description maximum 2000 characters, and malformed or invalid status values must be rejected before persistence
- [X] T009 Implement service-layer error types and consistent handling for validation, not-found, and persistence failures in `app/services/task_service.py`
- [X] T010 Implement the FastAPI application factory, database initialization, template/static mounting, and shared error responses without authentication in `app/main.py`
- [X] T011 [P] Create isolated test database fixtures, FastAPI test client setup, and database cleanup behavior in `tests/conftest.py`

---

## Phase 3: User Story 1 - Visualizar e revisar tarefas cadastradas (Priority: P1) 🎯 MVP

**Goal**: Users can open the browser application and see every registered task or a clear empty-state message.

**Independent Test**: Open the main page with an empty database and with seeded tasks; confirm the empty-state message or all task identifiers, titles, descriptions, and statuses are rendered.

### Tests for User Story 1

- [X] T012 [P] [US1] Add API and browser integration tests for `GET /` covering the empty-state message and rendering of all task fields in `tests/test_tasks_api.py` and `tests/test_tasks_ui.py`

### Implementation for User Story 1

- [X] T013 [US1] Implement task listing and empty-state retrieval in `app/services/task_service.py`, returning all tasks grouped by current status without modifying records
- [X] T014 [US1] Implement `GET /` and `GET /tasks/{id}` according to `contracts/task-api.md`, including clear not-found feedback, in `app/routes/tasks.py`
- [X] T015 [US1] Create the shared page layout and task list/empty-state markup in `app/templates/base.html` and `app/templates/tasks.html`
- [X] T016 [P] [US1] Add responsive task list styling and status presentation in `app/static/css/styles.css`

**Checkpoint**: User Story 1 is independently usable and testable through the browser and `GET /`.

---

## Phase 4: User Story 2 - Criar e editar tarefas (Priority: P1)

**Goal**: Users can create a task with a required title and optional description, then edit its title, description, or status with clear validation feedback.

**Independent Test**: Submit a valid task, verify it appears in the list, update its title or description, and verify invalid title, description, status, or malformed payload submissions are rejected without persistence.

### Tests for User Story 2

- [X] T017 [P] [US2] Add API contract tests for `POST /tasks` and `PUT /tasks/{id}` covering valid creation, editing, required trimmed title, optional description, status values, 200/2000-character limits, and invalid payload errors in `tests/test_tasks_api.py`
- [X] T018 [P] [US2] Add browser flow tests for the create and edit forms, success feedback, and validation error display in `tests/test_tasks_ui.py`

### Implementation for User Story 2

- [X] T019 [US2] Implement create and update service operations with atomic validation and timestamps in `app/services/task_service.py`
- [X] T020 [US2] Implement `POST /tasks` and `PUT /tasks/{id}` using the task schemas and shared validators, returning clear errors without silent failure, in `app/routes/tasks.py`
- [X] T021 [US2] Add create and edit forms with field-level error presentation to `app/templates/tasks.html`
- [X] T022 [P] [US2] Implement browser form submission, success feedback, and validation-error rendering in `app/static/js/app.js`

**Checkpoint**: User Stories 1 and 2 are independently usable; users can list, create, edit, and validate tasks.

---

## Phase 5: User Story 3 - Alterar status e remover tarefas (Priority: P1)

**Goal**: Users can move tasks among the allowed statuses and delete tasks without affecting other records.

**Independent Test**: Change a task through valid statuses, attempt an invalid status or unknown identifier, delete one task, and verify the remaining list and clear error feedback.

### Tests for User Story 3

- [X] T023 [P] [US3] Add API tests for status changes through `PUT /tasks/{id}`, `DELETE /tasks/{id}`, invalid status values, and unknown identifiers in `tests/test_tasks_api.py`
- [X] T024 [P] [US3] Add browser flow tests for status controls, delete confirmation, removal from the list, and operation error feedback in `tests/test_tasks_ui.py`

### Implementation for User Story 3

- [X] T025 [US3] Implement status transition and deletion operations with not-found handling and transaction rollback on persistence failure in `app/services/task_service.py`
- [X] T026 [US3] Complete status update and `DELETE /tasks/{id}` route behavior according to `contracts/task-api.md` in `app/routes/tasks.py`
- [X] T027 [US3] Add status controls, delete action, confirmation, and operation feedback to `app/templates/tasks.html` and `app/static/js/app.js`

**Checkpoint**: User Stories 1, 2, and 3 are independently functional for the complete task lifecycle.

---

## Phase 6: User Story 4 - Persistir dados e operar em navegação simples (Priority: P2)

**Goal**: Tasks remain available after application restart and the responsive browser interface works without authentication.

**Independent Test**: Create a task, restart the application using the same SQLite volume, reload the browser, and confirm the task remains available without login.

### Tests for User Story 4

- [X] T028 [P] [US4] Add persistence integration tests that create tasks, recreate the application session against the same SQLite database, and verify records remain available in `tests/test_tasks_api.py`
- [X] T029 [P] [US4] Add browser smoke coverage for unauthenticated access, responsive task layout, and navigation from the root page in `tests/test_tasks_ui.py`

### Implementation for User Story 4

- [X] T030 [US4] Verify database initialization and session lifecycle preserve data across application restart while retaining rollback behavior in `app/database.py` and `app/services/task_service.py`
- [X] T031 [US4] Complete responsive layout, accessible form controls, and browser navigation behavior in `app/templates/base.html`, `app/templates/tasks.html`, and `app/static/css/styles.css`
- [ ] T032 [US4] Validate Docker Compose volume persistence and browser access at `http://localhost:8000` using `docker-compose.yml` and the documented quickstart flow

**Checkpoint**: The complete academic task manager persists data and operates through a browser without authentication.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Finish quality gates, documentation, deployment automation, and final validation.

- [X] T033 [P] Add repository-level test, security analysis, SonarQube Cloud, Docker build, and deploy-gate jobs triggered from `main` in `.github/workflows/pipeline.yml`
- [X] T034 [P] Configure SonarQube Cloud project metadata and source/test exclusions without embedding tokens or credentials in `sonar-project.properties`
- [X] T035 [P] Document objective, architecture, technologies, local setup, Docker usage, SQLite volume persistence, CI/CD, SonarQube Cloud, GitHub Actions Secrets, and AWS EC2 deployment in `README.md`
- [ ] T036 Run the complete Pytest suite and quickstart validation scenarios, then record any required corrections in `tests/test_tasks_api.py`, `tests/test_tasks_ui.py`, or `README.md`
- [ ] T037 Run a final security and repository hygiene review to confirm no credentials, tokens, SSH keys, or sensitive deployment values are committed, using `.github/workflows/pipeline.yml` and `README.md` as the operational references
- [ ] T038 Provision and configure a suitable AWS EC2 Linux instance, including the application host settings and a Security Group that permits SSH administration and public HTTP access required by the application, documenting the procedure in `README.md`
- [ ] T039 Prepare the EC2 instance to run the project with Docker and Docker Compose, including the required runtime directories and permissions, documenting the commands in `README.md`
- [ ] T040 Configure the GitHub Actions repository secrets for the EC2 host, SSH username, and private SSH key, and document the required secret names and usage without storing their values in `README.md` or any repository file
- [ ] T041 Implement the automatic EC2 deployment job in `.github/workflows/pipeline.yml`, executing only after tests, SonarQube Cloud analysis, and Docker image build complete successfully, and connecting with the configured SSH secrets
- [ ] T042 Configure the EC2 deployment commands to recreate or update the application without removing the Docker named volume `task_data`, preserving the SQLite database across new versions through `docker-compose.yml`, `.github/workflows/pipeline.yml`, and `README.md`
- [ ] T043 Validate the production deployment from an external browser or HTTP request and document the public EC2 address and successful application reachability in `README.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; T001-T004 can run in parallel.
- **Foundational (Phase 2)**: Depends on Phase 1; T005-T008 and T011 can run in parallel, then T009-T010 complete the shared application foundation.
- **User Stories (Phases 3-6)**: Depend on Phase 2 completion. US1, US2, and US3 are priority P1; US4 is P2. After the foundation, story work can be parallelized by separate contributors, although US2 and US3 reuse the list UI and routes from US1.
- **Polish (Phase 7)**: Depends on all required user stories; T033-T035 can run in parallel, T036-T037 run after the application and pipeline files exist, and T038-T043 complete the infrastructure and deployment sequence.

### User Story Dependencies

- **User Story 1 (P1)**: Depends only on Phase 2 and is the MVP increment.
- **User Story 2 (P1)**: Depends on Phase 2; it reuses the list page from US1 for visible results but remains independently testable through `POST /tasks` and `PUT /tasks/{id}`.
- **User Story 3 (P1)**: Depends on Phase 2; it reuses the task list and update contract but is independently testable through status and delete operations.
- **User Story 4 (P2)**: Depends on Phase 2 and the application container files; it validates persistence and browser operation across the complete workflow.

### Parallel Opportunities

- Setup files T001-T004 are independent.
- Foundation model, schemas, validators, and test fixtures T005-T008 and T011 can be developed in parallel.
- Within each story, API and UI tests are parallel; CSS/static work can proceed alongside route work when dependencies are respected.
- T033-T035 are independent polish deliverables and can proceed in parallel after the core application exists.
- T038 and T039 can proceed in parallel before the first deployment; T040 can be prepared in parallel with the EC2 setup; T041 depends on the pipeline gates and configured secrets; T042 depends on the deployment job; T043 runs after the deployment completes.

---

## Parallel Example: User Story 1

```text
Task: "T012 [US1] Add API and browser integration tests in tests/test_tasks_api.py and tests/test_tasks_ui.py"
Task: "T016 [P] [US1] Add responsive task list styling in app/static/css/styles.css"
```

## Parallel Example: User Story 2

```text
Task: "T017 [P] [US2] Add POST and PUT contract tests in tests/test_tasks_api.py"
Task: "T018 [P] [US2] Add create and edit browser flow tests in tests/test_tasks_ui.py"
Task: "T022 [P] [US2] Implement browser form submission in app/static/js/app.js"
```

## Parallel Example: User Story 3

```text
Task: "T023 [P] [US3] Add status and delete API tests in tests/test_tasks_api.py"
Task: "T024 [P] [US3] Add status and delete browser flow tests in tests/test_tasks_ui.py"
```

## Parallel Example: User Story 4

```text
Task: "T028 [P] [US4] Add restart persistence tests in tests/test_tasks_api.py"
Task: "T029 [P] [US4] Add unauthenticated browser smoke coverage in tests/test_tasks_ui.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational.
3. Complete Phase 3: User Story 1.
4. Run the US1 API/UI tests and validate the empty state and task listing independently.
5. Demonstrate the first browser-accessible increment before adding mutations.

### Incremental Delivery

1. Complete Setup + Foundational and verify the database, validation, and test fixtures.
2. Add US1 and validate the list/empty-state MVP.
3. Add US2 and validate create/edit flows.
4. Add US3 and validate status/delete flows.
5. Add US4 and validate restart persistence and browser operation.
6. Complete Phase 7 and run the full quality, security, Docker, CI/CD, and documentation checks.

### Parallel Team Strategy

1. Complete Setup and the blocking foundation together.
2. After Phase 2, assign US1, US2, and US3 to separate contributors with coordinated changes to shared templates and routes.
3. Assign US4 to the contributor handling Docker/database validation.
4. Run Phase 7 only after the story checkpoints pass.

---

## Notes

- Every task uses the required checkbox, sequential ID, optional `[P]` marker, story label where required, and exact file paths.
- Tests are written before their story implementation tasks and should fail before the corresponding implementation exists.
- The implementation must preserve the no-authentication scope and must not introduce React, Kubernetes, RDS, queues, cache, microservices, or other unnecessary technologies.
