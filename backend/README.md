Backend (FastAPI)

Quick start (macOS / zsh)

1. Create and activate a virtualenv (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]
```

2. Copy the example env file and set environment variables you need:

```bash
cp ../.env.example .env
# Edit .env to set VECTOR_DB_URL, REDIS_URL, IMPACT_API_KEY, etc.
```

3. Using Docker Compose (recommended for Postgres+Redis):

```bash
# from repository root
docker-compose up -d db cache
# wait a few seconds for services to start
./scripts/dev_up.sh
```

4. Run alembic migrations (inside backend):

```bash
cd backend
alembic upgrade head
```

5. Start the backend (development):

```bash
# Either run via uvicorn directly
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Or use the helper (dev_up.sh starts backend + frontend when available)
```

Run tests

```bash
cd backend
pytest -q
```

Notes

- If you want real marketplace data, set `IMPACT_API_KEY`, `CJ_API_KEY`, or `RAKUTEN_API_KEY` in your `.env` or environment. When these are not provided, adapters fall back to a local sample catalog so search returns diverse demo items.

Git: commit & push changes

```bash
git add -A
git commit -m "Describe your change"
git push origin main
```
