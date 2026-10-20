from pydantic import BaseModel, ConfigDict


class CategoryRead(BaseModel):
    """Lo que la API devuelve de una categoría."""

    # Permite construir el esquema directamente desde un objeto SQLAlchemy (category.name, ...).
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
