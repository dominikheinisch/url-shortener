FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.13.5 /uv /usr/local/bin/uv

RUN mkdir /opt/venv && chown 1000:1000 /opt/venv

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_CACHE_DIR=/tmp/uv-cache

WORKDIR /app
USER 1000:1000

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache
