from app.schemas import TaskCreate, TaskUpdate


def validate_create_payload(payload: TaskCreate) -> TaskCreate:
    return payload


def validate_update_payload(payload: TaskUpdate) -> TaskUpdate:
    if not payload.model_fields_set:
        raise ValueError("Informe ao menos um campo para atualizar.")
    return payload
