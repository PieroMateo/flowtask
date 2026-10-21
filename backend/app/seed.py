from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.repositories.category_repository import CategoryRepository

DEFAULT_CATEGORIES = [
    ("Trabajo", "Actividades laborales y proyectos del equipo"),
    ("Personal", "Pendientes de la vida personal"),
    ("Urgente", "Tareas que requieren atención inmediata"),
]


# solo inserta las que faltan, asi se puede correr varias veces sin duplicar nada.
# devuelve cuantas inserto
def seed_categories(db: Session) -> int:
    repo = CategoryRepository(db)
    inserted = 0
    for name, description in DEFAULT_CATEGORIES:
        if repo.get_by_name(name) is None:
            repo.create(name, description)
            inserted += 1
    return inserted


# crea las tablas que no existan y luego mete las categorias base
def init_db() -> int:
    import app.models  # noqa: F401  (hace falta para que create_all conozca las tablas)

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        return seed_categories(db)
