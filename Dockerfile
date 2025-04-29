FROM python:3.13-slim

ARG JENKINS_UID=1000
RUN useradd -u $JENKINS_UID -ms /bin/bash jenkins
USER jenkins

# Add a non-root user
RUN useradd -ms /bin/bash appuser

# Create cache directory and assign ownership
ENV UV_CACHE_DIR=/home/appuser/.uv-cache
RUN mkdir -p $UV_CACHE_DIR && chown -R appuser:appuser $UV_CACHE_DIR

# Install uv from image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory and ensure it’s owned
WORKDIR /app
COPY . .
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Install dependencies (will use $UV_CACHE_DIR)
RUN uv sync --locked
