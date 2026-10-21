# se importan los dos modelos aqui para que queden registrados antes de crear las tablas
# y para que relationship("Task") encuentre la clase
from app.models.category import Category
from app.models.task import Task

__all__ = ["Category", "Task"]
