from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.routers import categories, tasks
from app.seed import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Se ejecuta una vez al arrancar el servidor: crea tablas y carga la semilla.
    init_db()
    yield


app = FastAPI(
    title="FlowTask API",
    description="Seguimiento de tareas por categoría.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS estricto: solo los orígenes configurados y solo los métodos que la API usa.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type"],
)

register_exception_handlers(app)

app.include_router(categories.router)
app.include_router(tasks.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok"}
