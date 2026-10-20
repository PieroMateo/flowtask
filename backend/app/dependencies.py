from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.category_service import CategoryService
from app.services.task_service import TaskService


def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(db)


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(db)
