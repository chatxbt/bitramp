FROM python:3.12-slim AS python-base

# https://python-poetry.org/docs#ci-recommendations
ENV POETRY_VERSION=1.2.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

# Tell Poetry where to place its cache and virtual environment
ENV POETRY_CACHE_DIR=/opt/.cache

# Create stage for Poetry installation
FROM python-base AS poetry-base

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Create a new stage from the base python image
FROM python-base AS example-app

RUN pip install --upgrade pip
RUN pip install pipx

RUN pipx ensurepath

RUN pipx install poetry "fastapi[standard]"

RUN curl -sfS https://dotenvx.sh/install.sh | sh

# Copy Poetry to app image
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

# Copy Dependencies
# COPY poetry.lock pyproject.toml ./
COPY poetry.lock pyproject.toml ./

# [OPTIONAL] Validate the project is properly configured
# RUN pipx run poetry check

# Install Dependencies
RUN pipx run poetry install --no-interaction --no-cache --without dev

# Copy Application
COPY . /app

# Run Application
EXPOSE 8000

CMD ["dotenvx", "run", "--", "pipx", "run", "poetry", "run", "fastapi", "run", "api/main.py", "--port", "8000"]
# CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]