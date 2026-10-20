from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.enums import TaskStatus
from app.models import Task


class TaskRepository:
    """Acceso a datos de tareas. Solo consulta y guarda; no aplica reglas de negocio."""

    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        status: TaskStatus | None = None,
        category_id: int | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Task]:
        # selectinload trae las categorías de todas las tareas en 1 consulta extra
        # (en vez de 1 por tarea: el problema N+1).
        stmt = select(Task).options(selectinload(Task.category))
        if status is not None:
            stmt = stmt.where(Task.status == status)
        if category_id is not None:
            stmt = stmt.where(Task.category_id == category_id)
        stmt = stmt.order_by(Task.due_date, Task.id).limit(limit).offset(offset)
        return list(self.db.scalars(stmt))

    def get_by_id(self, task_id: int) -> Task | None:
        return self.db.get(Task, task_id, options=[selectinload(Task.category)])

    def create(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task, ["category"])
        return task

    def update(self, task: Task, changes: dict[str, Any]) -> Task:
        for field, value in changes.items():
            setattr(task, field, value)
        self.db.commit()
        self.db.refresh(task, ["category"])
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()
