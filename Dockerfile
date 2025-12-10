FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN uv pip install --system -e .

# Copy application code
COPY app/ ./app/

# Expose port (will be set by platform)
EXPOSE 8000

# Run the application (PORT is set by platform)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}


