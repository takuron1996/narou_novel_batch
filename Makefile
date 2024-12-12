SHELL = /bin/bash
SOURCE_DIR = application
CONTAINER_NAME = app
DOCKER = docker exec $(CONTAINER_NAME)
POETRY_RUN = $(DOCKER) poetry run
LINT_RESULT = lint_result.txt

run:
	$(POETRY_RUN) python main.py

init_db:
	$(POETRY_RUN) python command.py init_db

test:
	$(POETRY_RUN) pytest -n auto -ra -p no:cacheprovider --strict-config --strict-markers -vv --diff-symbols --cov --cov-report=html

up:
	docker compose up -d

build:
	docker compose build

down:
	docker compose down

check:
	@$(POETRY_RUN) black .
	-@$(POETRY_RUN) ruff check --fix --show-files

install:
	$(DOCKER) poetry install

update:
	$(DOCKER) poetry update

migration:
	$(POETRY_RUN) alembic revision --autogenerate

upgrade:
	$(POETRY_RUN) alembic upgrade head
