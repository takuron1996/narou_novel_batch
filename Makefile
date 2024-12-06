SHELL = /bin/bash
SOURCE_DIR = application
CONTAINER_NAME = batch
DOCKER = docker exec $(CONTAINER_NAME)
POETRY_RUN = $(DOCKER) poetry run
LINT_RESULT = lint_result.txt

test:
	$(POETRY_RUN) pytest -n auto -ra -p no:cacheprovider --strict-config --strict-markers -vv --diff-symbols --cov --cov-report=html --gherkin-terminal-reporter

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
