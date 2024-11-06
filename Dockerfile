# Use a Python 3.12 slim image as base
FROM python:3.12-slim AS python-base

# Install system dependencies for building packages
RUN apt-get update && \
    apt-get install -y gcc python3-dev libpq-dev build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry globally
ENV POETRY_HOME="/opt/poetry"
RUN pip install "poetry==1.8.3"

# Set paths for Poetry
ENV POETRY_VENV="/opt/poetry-venv"
ENV PATH="${POETRY_HOME}/bin:${PATH}"

# Create a dedicated virtual environment for the app
FROM python-base AS app-stage

WORKDIR /app

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies with Poetry
RUN poetry config virtualenvs.in-project true && \
    poetry install --no-interaction --no-cache --without dev

# Copy application code
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
