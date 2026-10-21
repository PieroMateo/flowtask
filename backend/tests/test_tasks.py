import pytest


# caso 2: registro y validación

def test_create_task_returns_201_with_id_and_defaults(client, task_payload):
    response = client.post("/tasks", json=task_payload)

    assert response.status_code == 201
    body = response.json()
    assert isinstance(body["id"], int)
    assert body["status"] == "Pendiente"
    assert body["category"]["name"] == "Trabajo"


def test_create_task_trims_title(client, task_payload):
    response = client.post("/tasks", json={**task_payload, "title": "  Estudiar  "})

    assert response.status_code == 201
    assert response.json()["title"] == "Estudiar"


@pytest.mark.parametrize(
    "override",
    [
        {"title": ""},
        {"title": "   "},
        {"status": "Hecho"},
        {"due_date": "2026-02-30"},
        {"due_date": "mañana"},
    ],
    ids=["titulo-vacio", "titulo-espacios", "status-invalido", "fecha-inexistente", "fecha-texto"],
)
def test_create_task_with_invalid_data_returns_422(client, task_payload, override):
    response = client.post("/tasks", json={**task_payload, **override})

    assert response.status_code == 422


def test_create_task_with_missing_category_returns_422(client, task_payload):
    response = client.post("/tasks", json={**task_payload, "category_id": 999})

    assert response.status_code == 422
    assert response.json() == {"detail": "La categoría con id 999 no existe"}


# caso 3: listado y filtros

def test_list_tasks_filters_by_status(client, task_payload):
    client.post("/tasks", json=task_payload)
    client.post("/tasks", json={**task_payload, "title": "Otra", "status": "Completada"})

    response = client.get("/tasks", params={"status": "Completada"})

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["status"] == "Completada"


def test_list_tasks_supports_pagination(client, task_payload):
    for i in range(3):
        client.post("/tasks", json={**task_payload, "title": f"Tarea {i}"})

    response = client.get("/tasks", params={"limit": 2, "offset": 1})

    assert [task["title"] for task in response.json()] == ["Tarea 1", "Tarea 2"]


# caso 4: cambio de estado y borrado

def test_patch_marks_task_as_completed(client, task_payload):
    task_id = client.post("/tasks", json=task_payload).json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"status": "Completada"})

    assert response.status_code == 200
    assert response.json()["status"] == "Completada"
    assert response.json()["title"] == task_payload["title"]  # lo demas se queda igual


def test_delete_task_removes_it(client, task_payload):
    task_id = client.post("/tasks", json=task_payload).json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404


# caso 5: recursos inexistentes

def test_get_missing_task_returns_404_with_detail(client):
    response = client.get("/tasks/99999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Tarea no encontrada"}


@pytest.mark.parametrize("method", ["patch", "delete"])
def test_modify_missing_task_returns_404(client, method):
    kwargs = {"json": {"status": "Completada"}} if method == "patch" else {}

    response = getattr(client, method)("/tasks/99999", **kwargs)

    assert response.status_code == 404
