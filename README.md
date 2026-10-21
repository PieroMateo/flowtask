# FlowTask

Aplicación para llevar el seguimiento de tareas de un equipo pequeño. Cada tarea pertenece a una categoría (un área o proyecto) y pasa por tres estados: Pendiente, En Progreso y Completada.

![Tablero de FlowTask](docs/captura.jpg)

## Tecnologías

- Backend: Python 3.10+ con FastAPI y Pydantic v2
- Base de datos: SQLite, usando SQLAlchemy 2.x como ORM
- Frontend: Angular 22 con TypeScript y Tailwind CSS 4
- Pruebas: pytest con el TestClient de FastAPI
- Docker Compose para levantar todo junto (el frontend se sirve con nginx)

## Estructura

```
FlowTask/
├── backend/
│   ├── app/
│   │   ├── core/           # configuración, enums y excepciones propias
│   │   ├── models/         # modelos de SQLAlchemy (las tablas)
│   │   ├── schemas/        # esquemas de Pydantic (lo que entra y sale de la API)
│   │   ├── repositories/   # consultas a la base de datos
│   │   ├── services/       # reglas de negocio
│   │   ├── routers/        # endpoints
│   │   ├── dependencies.py # inyección de los services con Depends
│   │   ├── database.py     # engine, sesión y get_db
│   │   └── seed.py         # lógica de la semilla
│   ├── tests/
│   ├── main.py             # crea la app, CORS, routers y manejo de errores
│   └── seed.py             # script para correr la semilla: python seed.py
├── frontend/
│   └── src/app/
│       ├── core/           # modelos, servicios HTTP e interceptor de errores
│       ├── features/tasks/ # TaskBoard, TaskForm, FilterBar, TaskList, TaskCard
│       └── shared/         # avisos (notificaciones)
└── docker-compose.yml
```

## Requisitos

- Python 3.10 o superior
- Node.js 22.22+ o 24.15+ con npm (lo pide Angular 22)
- Docker Desktop, solo si se quiere usar la opción con Docker

## Cómo levantar el backend

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

La API queda en http://localhost:8000 y la documentación de Swagger en http://localhost:8000/docs.

El paso 3 se puede saltar, porque al arrancar la API también crea las tablas y carga la semilla. La semilla revisa qué categorías ya existen antes de insertar, así que correrla varias veces no duplica nada.

## Cómo levantar el frontend

En otra terminal, con el backend corriendo:

```bash
cd frontend
npm install
npm start
```

Luego abrir http://localhost:4200

## Con Docker

```bash
docker compose up --build
```

El frontend queda en http://localhost:4200 y el backend en http://localhost:8000/docs. La base de datos se guarda en el volumen `flowtask-data`, así que las tareas no se pierden al reiniciar los contenedores. Para borrarlas se usa `docker compose down -v`.

## Pruebas

```bash
cd backend
pytest -v
```

Cada prueba trabaja con una base de datos SQLite en memoria que se crea y se borra en el momento, por eso nunca modifican `flowtask.db`.

## Endpoints

| Método | Ruta | Qué hace | Respuestas |
|---|---|---|---|
| GET | `/categories` | Lista las categorías | 200 |
| GET | `/tasks` | Lista tareas. Filtros: `status`, `category_id`. Paginación: `limit` (1-100, por defecto 50) y `offset` | 200, 422 |
| GET | `/tasks/{id}` | Devuelve una tarea | 200, 404 |
| POST | `/tasks` | Crea una tarea | 201, 422 |
| PATCH | `/tasks/{id}` | Cambia solo los campos enviados, por ejemplo el `status` | 200, 404, 422 |
| DELETE | `/tasks/{id}` | Elimina una tarea | 204, 404 |

Ejemplo para crear una tarea:

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

Todos los errores tienen la forma `{"detail": ...}`. Por ejemplo, `GET /tasks/99999` responde `404 {"detail": "Tarea no encontrada"}`.

## Decisiones de Diseño y Arquitectura

### El backend en capas

Separé el backend para que cada petición pase por `router`, luego `service`, luego `repository` y recién ahí llegue a la base de datos.

Los routers solo se encargan de lo que tiene que ver con HTTP: la ruta, los parámetros, el código de respuesta y el `response_model`. Cada endpoint tiene una sola línea que llama al service.

En los services están las reglas, por ejemplo revisar que la tarea o la categoría existan. No importan nada de FastAPI. Cuando algo está mal lanzan una excepción propia y es `main.py` quien decide qué código HTTP devolver.

