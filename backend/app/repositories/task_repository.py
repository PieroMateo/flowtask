from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.enums import TaskStatus
from app.models import Task


# aqui solo se consulta y se guarda, las reglas van en el service
class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        status: TaskStatus | None = None,
        category_id: int | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Task]:
        # selectinload trae todas las categorias en una sola consulta extra,
        # si no se haria una consulta por cada tarea
        stmt = select(Task).options(selectinload(Task.category))
        if status is not None:
            stmt = stmt.where(Task.status == status)
        if category_id is not None:
            stmt = stmt.where(Task.category_id == category_id)
        # el id desempata cuando dos tareas tienen la misma fecha, sino la paginacion se mueve
        stmt = stmt.order_by(Task.due_date, Task.id).limit(limit).offset(offset)
        return list(self.db.scalars(stmt))

    def get_by_id(self, task_id: int) -> Task | None:
        return self.db.get(Task, task_id, options=[selectinload(Task.category)])

    def create(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        # se recarga con la categoria para que la respuesta del POST ya traiga el nombre
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
