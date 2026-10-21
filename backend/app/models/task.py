from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import TaskStatus
from app.database import Base

if TYPE_CHECKING:
    from app.models.category import Category


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(
        # values_callable hace que se guarde "En Progreso" y no el nombre EN_PROGRESO
        Enum(TaskStatus, values_callable=lambda e: [m.value for m in e], native_enum=False),
        default=TaskStatus.PENDIENTE,
    )
    due_date: Mapped[date]
    # la llave foranea va en la tarea porque es el lado "muchos"
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), index=True)

    category: Mapped["Category"] = relationship(back_populates="tasks")
