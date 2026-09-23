# Data Model: Gerenciamento de Tarefas

## Entity: Task

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | integer | Primary key, auto-generated | Unique identifier for each task |
| title | string | Required, trimmed, non-empty | Displayed in the task list |
| description | string | Optional | May be empty or null |
| status | string | Enum: Pendente, Em andamento, Concluída; defaults to Pendente when omitted | Controlled by user actions |
| created_at | datetime | Auto-generated | Useful for traceability |
| updated_at | datetime | Auto-generated | Useful for updates |

## Relationships

- One task has exactly one status value.
- The list view aggregates all tasks and groups them by current status.

## Validation Rules

- title must be present and cannot be blank after trimming.
- description may be omitted.
- status must be one of the valid values defined in the specification.
- invalid statuses, empty titles, or malformed task payloads must be rejected with clear feedback.

## State Transitions

- Pendente -> Em andamento
- Em andamento -> Concluída
- Em andamento -> Pendente
- Concluída -> Em andamento or Pendente (when reopened)
- Any status may be retained after editing if the user leaves it unchanged.
