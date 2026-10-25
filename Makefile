RUN = docker compose run --rm app

.PHONY: build up down shell lock migrate test lint fmt

build:
	docker compose build
up:
	docker compose up --build
down:
	docker compose down
shell:
	$(RUN) bash
lock:
	docker run --rm -u 1000:1000 -e UV_CACHE_DIR=/tmp/uv-cache -v $(CURDIR):/app -w /app \
		ghcr.io/astral-sh/uv:0.13.5-python3.13-trixie-slim uv lock
migrate:
	$(RUN) uv run python manage.py migrate

test:
	$(RUN) uv run pytest

lint:
	docker compose run --rm --no-deps app sh -c "uv run ruff check . && uv run ruff format --check . && uv run mypy ."

fmt:
	$(RUN) sh -c "uv run ruff check --fix . && uv run ruff format ."
