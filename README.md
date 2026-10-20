# FlowTask

Herramienta ligera de seguimiento de actividades para equipos pequeños: las tareas se clasifican por **categoría** (área o proyecto) y avanzan por los estados **Pendiente → En Progreso → Completada**.

![Tablero de FlowTask](docs/captura.jpg)

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Python 3.10+ · FastAPI · Pydantic v2 |
| ORM y base de datos | SQLAlchemy 2.x · SQLite |
| Frontend | Angular 22 · TypeScript · Tailwind CSS 4 |
| Pruebas | pytest · TestClient |
| Contenedores | Docker · Docker Compose · nginx |

## Estructura del repositorio

```
FlowTask/
├── backend/
│   ├── app/
│   │   ├── core/           # Configuración, enums y excepciones de dominio
│   │   ├── models/         # Modelos SQLAlchemy (tablas)
│   │   ├── schemas/        # Esquemas Pydantic (entrada y salida de la API)
│   │   ├── repositories/   # Consultas a la base de datos
│   │   ├── services/       # Reglas de negocio
│   │   ├── routers/        # Endpoints HTTP
│   │   ├── dependencies.py # Inyección de servicios con Depends
│   │   ├── database.py     # Engine, sesión y get_db
│   │   └── seed.py         # Lógica de la semilla
│   ├── tests/              # Pruebas con pytest
│   ├── main.py             # App FastAPI, CORS, routers y manejadores de error
│   └── seed.py             # Script ejecutable: python seed.py
├── frontend/
│   └── src/app/
│       ├── core/           # Modelos tipados, servicios HTTP e interceptor
│       ├── features/tasks/ # TaskBoard, TaskForm, FilterBar, TaskList, TaskCard
│       └── shared/         # Componente de notificaciones
└── docker-compose.yml
```

## Requisitos previos

- Python 3.10 o superior
- Node.js 22.22+ o 24.15+ (con npm), requerido por Angular 22
- Opcional: Docker Desktop

## Levantar el backend

```bash
cd backend

# 1. Crear y activar el entorno virtual
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux / macOS

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear las tablas y cargar las categorías base (Trabajo, Personal, Urgente)
python seed.py

# 4. Levantar el servidor
uvicorn main:app --reload
```

- API: http://localhost:8000
- Documentación interactiva (Swagger): http://localhost:8000/docs

> El paso 3 es opcional: al arrancar, la API también crea las tablas y carga la semilla. La semilla es idempotente, así que ejecutarla varias veces no duplica categorías.

## Levantar el frontend

En otra terminal, con el backend en ejecución:

```bash
cd frontend
npm install
npm start
```

Abrir http://localhost:4200

## Levantar todo con Docker

```bash
docker compose up --build
```

- Frontend: http://localhost:4200
- Backend: http://localhost:8000/docs

La base de datos SQLite se guarda en el volumen `flowtask-data`, por lo que los datos se conservan al reiniciar los contenedores. Para borrarlos: `docker compose down -v`.

## Ejecutar las pruebas

```bash
cd backend
pytest -v
```

Cada prueba usa una base de datos SQLite **en memoria** y desechable, por lo que nunca modifica `flowtask.db`.

## Endpoints

| Método | Ruta | Descripción | Respuestas |
|---|---|---|---|
| GET | `/categories` | Lista las categorías | 200 |
| GET | `/tasks` | Lista tareas. Filtros: `status`, `category_id`. Paginación: `limit` (1-100, por defecto 50) y `offset` | 200, 422 |
| GET | `/tasks/{id}` | Obtiene una tarea | 200, 404 |
| POST | `/tasks` | Crea una tarea | 201, 422 |
| PATCH | `/tasks/{id}` | Actualiza parcialmente una tarea (por ejemplo, solo `status`) | 200, 404, 422 |
| DELETE | `/tasks/{id}` | Elimina una tarea | 204, 404 |

Ejemplo de creación:

```json
POST /tasks
{
  "title": "Preparar informe mensual",
  "description": "Consolidar métricas del equipo",
  "status": "Pendiente",
  "due_date": "2026-10-30",
  "category_id": 1
}
```

Los errores siempre tienen el formato `{"detail": ...}`. Por ejemplo, `GET /tasks/99999` responde `404 {"detail": "Tarea no encontrada"}`.

## Decisiones de Diseño y Arquitectura

### Backend en capas

Cada petición recorre `router → service → repository → base de datos`, y cada capa tiene una única responsabilidad:

