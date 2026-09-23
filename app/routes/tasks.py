from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service


router = APIRouter()


def _service_error(error: Exception) -> HTTPException:
    if isinstance(error, task_service.TaskNotFoundError):
        return HTTPException(status_code=404, detail=str(error))
    if isinstance(error, ValueError):
        return HTTPException(status_code=422, detail=str(error))
    if isinstance(error, task_service.TaskPersistenceError):
        return HTTPException(status_code=500, detail=str(error))
    return HTTPException(status_code=500, detail="Ocorreu um erro inesperado.")


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="tasks.html",
        context={"tasks": task_service.list_tasks(db)},
    )


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    try:
        return task_service.get_task(db, task_id)
    except Exception as error:
        raise _service_error(error) from error


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    try:
        return task_service.create_task(db, payload)
    except Exception as error:
        raise _service_error(error) from error


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    try:
        return task_service.update_task(db, task_id, payload)
    except Exception as error:
        raise _service_error(error) from error


@router.delete("/tasks/{task_id}")
def remove_task(task_id: int, db: Session = Depends(get_db)):
    try:
        task_service.delete_task(db, task_id)
        return {"message": "Tarefa excluída com sucesso."}
    except Exception as error:
        raise _service_error(error) from error
