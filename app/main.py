from fastapi import FastAPI
from app.api.routes import router
import uvicorn
from app.core.events import startup_handler, shutdown_handler

def create_app() -> FastAPI:
    app = FastAPI(title="Application State")
    app.add_event_handler("startup", startup_handler(app))
    app.add_event_handler("shutdown", shutdown_handler(app))
    app.include_router(router)

    return app

app = create_app()
