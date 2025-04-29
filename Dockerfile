FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install via uv:
COPY uv.lock .
RUN uv sync --locked

