FROM --platform=$BUILDPLATFORM node:22-alpine AS browser-builder
WORKDIR /app/browser
COPY browser/package.json browser/package-lock.json ./
RUN npm ci
COPY browser/ ./
RUN npm run build

FROM python:3.12-slim AS builder
ENV UV_CACHE_DIR=/tmp/uv-cache UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && uv sync --frozen --no-dev --no-install-project
COPY . .
RUN uv sync --frozen --no-dev

FROM python:3.12-slim AS runtime
ARG MODWIRE_MCP_VERSION=0.0.0+dev
ENV PATH="/app/.venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 VIRTUAL_ENV="/app/.venv" PYTHONPATH="/app/src:/app" MODWIRE_MCP_VERSION="$MODWIRE_MCP_VERSION"
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends dumb-init && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=browser-builder /app/browser/dist /app/browser/dist
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 CMD python -c "from urllib.request import urlopen; urlopen('http://127.0.0.1:8000/health/', timeout=4).read()"
ENTRYPOINT ["dumb-init", "--"]
CMD ["gunicorn", "modwire.core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-"]
