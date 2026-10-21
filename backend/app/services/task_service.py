from sqlalchemy.orm import Session

from app.core.enums import TaskStatus
from app.core.exceptions import InvalidReferenceError, NotFoundError
from app.models import Task
from app.repositories.category_repository import CategoryRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


# aqui van las reglas de las tareas. si algo esta mal se lanza una excepcion
# y exceptions.py la convierte en 404 o 422
class TaskService:
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

    # la usan tambien update y delete, asi el 404 se escribe una sola vez
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
        # exclude_unset deja solo los campos que el cliente mando
        changes = data.model_dump(exclude_unset=True)
        if "category_id" in changes:
            self._ensure_category_exists(changes["category_id"])
        return self.tasks.update(task, changes)

    def delete_task(self, task_id: int) -> None:
        self.tasks.delete(self.get_task(task_id))

    # pydantic no puede saber si la categoria existe, eso hay que preguntarlo a la bd
    def _ensure_category_exists(self, category_id: int) -> None:
        if self.categories.get_by_id(category_id) is None:
            raise InvalidReferenceError(f"La categoría con id {category_id} no existe")
