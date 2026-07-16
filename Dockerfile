FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (optional minimal)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
	ca-certificates \
	&& rm -rf /var/lib/apt/lists/*

# Install python deps first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app sources
COPY app.py validation.py ./
COPY templates ./templates

ENV PORT=8080

EXPOSE 8080

# Secrets (API keys) should be provided at runtime via --env/--env-file
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 2 --threads 4 --worker-tmp-dir /dev/shm app:app"]
