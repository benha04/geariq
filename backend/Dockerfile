FROM python:3.11-slim
WORKDIR /app
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev gcc \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# Install runtime dependencies (kept explicit to avoid complex pyproject parsing in Dockerfile)
RUN pip install --no-cache-dir \
    fastapi~=0.115 \
    "uvicorn[standard]"~=0.30 \
    pydantic~=2.8 \
    SQLAlchemy~=2.0 \
    "psycopg[binary]"~=3.2 \
    alembic~=1.13 \
    redis~=5.0 \
    httpx~=0.27 \
    tenacity~=9.0 \
    pgvector~=0.3.5

COPY . /app
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
