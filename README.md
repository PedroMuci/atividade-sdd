# Gerenciador de Tarefas

Aplicação web acadêmica simples para criar, listar, editar, alterar status e excluir tarefas.

## Tecnologias

- Python 3.11
- FastAPI e Uvicorn
- Jinja2
- SQLAlchemy com SQLite
- Pytest
- Docker e Docker Compose
- GitHub Actions e SonarQube Cloud

A aplicação não possui autenticação, conforme o escopo da atividade.

## Execução local

Pré-requisitos: Python 3.11, Docker e Docker Compose.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Acesse `http://localhost:8000`.

## Docker

```powershell
docker compose up --build
```

O SQLite fica em `/app/data/tasks.db`, dentro do volume nomeado `task_data`. O volume não deve ser removido durante atualizações, pois ele preserva as tarefas entre recriações do container.

## Testes

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Os testes cobrem listagem, estado vazio, criação, edição, validações, status, exclusão, erros e persistência.

Durante a validação manual, confirme que o status e os detalhes de cada tarefa são facilmente identificáveis na tela principal.

## CI/CD e SonarQube Cloud

Pushes para `main` executam a pipeline em `.github/workflows/pipeline.yml` na seguinte ordem:

1. Instalação das dependências e execução do Pytest.
2. Análise de qualidade e segurança no SonarQube Cloud.
3. Build da imagem Docker.
4. Deploy na EC2 somente se todas as etapas anteriores passarem.

Configure no GitHub Actions Secrets:

- `EC2_HOST`: endereço público ou hostname da EC2.
- `EC2_USER`: usuário SSH da EC2.
- `EC2_SSH_KEY`: chave privada SSH para o deploy.
- `SONAR_TOKEN`: token do SonarQube Cloud.
- `SONAR_ORGANIZATION`: organização do SonarQube Cloud.

Os valores dos secrets nunca devem ser commitados no repositório.

## AWS EC2

1. Provisione uma instância Linux adequada ao pequeno workload acadêmico.
2. Configure o Security Group para permitir SSH na porta 22 apenas conforme a necessidade administrativa e HTTP na porta 80; a aplicação pode ser publicada na porta 8000 conforme a configuração de rede adotada.
3. Instale Docker e Docker Compose Plugin na EC2.
4. Clone o repositório em `/opt/task-manager` e conceda ao usuário de deploy permissão para executar Docker.
5. Configure os secrets do GitHub Actions.
6. O deploy executa `git pull` e `docker compose up -d --build` sem remover o volume `task_data`.
7. Valide o endereço público da EC2 com um navegador ou requisição HTTP.

A aplicação deve ficar acessível pelo endereço público configurado para a instância.
