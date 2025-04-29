FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Set a writable directory for UV's cache
ENV UV_CACHE_DIR=/tmp/.uv-cache

# Install via uv:
RUN uv sync --locked

