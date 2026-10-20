from collections.abc import Generator

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    """Clase padre de todos los modelos. Guarda el registro de tablas (Base.metadata)."""


def create_db_engine(url: str, **kwargs) -> Engine:
    """Crea el engine (la "fábrica de conexiones") hacia la base de datos."""
    is_sqlite = url.startswith("sqlite")
    # SQLite por defecto solo deja usar una conexión en el hilo que la creó;
    # FastAPI atiende peticiones en varios hilos, por eso se desactiva el chequeo.
    connect_args = {"check_same_thread": False} if is_sqlite else {}
    engine = create_engine(url, connect_args=connect_args, **kwargs)

    if is_sqlite:
        # SQLite no aplica las llaves foráneas a menos que se active en cada conexión.
        @event.listens_for(engine, "connect")
        def _enable_foreign_keys(dbapi_connection, _):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


engine = create_db_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    """Dependencia de FastAPI: una sesión nueva por petición, cerrada siempre al final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
