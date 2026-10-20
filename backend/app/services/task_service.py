from sqlalchemy.orm import Session

from app.core.enums import TaskStatus
from app.core.exceptions import InvalidReferenceError, NotFoundError
from app.models import Task
from app.repositories.category_repository import CategoryRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """Reglas de negocio de las tareas. No sabe nada de HTTP: comunica errores con excepciones."""

    def __init__(self, db: Session):
        self.tasks = TaskRepository(db)
        self.categories = CategoryRepository(db)

    def list_tasks(
        self,
        status: TaskStatus | None = None,
        category_id: int | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Task]:
        return self.tasks.list(status, category_id, limit, offset)

    def get_task(self, task_id: int) -> Task:
        task = self.tasks.get_by_id(task_id)
        if task is None:
            raise NotFoundError("Tarea no encontrada")
        return task

    def create_task(self, data: TaskCreate) -> Task:
        self._ensure_category_exists(data.category_id)
        return self.tasks.create(Task(**data.model_dump()))

    def update_task(self, task_id: int, data: TaskUpdate) -> Task:
        task = self.get_task(task_id)
        # exclude_unset: solo los campos que el cliente envió de verdad.
        changes = data.model_dump(exclude_unset=True)
        if "category_id" in changes:
            self._ensure_category_exists(changes["category_id"])
        return self.tasks.update(task, changes)

    def delete_task(self, task_id: int) -> None:
        self.tasks.delete(self.get_task(task_id))

    def _ensure_category_exists(self, category_id: int) -> None:
        # Pydantic valida la forma del dato; que la categoría exista solo lo sabe la BD.
        if self.categories.get_by_id(category_id) is None:
            raise InvalidReferenceError(f"La categoría con id {category_id} no existe")
