from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator

from app.core.enums import TaskStatus
from app.schemas.category import CategoryRead

# Quita espacios al inicio y al final y luego exige al menos 1 carácter: "   " es inválido.
TaskTitle = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=150)]


class TaskCreate(BaseModel):
    """Body de POST /tasks. No incluye id: lo genera la base de datos."""

    title: TaskTitle
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDIENTE
    due_date: date
    category_id: int


class TaskUpdate(BaseModel):
    """Body de PATCH /tasks/{id}. Todo es opcional: solo se cambian los campos enviados."""

    title: TaskTitle | None = None
    description: str | None = None
    status: TaskStatus | None = None
    due_date: date | None = None
    category_id: int | None = None

    @field_validator("title", "status", "due_date", "category_id")
    @classmethod
    def reject_explicit_null(cls, value):
        # Omitir un campo = "no lo cambies". Enviarlo como null = intentar borrarlo,
        # y estas columnas son obligatorias, así que se rechaza con 422.
        if value is None:
            raise ValueError("Este campo no puede ser nulo")
        return value


class TaskRead(BaseModel):
    """Respuesta de la API. Anida la categoría para mostrar su nombre sin otra petición."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: TaskStatus
    due_date: date
    category_id: int
    category: CategoryRead
