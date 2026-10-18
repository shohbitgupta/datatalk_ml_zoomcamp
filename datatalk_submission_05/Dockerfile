# ---- build stage: install dependencies with uv ----
FROM python:3.11.15-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:0.10.12 /uv /bin/uv

WORKDIR /service
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    # use the image's Python 3.11, never download another one
    UV_PYTHON_DOWNLOADS=never

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project


# ---- runtime stage: only Python, the installed packages and the service ----
# same base image as the build stage, so the .venv's Python path still matches
FROM python:3.11.15-slim-bookworm

# pull in Debian security fixes released after the base image was built
RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /service
ENV PYTHONUNBUFFERED=1 \
    PATH="/service/.venv/bin:$PATH"

COPY --from=builder /service/.venv ./.venv
COPY app ./app
COPY models ./models

RUN useradd --create-home appuser
USER appuser

EXPOSE 9696

# slim images have no curl, so check /health with Python
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:9696/health', timeout=3)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9696"]
