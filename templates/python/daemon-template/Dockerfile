FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir .

COPY src/ src/
COPY config.example.toml config.toml

ENV DAEMON_CONFIG=/app/config.toml
ENV DAEMON_HEALTH_FILE=/app/var/health.json
ENV DAEMON_LOG_JSON=true

RUN mkdir -p /app/var

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD python -c "import json, sys; d=json.load(open('/app/var/health.json')); sys.exit(0 if d['status']=='ok' else 1)"

CMD ["python", "-m", "src.main"]
