from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# solo para el editor, evita el import circular entre category.py y task.py
if TYPE_CHECKING:
    from app.models.task import Task


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str | None] = mapped_column(String(255))

    # una categoria tiene muchas tareas (lado "1" de la relacion)
    tasks: Mapped[list["Task"]] = relationship(back_populates="category")
