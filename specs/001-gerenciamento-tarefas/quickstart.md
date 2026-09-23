# Quickstart: Gerenciamento de Tarefas

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- GitHub repository configured for CI/CD
- AWS EC2 instance for production deployment

## Local setup

1. Create a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Start the application with `uvicorn app.main:app --reload`.
4. Open the application in a browser at `http://localhost:8000`.

## Docker setup

1. Build the image with `docker build -t task-manager .`.
2. Start the application with Docker Compose:
   `docker compose up --build`
3. The SQLite database is stored in a named Docker volume named `task_data`, so task data remains available even if the container is recreated during deployment.
4. Validate the UI and CRUD flows in the browser at `http://localhost:8000`.

## Deployment notes

- Keep the SQLite database inside the Docker volume mounted at `/app/data`.
- When deploying to EC2, keep the same volume mapping in the production container so data survives container refreshes.
- Do not store credentials or SSH keys in the repository; use GitHub Actions Secrets and environment variables instead.

## Validation scenarios

- Create a new task and confirm it appears in the task list.
- Edit an existing task and verify the updated title or description is shown.
- Change status from Pendente to Em andamento and then to Concluída.
- Delete a task and verify it is removed from the list.
- Restart the application and confirm data remains available.
- Attempt to save a task without a valid title to confirm validation errors.
- Run the automated Pytest suite and confirm the valid CRUD flow tests complete successfully.
- Manually inspect the main interface and confirm that each task's status and details are clearly identifiable without formal usability research.

## Production readiness

1. Ensure GitHub Actions Secrets contain all sensitive values.
2. Run the full pipeline: install, tests, SonarQube, Docker build.
3. Verify that deployment only proceeds after all checks pass.
4. Confirm the application is reachable via the EC2 public URL.