- **Routers**: solo traducen HTTP (rutas, parámetros, códigos de estado y `response_model`). Cada endpoint delega en una línea al servicio.
- **Services**: contienen las reglas de negocio, como verificar que la tarea o la categoría existan. No importan nada de FastAPI: comunican los errores lanzando excepciones de dominio.
- **Repositories**: encapsulan las consultas SQLAlchemy. Cambiar de motor de base de datos o de estrategia de consulta no afecta la lógica de negocio.

Esta separación permite probar y modificar cada parte por separado. Por ejemplo, las pruebas reemplazan la base de datos con `dependency_overrides` sin tocar ninguna capa.

### Modelos separados de los esquemas

Los modelos SQLAlchemy describen cómo se **guardan** los datos; los esquemas Pydantic describen lo que **entra y sale** de la API. Así, `TaskCreate` no acepta `id`, `TaskUpdate` tiene todos sus campos opcionales para el PATCH parcial, y `TaskRead` **anida la categoría** para que el frontend muestre su nombre sin hacer otra petición.

### Validación en dos niveles

1. **Pydantic** valida la forma de los datos y responde 422 automáticamente: título obligatorio y no vacío (se recortan los espacios), estado restringido al enum `TaskStatus`, y fecha ISO válida.
2. **El servicio** valida lo que requiere consultar la base de datos, como que `category_id` exista.

El estado se define una sola vez como `Enum` en Python (`app/core/enums.py`) y lo comparten el modelo, los esquemas y los filtros. En el frontend, `TASK_STATUSES` cumple el mismo papel.

### Manejo de errores

Los servicios lanzan `NotFoundError` o `InvalidReferenceError`, y un manejador global en `main.py` las traduce a respuestas JSON. Esto mantiene los servicios independientes de HTTP y garantiza que un recurso inexistente nunca produzca un 500. Un manejador adicional captura cualquier error inesperado, lo registra en el log y devuelve un mensaje genérico, sin exponer detalles internos.

**404 frente a 422:** se responde **404** cuando no existe el recurso de la URL (`/tasks/99999`) y **422** cuando el *body* hace referencia a una categoría inexistente, porque la ruta `/tasks` sí existe y el problema está en el contenido enviado.

En un PATCH, enviar explícitamente `null` en un campo obligatorio (por ejemplo, `{"title": null}`) se rechaza con 422, en lugar de llegar a la base de datos y provocar un error de integridad.

### Base de datos

- **SQLite**, por simplicidad: no requiere instalar un servidor. La URL se lee de la variable de entorno `DATABASE_URL`, así que migrar a PostgreSQL solo requiere cambiar esa variable e instalar el driver.
- Las llaves foráneas se activan con `PRAGMA foreign_keys=ON` en cada conexión, porque SQLite no las aplica por defecto.
- El listado usa `selectinload` para traer las categorías en una sola consulta adicional y evitar el problema N+1. El orden es por fecha límite y luego por `id`, para que la paginación sea estable.

### CORS estricto

Solo se permite el origen `http://localhost:4200` (configurable con `CORS_ORIGINS`), los métodos que la API usa (`GET`, `POST`, `PATCH`, `DELETE`) y el encabezado `Content-Type`.

### Frontend

- **Servicios**: `TaskService` y `CategoryService` son los únicos que usan `HttpClient`. Los componentes nunca declaran peticiones HTTP.
- **Interfaces tipadas** (`Task`, `Category`, `TaskCreate`, `TaskUpdate`) que reflejan los esquemas del backend.
- **Componentes contenedor y presentacionales**: `TaskBoard` guarda el estado y coordina los servicios; `FilterBar`, `TaskList` y `TaskCard` solo reciben datos con `input()` y emiten eventos con `output()`. `TaskForm` gestiona su propio envío para controlar su estado "guardando" y su reinicio.
- **Signals** para todo el estado, lo que permite que la aplicación funcione sin Zone.js y que la vista se actualice al instante tras crear, completar o eliminar, sin recargar la página.
- **Interceptor de errores**: centraliza los avisos al usuario. Distingue el backend caído (`status 0`), los errores de dominio (`detail` como texto) y los errores de validación (`detail` como lista).
- Al cambiar de filtro se cancela la petición anterior, para evitar que una respuesta tardía sobrescriba a la más reciente. Los botones de una tarea se desactivan mientras su petición está en curso, para evitar dobles envíos.

### Mejoras con más tiempo

- Migraciones con Alembic en lugar de `create_all`.
- Pruebas del frontend y pruebas end-to-end.
- Devolver el total de registros en el listado para mostrar una paginación completa en la interfaz.
- Edición completa de tareas desde la interfaz y gestión de categorías.
- Autenticación y tareas por usuario.
