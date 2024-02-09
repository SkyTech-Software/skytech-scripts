FROM python:3.12.1 as build

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

COPY ./backend /app/.
COPY ./pyproject.toml .

COPY ./scripts/start.sh /start.sh
RUN chmod +x /start.sh

COPY ./scripts/gunicorn_conf.py /gunicorn_conf.py

COPY ./scripts/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

ENV PYTHONPATH=/app

EXPOSE 80

FROM build as development

WORKDIR /backend/

RUN --mount=type=cache,target="$POETRY_CACHE_DIR" poetry install --no-interaction --no-ansi

FROM development AS production

WORKDIR /backend/

RUN poetry install --no-interaction --no-ansi --no-dev
