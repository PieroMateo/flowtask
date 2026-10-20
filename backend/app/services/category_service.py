from sqlalchemy.orm import Session

from app.models import Category
from app.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, db: Session):
        self.categories = CategoryRepository(db)

    def list_categories(self) -> list[Category]:
        return self.categories.get_all()
