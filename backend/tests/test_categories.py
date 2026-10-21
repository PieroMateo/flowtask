from app.seed import seed_categories


def test_list_categories_returns_seeded_defaults(client):
    response = client.get("/categories")

    assert response.status_code == 200
    names = [category["name"] for category in response.json()]
    assert {"Trabajo", "Personal", "Urgente"} <= set(names)


def test_seed_is_idempotent(db_session):
    # la fixture ya corrio la semilla una vez, la segunda no deberia insertar nada
    assert seed_categories(db_session) == 0
