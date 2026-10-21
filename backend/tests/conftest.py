from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401  (registra los modelos antes de crear las tablas)
from app.database import Base, create_db_engine, get_db
from app.seed import seed_categories
from main import app

# los tests usan una bd en memoria que se borra al terminar, flowtask.db no se toca.
# StaticPool reusa la misma conexion, sin eso cada conexion nueva veria la bd vacia
test_engine = create_db_engine("sqlite://", poolclass=StaticPool)
TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False)


# antes de cada test crea las tablas y la semilla, despues borra todo
@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    seed_categories(session)
    yield session
    session.close()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    # cambia get_db por la sesion de prueba, los endpoints ni se enteran
    app.dependency_overrides[get_db] = lambda: db_session
    # sin "with" para que no corra el lifespan y no cree la bd real
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def task_payload() -> dict:
    return {"title": "Preparar informe", "due_date": "2026-10-30", "category_id": 1}
