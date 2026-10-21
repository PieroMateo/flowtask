from enum import Enum


# los 3 estados que acepta una tarea. si se agrega otro hay que ponerlo tambien
# en TASK_STATUSES del frontend (task.model.ts)
# hereda de str para que en el json salga como texto normal ("Pendiente")
class TaskStatus(str, Enum):
    PENDIENTE = "Pendiente"
    EN_PROGRESO = "En Progreso"
    COMPLETADA = "Completada"
