from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import init_db
from app.routes.tasks import router as tasks_router


BASE_DIR = Path(__file__).resolve().parent


def create_app() -> FastAPI:
    application = FastAPI(title="Gerenciador de Tarefas")
    application.state.templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
    application.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
    application.include_router(tasks_router)
    init_db()
    return application


app = create_app()
