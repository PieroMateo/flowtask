from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.routers import categories, tasks
from app.seed import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    # se ejecuta una vez al arrancar el servidor: crea tablas y carga la semilla.
    init_db()
    yield

# este es el objeto principal de la aplicacion fastapi
app = FastAPI(
    title="FlowTask API",
    description="Seguimiento de tareas por categoría.",
    version="1.0.0",
    lifespan=lifespan,
)

# solo dejamos entrar al frontend (localhost:4200) y con los metodos que de verdad usamos
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type"],
)
#manejo de errores, se envia todo a app
register_exception_handlers(app)
# incluyen los routers para el funcionamiento de la API que se conecte, en este caso task y categories
app.include_router(categories.router)
app.include_router(tasks.router)

# este pequeño fragmento es para que el servidor tenga un endpoint de prueba
@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok"}
