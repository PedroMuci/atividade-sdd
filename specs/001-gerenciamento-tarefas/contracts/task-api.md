# Task API Contract

## Overview

This project exposes a simple web application interface for task management. The primary contract is browser-driven HTTP interaction with server-rendered pages and JSON-friendly backend endpoints for the task operations.

## Endpoints

### GET /
- Returns the task list page.
- If no tasks exist, shows an empty-state message.

### POST /tasks
- Creates a new task.
- Requires a title.
- Accepts an optional description and status.
- Rejects invalid payloads with a clear error response.

### GET /tasks/{id}
- Retrieves a single task record.

### PUT /tasks/{id}
- Updates an existing task.
- Supports title, description, and status modification.

### DELETE /tasks/{id}
- Deletes the task.
- Returns success or error feedback.

## Validation Contract

- Empty or whitespace title values, titles longer than 200 characters, and descriptions longer than 2000 characters are rejected.
- Only statuses `Pendente`, `Em andamento`, and `Concluída` are accepted.
- Malformed payloads are rejected before persistence.
- Requests for an unknown task identifier return a clear not-found error and do not modify other tasks.
- Persistence failures return a clear error and do not report the change as completed.
- Errors return clear user-facing messages and do not silently fail.
