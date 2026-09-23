def test_home_page_contains_task_form(client):
    response = client.get("/")

    assert response.status_code == 200
    assert 'name="title"' in response.text
    assert 'name="description"' in response.text
    assert 'name="status"' in response.text


def test_home_page_contains_task_lifecycle_controls(client):
    client.post("/tasks", json={"title": "Tarefa editável"})
    response = client.get("/")

    assert 'data-action="edit"' in response.text
    assert 'data-action="status"' in response.text
    assert 'data-action="delete"' in response.text
