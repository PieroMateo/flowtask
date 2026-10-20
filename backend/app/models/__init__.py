# Importar todos los modelos aquí asegura que queden registrados en Base.metadata
# antes de crear las tablas, y que las relaciones por nombre ("Task") se resuelvan.
from app.models.category import Category
from app.models.task import Task

__all__ = ["Category", "Task"]
