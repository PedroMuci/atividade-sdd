def test_list_empty_state(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Nenhuma tarefa cadastrada" in response.text


def test_list_renders_all_task_fields(client):
    created = client.post("/tasks", json={"title": "Estudar FastAPI", "description": "Revisar rotas"})
    assert created.status_code == 201

    response = client.get("/")

    assert response.status_code == 200
    assert "Estudar FastAPI" in response.text
    assert "Revisar rotas" in response.text
    assert "Pendente" in response.text


def test_create_defaults_to_pending_and_update_task(client):
    created = client.post(
        "/tasks",
        json={"title": "Criar documentação", "description": "Escrever README"},
    )

    assert created.status_code == 201
    task = created.json()
    assert task["status"] == "Pendente"

    updated = client.put(
        f"/tasks/{task['id']}",
        json={"title": "Atualizar documentação", "description": "Revisar README"},
    )

    assert updated.status_code == 200
    assert updated.json()["title"] == "Atualizar documentação"


def test_rejects_invalid_task_payloads(client):
    assert client.post("/tasks", json={"title": "   "}).status_code == 422
    assert client.post("/tasks", json={"title": "x" * 201}).status_code == 422
    assert client.post("/tasks", json={"title": "x", "description": "x" * 2001}).status_code == 422
    assert client.post("/tasks", json={"title": "x", "status": "Invalido"}).status_code == 422


def test_change_status_and_delete_task(client):
    created = client.post("/tasks", json={"title": "Concluir atividade"})
    task_id = created.json()["id"]

    updated = client.put(f"/tasks/{task_id}", json={"status": "Concluída"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "Concluída"

    deleted = client.delete(f"/tasks/{task_id}")
    assert deleted.status_code == 200
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_unknown_task_does_not_change_other_records(client):
    created = client.post("/tasks", json={"title": "Manter registro"})
    task_id = created.json()["id"]

    assert client.put("/tasks/999", json={"title": "Inválida"}).status_code == 404
    assert client.delete("/tasks/999").status_code == 404
    assert client.get(f"/tasks/{task_id}").json()["title"] == "Manter registro"


def test_task_survives_application_session_restart(client):
    created = client.post("/tasks", json={"title": "Persistir tarefa"})
    task_id = created.json()["id"]

    client.app.state.templates = client.app.state.templates
    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Persistir tarefa"
