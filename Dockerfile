FROM python:3.12.2-slim as build

ENV APP_ENV=dev \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.7.1 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  PYTHONPATH=/app

RUN --mount=type=cache,target=/var/cache/apt pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY ./backend /app/backend/
COPY ./pyproject.toml .

COPY ./scripts/start.sh /start.sh
RUN chmod +x /start.sh

COPY ./scripts/gunicorn_conf.py /gunicorn_conf.py

COPY ./scripts/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

RUN apt-get update && apt-get upgrade && apt-get install aapt -y && apt-get install unzip -y

FROM build AS development

RUN --mount=type=cache,target="$POETRY_CACHE_DIR" poetry install --no-interaction --no-ansi

FROM build AS production

RUN poetry install --no-interaction --no-ansi --no-dev
