from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Category


class CategoryRepository:
    """Acceso a datos de categorías. Solo consulta y guarda; no aplica reglas de negocio."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Category]:
        return list(self.db.scalars(select(Category).order_by(Category.id)))

    def get_by_id(self, category_id: int) -> Category | None:
        return self.db.get(Category, category_id)

    def get_by_name(self, name: str) -> Category | None:
        return self.db.scalar(select(Category).where(Category.name == name))

    def create(self, name: str, description: str | None = None) -> Category:
        category = Category(name=name, description=description)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
