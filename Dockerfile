# syntax=docker/dockerfile:1.4
FROM python:3.13-slim

# Get UID from build args (default to 1000 if not provided)
ARG JENKINS_UID=1000

# Create a user with the provided UID
RUN useradd -u $JENKINS_UID -ms /bin/bash jenkinsuser

# Set environment variable for uv cache
ENV UV_CACHE_DIR=/home/jenkinsuser/.uv-cache

# Create cache directory and make sure it's owned by the new user
RUN mkdir -p $UV_CACHE_DIR && chown -R jenkinsuser:jenkinsuser $UV_CACHE_DIR

# Install uv from astral's image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory and ensure it’s owned
WORKDIR /app
COPY . .
RUN chown -R jenkinsuser:jenkinsuser /app

# Switch to the created user
USER jenkinsuser

# Install dependencies (will use $UV_CACHE_DIR)
RUN --mount=type=cache,target=${UV_CACHE_DIR} \
    uv sync --locked --frozen