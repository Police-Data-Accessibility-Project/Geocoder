FROM python:3.13-slim

# Install system dependencies and uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install via uv:
COPY uv.lock .
RUN uv pip sync

# Set the entrypoint or command
CMD ["python", "main.py"]