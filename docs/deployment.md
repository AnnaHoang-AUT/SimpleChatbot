# Deployment Guide

## Local Development

```bash
scripts\run_web.bat   # Windows
./scripts/run_web.sh  # macOS/Linux
```

## Production with Gunicorn

```bash
pip install gunicorn
gunicorn "simplechatbot.web.app:app" --bind 0.0.0.0:8000 --workers 4 --timeout 120
```

## Docker

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -e . gunicorn
EXPOSE 8000
CMD ["gunicorn", "simplechatbot.web.app:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| AWS_DEFAULT_REGION | us-east-1 | AWS region |
| MAX_TOKENS | 4096 | Max response tokens |
| FLASK_HOST | 127.0.0.1 | Flask bind address |
| FLASK_PORT | 5000 | Flask port |
| FLASK_DEBUG | false | Debug mode |
