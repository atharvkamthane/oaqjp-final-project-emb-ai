# Python application container
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install only the system packages typically needed to build Python wheels.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies separately to improve Docker layer caching.
COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip \
    && if [ -s requirements.txt ]; then pip install -r requirements.txt; fi

# Copy application source after dependency installation.
COPY . .

# Do not run the application as root.
RUN useradd --create-home --shell /usr/sbin/nologin appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

# Override APP_MODULE if the application entry point differs.
ENV APP_MODULE=app:app
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-8080} ${APP_MODULE}"]
