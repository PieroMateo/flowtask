from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.repositories.category_repository import CategoryRepository

DEFAULT_CATEGORIES = [
    ("Trabajo", "Actividades laborales y proyectos del equipo"),
    ("Personal", "Pendientes de la vida personal"),
    ("Urgente", "Tareas que requieren atención inmediata"),
]


def seed_categories(db: Session) -> int:
    """Inserta las categorías base que falten. Es idempotente: ejecutarla N veces no duplica.

    Devuelve cuántas categorías nuevas se insertaron.
    """
    repo = CategoryRepository(db)
    inserted = 0
    for name, description in DEFAULT_CATEGORIES:
        if repo.get_by_name(name) is None:
            repo.create(name, description)
            inserted += 1
    return inserted


def init_db() -> int:
    """Crea las tablas que no existan y carga la semilla."""
    import app.models  # noqa: F401  (registra los modelos en Base.metadata)

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        return seed_categories(db)
