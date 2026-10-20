from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401  (registra los modelos en Base.metadata)
from app.database import Base, create_db_engine, get_db
from app.seed import seed_categories
from main import app

# SQLite en memoria: cada test trabaja sobre una BD vacía y desechable, nunca sobre flowtask.db.
# StaticPool reutiliza una única conexión; sin él, cada conexión nueva vería una BD en blanco.
test_engine = create_db_engine("sqlite://", poolclass=StaticPool)
TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False)


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
    # Reemplaza la dependencia real: los endpoints reciben la sesión de prueba.
    app.dependency_overrides[get_db] = lambda: db_session
    # Sin "with": no se ejecuta el lifespan, así que no se toca la BD real.
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def task_payload() -> dict:
    return {"title": "Preparar informe", "due_date": "2026-10-30", "category_id": 1}