Los repositories tienen las consultas de SQLAlchemy. Si mañana se cambia de base de datos o la forma de consultar, la lógica de los services no se toca.

Con esta separación cada parte se puede probar por su lado. En los tests, por ejemplo, cambio la base de datos real por una en memoria con `dependency_overrides` sin modificar ninguna capa.

### Modelos y esquemas por separado

Los modelos de SQLAlchemy describen cómo se guardan los datos y los esquemas de Pydantic describen lo que recibe y devuelve la API. Por eso `TaskCreate` no acepta `id`, `TaskUpdate` tiene todos sus campos opcionales para el PATCH, y `TaskRead` trae la categoría completa adentro para que el frontend muestre el nombre sin tener que hacer otra petición.

### Validaciones

Las validaciones están en dos lugares. Pydantic revisa la forma de los datos y responde 422 solo: que el título no esté vacío (también le quita los espacios de los lados), que el estado sea uno de los tres permitidos y que la fecha sea válida. Lo que necesita consultar la base de datos, como que el `category_id` exista, lo revisa el service.

Los estados están definidos una sola vez en un `Enum` (`app/core/enums.py`) que usan el modelo, los esquemas y los filtros. En el frontend `TASK_STATUSES` cumple el mismo papel.

### Manejo de errores

Los services lanzan `NotFoundError` o `InvalidReferenceError` y un manejador en `main.py` las convierte en una respuesta JSON. Así los services no dependen de HTTP y un recurso que no existe nunca termina en un error 500. También agregué un manejador para cualquier error que no esté previsto, que lo deja registrado en la consola y al cliente le devuelve un mensaje simple sin detalles internos.

Elegí 404 cuando lo que no existe es el recurso de la URL (`/tasks/99999`) y 422 cuando el body apunta a una categoría que no existe. En ese segundo caso la ruta `/tasks` sí existe, el problema está en los datos que se mandaron.

En el PATCH, si se manda un campo obligatorio en `null` (por ejemplo `{"title": null}`) se rechaza con 422. Sin esa validación el valor llegaba a la base de datos y terminaba en un error de integridad.

### Base de datos

Usé SQLite porque no hace falta instalar ningún servidor. La conexión se lee de la variable de entorno `DATABASE_URL`, así que pasar a PostgreSQL sería cambiar esa variable e instalar el driver.

SQLite trae las llaves foráneas desactivadas, por eso las activo con `PRAGMA foreign_keys=ON` en cada conexión.

Al listar tareas uso `selectinload` para traer las categorías en una sola consulta extra y no una por cada tarea (el problema N+1). El orden es por fecha límite y después por `id`, así la paginación no cambia de orden entre una página y otra.

### CORS

Solo se permite el origen `http://localhost:4200` (se puede cambiar con `CORS_ORIGINS`), los métodos que la API usa (`GET`, `POST`, `PATCH`, `DELETE`) y el encabezado `Content-Type`.

### Frontend

`TaskService` y `CategoryService` son los únicos que usan `HttpClient`, ningún componente hace peticiones directamente. Las interfaces `Task`, `Category`, `TaskCreate` y `TaskUpdate` copian los esquemas del backend.

`TaskBoard` es el componente que guarda el estado y llama a los servicios. `FilterBar`, `TaskList` y `TaskCard` solo reciben datos con `input()` y avisan con `output()` cuando el usuario hace algo. `TaskForm` es la excepción: hace su propio POST porque necesita saber cuándo termina para limpiar el formulario y volver a habilitar el botón.

Todo el estado está en signals. Gracias a eso la app funciona sin Zone.js y la pantalla se actualiza en cuanto se crea, completa o elimina una tarea, sin recargar.

Los errores los maneja un interceptor que distingue tres casos: el backend no responde (`status 0`), un error nuestro (`detail` como texto) o un error de validación de Pydantic (`detail` como lista).

Cuando se cambia de filtro se cancela la petición anterior, porque si no una respuesta que llega tarde podía reemplazar a la más reciente. Además, mientras una tarea espera respuesta sus botones se desactivan para que un doble clic no mande la petición dos veces.

### Qué mejoraría con más tiempo

- Migraciones con Alembic en lugar de `create_all`
- Pruebas en el frontend y pruebas end-to-end
- Que el listado devuelva el total de registros para armar una paginación completa en la interfaz
- Poder editar una tarea completa desde la interfaz y administrar las categorías
- Autenticación y tareas por usuario
