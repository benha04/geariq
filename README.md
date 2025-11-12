# GearIQ

GearIQ — Monorepo (v0.1)

Tagline: Find the best product for you — not just the cheapest item.

# GearIQ

GearIQ — Monorepo (v0.1)

Tagline: Find the best product for you — not just the cheapest item.

This repository is a starter scaffold with a FastAPI backend, Next.js + Tailwind frontend, Docker Compose (Postgres + pgvector + Redis), CI workflows, and contribution templates.

## Prerequisites

- Git & gh CLI (optional)
- Docker & Docker Compose (optional)
- Node.js 20+
- Python 3.11+

## Quick start — create the GitHub repo

```bash
# create a local folder and initialize
mkdir geariq && cd geariq
git init
git checkout -b main  # optional
echo "# GearIQ" > README.md
git add . && git commit -m "chore: init repo"

# Create GitHub repo (public). Replace ORG if needed.
gh repo create geariq --public --source=. --push

# After adding scaffold files locally:
git add .
git commit -m "feat: v0.1 scaffold (backend+frontend+devops)"
git push -u origin main
```

## Repository structure

Top-level layout (abridged):

```
geariq/
├─ .github/ … CI, issue/pr templates
├─ backend/ … FastAPI app, DB models, alembic
├─ frontend/ … Next.js + Tailwind app
├─ docker-compose.yml
├─ .env.example
└─ README.md
```

See the repo for full file tree and detailed module locations.

## Local development

There are two common ways to run locally: with Docker Compose or running services directly.

### Option A — Docker Compose (recommended for a full stack)

```bash
cp .env.example .env
docker compose up --build

# frontend: http://localhost:3000
# backend:  http://localhost:8000
```

### Option B — Run services locally (macOS / manual)

Backend (FastAPI)

```bash
# ensure Python 3.11 is available
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
cd backend
python -m pip install -e ".[dev]"

# start the backend (background). Logs -> /tmp/uvicorn.log
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload > /tmp/uvicorn.log 2>&1 & echo $! > /tmp/uvicorn.pid
curl http://127.0.0.1:8000/health
```

Frontend (Next.js)

```bash
cd frontend
npm install
# start dev server. Logs -> /tmp/next-dev.log
npm run dev > /tmp/next-dev.log 2>&1 & echo $! > /tmp/next-dev.pid
curl -I http://127.0.0.1:3000
tail -n 200 /tmp/next-dev.log
```

Notes:

- The codebase uses modern Python syntax that requires Python 3.11+.
- We replaced `frontend/next.config.ts` with `frontend/next.config.mjs` (JS ESM) so the Next dev server can read the config at runtime. If you prefer a TypeScript config, use a prebuild step that compiles the config.

## Docker Compose (excerpt)

The provided `docker-compose.yml` wires up Postgres (pgvector), Redis, backend, and frontend. It maps:

- Postgres: 5432
- Redis: 6379
- Backend: 8000
- Frontend: 3000

## CI (GitHub Actions)

There is a CI workflow under `.github/workflows/ci.yml` that runs backend linting/tests and frontend typecheck/lint/tests.

## Development notes & roadmap

- Matching: `backend/app/services/matching.py` currently uses a simple weighted score. Future work: embeddings and learned weights.
- Product model, migrations, and basic API routes exist under `backend/app/` (see `app.main`, `api/routes/*`).
- Frontend pages are in `frontend/src/pages` and a minimal search UI is wired to call `/v1/search` on the API.

## Contributing

1. Fork and branch from `main`.
2. Run linters/tests locally (backend: `ruff`, `black`, `mypy`, `pytest`; frontend: `npm run typecheck`, `npm run lint`, `npm test`).
3. Open a PR with the problem, solution, and how to test.

---


## Demo / Animated snippet

We include a small helper script to demo the app in a terminal (suitable for recording with asciinema).

To record a short demo and embed it in the README later:

1. Install asciinema (https://asciinema.org/docs/installation).

2. Record using the helper script:

```bash
# from repo root
asciinema rec demo.cast ./scripts/record_demo.sh
```

3. Upload the cast to asciinema.org and copy the embed code they give you.

For now we include a placeholder for the demo. Replace the HTML/embed below with the embed you get from asciinema:

```html
<!-- Asciinema embed placeholder -->
<iframe
  src="https://asciinema.org/a/REPLACE_ME/embed"
  style="width: 100%; height: 300px; border: 0"
></iframe>
```

