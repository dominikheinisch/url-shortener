RUN = docker compose run --rm app

.PHONY: build up down shell

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
