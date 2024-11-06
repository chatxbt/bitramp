# Base stage with Python and Poetry installation
FROM python:3.12-slim AS python-base

# Set Poetry version and paths
ENV POETRY_VERSION=1.2.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Install Poetry in a dedicated virtual environment
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Application build stage
FROM python:3.11 AS example-app

# Copy Poetry environment from the base stage
COPY --from=python-base ${POETRY_VENV} ${POETRY_VENV}

# Set up the work directory
WORKDIR /app

# Copy the Poetry files and install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction --no-cache --without dev

# Copy the rest of the application code
COPY . /app

# Expose port for FastAPI
EXPOSE 8000

# Run the FastAPI application with Uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
