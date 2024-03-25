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
RUN --mount=type=cache,target=/var/cache/apt apt-get update && apt-get upgrade && apt-get install aapt -y && apt-get install unzip -y && apt-get install nodejs npm -y

WORKDIR /app

# Install node dependencies
COPY ./wrappers/google-play-scraper-wrapper/package.json /app/wrappers/google-play-scraper-wrapper/package.json
WORKDIR /app/wrappers/google-play-scraper-wrapper
RUN npm i
WORKDIR /app

# Resolve dependencies
COPY ./pyproject.toml /app/pyproject.toml
RUN poetry install --no-interaction --no-ansi

# Copy project files
COPY ./backend /app/backend/
COPY ./wrappers /app/wrappers/

# Setup
COPY ./scripts/start.sh /start.sh
RUN chmod +x /start.sh

COPY ./scripts/gunicorn_conf.py /gunicorn_conf.py

COPY ./scripts/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

FROM build AS development

COPY ./scripts/celery/start-celery-worker /app/start-celery-worker.sh
RUN chmod +x /app/start-celery-worker.sh

FROM build AS production

COPY ./scripts/celery/start-celery-worker-prod /app/start-celery-worker-prod.sh
RUN chmod +x /app/start-celery-worker-prod.sh
