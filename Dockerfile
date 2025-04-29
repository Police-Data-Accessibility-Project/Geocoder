FROM python:3.13-slim
# Create a safe cache directory
ENV UV_CACHE_DIR=/tmp/.uv-cache
RUN mkdir -p $UV_CACHE_DIR && chmod -R 777 $UV_CACHE_DIR

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install via uv:
RUN uv sync --locked

