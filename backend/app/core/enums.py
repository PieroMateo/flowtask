from enum import Enum


class TaskStatus(str, Enum):
    """Estados permitidos de una tarea.

    Es la única fuente de verdad: la usan el modelo (BD), los esquemas (validación)
    y los filtros del router. Hereda de str para que se serialice como texto en JSON.
    """

    PENDIENTE = "Pendiente"
    EN_PROGRESO = "En Progreso"
    COMPLETADA = "Completada"
