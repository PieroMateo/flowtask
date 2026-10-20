from fastapi import APIRouter, Depends, Query, status

from app.core.enums import TaskStatus
from app.dependencies import get_task_service
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Respuestas de error documentadas en /docs (además del 422 que FastAPI agrega solo).
NOT_FOUND = {404: {"description": "Tarea no encontrada"}}


@router.get("", response_model=list[TaskRead])
def list_tasks(
    # alias: en la URL se llama ?status=..., pero en Python evitamos chocar con fastapi.status.
    task_status: TaskStatus | None = Query(None, alias="status"),
    category_id: int | None = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: TaskService = Depends(get_task_service),
):
    return service.list_tasks(task_status, category_id, limit, offset)


@router.get("/{task_id}", response_model=TaskRead, responses=NOT_FOUND)
def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    return service.get_task(task_id)


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, service: TaskService = Depends(get_task_service)):
    return service.create_task(data)


@router.patch("/{task_id}", response_model=TaskRead, responses=NOT_FOUND)
def update_task(task_id: int, data: TaskUpdate, service: TaskService = Depends(get_task_service)):
    return service.update_task(task_id, data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, responses=NOT_FOUND)
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    service.delete_task(task_id)
