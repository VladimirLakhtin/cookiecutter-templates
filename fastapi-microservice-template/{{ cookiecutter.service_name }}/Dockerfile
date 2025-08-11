FROM python:3.11-slim-bookworm

ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY

ENV HTTP_PROXY=${HTTP_PROXY} \
    HTTPS_PROXY=${HTTPS_PROXY} \
    NO_PROXY=${NO_PROXY} \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH \
    PYTHONOPTIMIZE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_INSECURE_HOST="repo.corp.tander.ru"

# Для health-проверок
RUN apt-get update && apt-get install -y curl

RUN pip install --upgrade pip \
    && pip install uv==0.6.0

WORKDIR /{{ cookiecutter.service_name }}

RUN uv venv

COPY pyproject.toml auth_app .env ./

RUN uv sync --package {{ cookiecutter.service_name }} --active

CMD sh -c 'uvicorn {{ cookiecutter.app_name }}.main:app --host ${RUN_HOST} --port ${RUN_PORT} --reload'
