#!/usr/bin/env bash
# Dev helper: start services and run alembic migrations
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"

echo "Bringing up docker-compose services (db + redis)..."
docker-compose -f "$ROOT_DIR/docker-compose.yml" up -d db cache

echo "Waiting for Postgres to be ready..."
# Use docker-compose exec to run pg_isready inside the 'db' container (works on macOS)
until docker-compose -f "$ROOT_DIR/docker-compose.yml" exec -T db pg_isready -U postgres >/dev/null 2>&1; do
  echo -n '.'; sleep 1
done

echo "Running Alembic migrations..."
cd "$BACKEND_DIR"
if [ -z "${VECTOR_DB_URL:-}" ]; then
  echo "VECTOR_DB_URL not set — using default from settings. Ensure .env is configured if needed."
fi
alembic upgrade head

echo "Starting backend and frontend (in detached mode)..."
docker-compose -f "$ROOT_DIR/docker-compose.yml" up -d backend frontend

echo "Note: make the script executable if needed: chmod +x $0"

echo "Services started. Backend logs: docker-compose logs -f backend"
