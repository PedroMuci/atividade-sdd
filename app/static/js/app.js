const form = document.querySelector('#task-form');

if (form) {
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const feedback = document.querySelector('#form-feedback');
    const data = Object.fromEntries(new FormData(form).entries());
    if (!data.description) delete data.description;

    const response = await fetch('/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      window.location.reload();
      return;
    }

    const body = await response.json();
    feedback.textContent = body.detail || 'Não foi possível salvar a tarefa.';
  });
}

async function updateTask(taskId, payload) {
  const response = await fetch(`/tasks/${taskId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const body = await response.json();
    throw new Error(body.detail || 'Não foi possível atualizar a tarefa.');
  }
  window.location.reload();
}

document.querySelectorAll('[data-action="status"]').forEach((control) => {
  control.addEventListener('change', async () => {
    try {
      await updateTask(control.dataset.taskId, { status: control.value });
    } catch (error) {
      window.alert(error.message);
    }
  });
});

document.querySelectorAll('[data-action="edit"]').forEach((control) => {
  control.addEventListener('click', async () => {
    const title = window.prompt('Título', control.dataset.title);
    if (title === null) return;
    const description = window.prompt('Descrição', control.dataset.description);
    if (description === null) return;
    try {
      await updateTask(control.dataset.taskId, { title, description });
    } catch (error) {
      window.alert(error.message);
    }
  });
});

document.querySelectorAll('[data-action="delete"]').forEach((control) => {
  control.addEventListener('click', async () => {
    if (!window.confirm('Excluir esta tarefa?')) return;
    const response = await fetch(`/tasks/${control.dataset.taskId}`, { method: 'DELETE' });
    if (response.ok) window.location.reload();
  });
});
