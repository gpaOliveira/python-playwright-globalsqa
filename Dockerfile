######## Stage 1: Build stage with all dependencies ########
FROM python:3.12.6-slim as builder
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates wget gnupg2 unzip fonts-liberation \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libx11-xcb1 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpangocairo-1.0-0 \
    libxss1 libasound2 libxshmfence1 libgtk-3-0 libatspi2.0-0 libxkbcommon0 \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy pyproject.toml and lock files
COPY pyproject.toml poetry.lock /app/

# Create Poetry environment and install dependencies
WORKDIR /app
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Install Playwright browsers (uses the CLI installed by the Python package)
RUN playwright install --with-deps || playwright install || true

######## Stage 2: Final build stage just to execute tests ########
FROM builder

# Copy application code
COPY . /app

# Set the default command
CMD ["poetry", "run", "pytest"]
