from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator

from app.core.enums import TaskStatus
from app.schemas.category import CategoryRead

# primero quita los espacios de los lados y despues cuenta, asi "   " no pasa como titulo
TaskTitle = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=150)]


# body del POST /tasks, sin id porque ese lo pone la bd
class TaskCreate(BaseModel):
    title: TaskTitle
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDIENTE
    due_date: date
    category_id: int


# body del PATCH, todo opcional porque solo se cambia lo que se manda
class TaskUpdate(BaseModel):
    title: TaskTitle | None = None
    description: str | None = None
    status: TaskStatus | None = None
    due_date: date | None = None
    category_id: int | None = None

    # no mandar el campo = no tocarlo, pero mandarlo en null seria borrarlo
    # y esas columnas son obligatorias, sin esto terminaba en un error 500
    @field_validator("title", "status", "due_date", "category_id")
    @classmethod
    def reject_explicit_null(cls, value):
        if value is None:
            raise ValueError("Este campo no puede ser nulo")
        return value


# lo que devuelve la API. trae la categoria completa para que el
# frontend pueda mostrar el nombre sin pedirla aparte
class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: TaskStatus
    due_date: date
    category_id: int
    category: CategoryRead
