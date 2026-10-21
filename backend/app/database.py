from collections.abc import Generator

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


# todos los modelos heredan de aqui, asi sqlalchemy sabe que tablas tiene que crear
class Base(DeclarativeBase):
    pass


# esta en una funcion para que los tests puedan crear su propia bd en memoria con las mismas reglas
def create_db_engine(url: str, **kwargs) -> Engine:
    is_sqlite = url.startswith("sqlite")
    # sqlite por defecto no deja usar la conexion desde otro hilo, y fastapi usa varios
    connect_args = {"check_same_thread": False} if is_sqlite else {}
    engine = create_engine(url, connect_args=connect_args, **kwargs)

    if is_sqlite:
        # sqlite trae las llaves foraneas apagadas, hay que activarlas en cada conexion
        @event.listens_for(engine, "connect")
        def _enable_foreign_keys(dbapi_connection, _):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


engine = create_db_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


# cada peticion recibe su propia sesion y al terminar se cierra, aunque haya habido un error
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
