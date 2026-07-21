FROM python:3.13-slim-bookworm

WORKDIR /app

RUN pip install -U pip && \
    pip install "poetry==2.3.2" && \
    poetry config virtualenvs.create false && \
    poetry config installer.max-workers 10

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi --no-root --no-cache --only main && \
    rm -rdf ~/.cache