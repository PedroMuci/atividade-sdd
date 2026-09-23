from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskCreate, TaskUpdate
from app.validators.task_validators import validate_create_payload, validate_update_payload


class TaskNotFoundError(Exception):
    pass


class TaskPersistenceError(Exception):
    pass


def list_tasks(db: Session) -> list[Task]:
    return list(db.scalars(select(Task).order_by(Task.id)).all())


def get_task(db: Session, task_id: int) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise TaskNotFoundError(f"Tarefa {task_id} não foi encontrada.")
    return task


def create_task(db: Session, payload: TaskCreate) -> Task:
    validate_create_payload(payload)
    task = Task(
        title=payload.title,
        description=payload.description,
        status=payload.status.value,
    )
    db.add(task)
    return _commit(db, task)


def update_task(db: Session, task_id: int, payload: TaskUpdate) -> Task:
    validate_update_payload(payload)
    task = get_task(db, task_id)
    values = payload.model_dump(exclude_unset=True)
    if "status" in values and values["status"] is not None:
        values["status"] = values["status"].value
    for field, value in values.items():
        setattr(task, field, value)
    return _commit(db, task)


def delete_task(db: Session, task_id: int) -> None:
    task = get_task(db, task_id)
    db.delete(task)
    try:
        db.commit()
    except SQLAlchemyError as error:
        db.rollback()
        raise TaskPersistenceError("Não foi possível persistir a alteração.") from error


def _commit(db: Session, task: Task) -> Task:
    try:
        db.commit()
        db.refresh(task)
        return task
    except SQLAlchemyError as error:
        db.rollback()
        raise TaskPersistenceError("Não foi possível persistir a alteração.") from error
