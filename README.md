# GearIQ
GearIQ — Monorepo (v0.1)

Tagline: Find the best product for you — not just the cheapest item.

This scaffold gives you a copy‑pasteable starter to create the GearIQ GitHub repo with a working FastAPI backend, a Next.js+Tailwind frontend, Docker Compose (Postgres + pgvector + Redis), CI, and contribution templates.

1) Create the GitHub repo & push (commands)

# prerequisites: gh CLI, Git, Docker, Node 20+, Python 3.11+

mkdir geariq && cd geariq

# initialize & create GitHub repo
git init

# OPTIONAL: set your main branch name
git checkout -b main

echo "# GearIQ" > README.md

git add . && git commit -m "chore: init repo"

# Create remote on GitHub (public). Replace ORG or leave blank for personal.
# If you're in a GitHub org, use: gh repo create ORG/geariq --public --source=. --push
gh repo create geariq --public --source=. --push

After you paste in the files below, run:

git add .
git commit -m "feat: v0.1 scaffold (backend+frontend+devops)"
git push -u origin main

2) Repository Structure (monorepo)

geariq/
├─ .github/
│  ├─ ISSUE_TEMPLATE/
│  │  ├─ bug_report.md
│  │  └─ feature_request.md
│  ├─ pull_request_template.md
│  └─ workflows/
│     └─ ci.yml
├─ backend/
│  ├─ app/
│  │  ├─ api/
│  │  │  ├─ routes/
│  │  │  │  ├─ health.py
│  │  │  │  └─ search.py
│  │  │  └─ __init__.py
│  │  ├─ core/
│  │  │  ├─ config.py
│  │  │  └─ __init__.py
│  │  ├─ db/
│  │  │  ├─ base.py
│  │  │  ├─ init_db.py
│  │  │  ├─ session.py
│  │  │  └─ __init__.py
│  │  ├─ models/
│  │  │  ├─ product.py
│  │  │  └─ __init__.py
│  │  ├─ services/
│  │  │  ├─ matching.py
│  │  │  ├─ search_service.py
│  │  │  └─ __init__.py
│  │  ├─ main.py
│  │  └─ __init__.py
│  ├─ alembic/
│  │  ├─ versions/.gitkeep
│  │  └─ env.py
│  ├─ alembic.ini
│  ├─ pyproject.toml
│  └─ README.md
├─ frontend/
│  ├─ package.json
│  ├─ next.config.ts
│  ├─ postcss.config.js
│  ├─ tailwind.config.ts
│  └─ src/
│     ├─ pages/
│     │  └─ index.tsx
│     ├─ components/
│     │  └─ SearchBar.tsx
│     └─ lib/
│        └─ api.ts
├─ .env.example
├─ .gitignore
├─ CODE_OF_CONDUCT.md
├─ CONTRIBUTING.md
├─ docker-compose.yml
├─ LICENSE
└─ README.md

3) Top‑level files

.gitignore

# Node
node_modules/
.next/
*.log

# Python
__pycache__/
*.pyc
.venv/
.venv*/
.env

# OS
.DS_Store

# Alembic
backend/alembic/versions/*.pyc

LICENSE (MIT)

MIT License

Copyright (c) 2025 GearIQ

Permission is hereby granted, free of charge, to any person obtaining a copy ...

CODE_OF_CONDUCT.md

# Code of Conduct
We are committed to a harassment-free, inclusive community. Be kind, be respectful, and assume good intent. Report issues to maintainers@geariq.dev.

CONTRIBUTING.md

# Contributing
1. Fork & branch from `main`.
2. Run locally with Docker (see README).
3. Lint/format: `ruff`, `black`, `mypy` (backend) and `eslint`, `tsc` (frontend).
4. Ensure `pytest` and frontend `vitest` pass.
5. Open a PR with a clear description and screenshots for UI.

.env.example

# Shared
ENV=dev
OPENAI_API_KEY=
VECTOR_DB_URL=postgresql+psycopg://postgres:postgres@db:5432/geariq
REDIS_URL=redis://cache:6379/0

# Affiliate / Catalog (fill as you onboard)
IMPACT_API_KEY=
CJ_API_KEY=
RAKUTEN_API_KEY=

docker-compose.yml

version: "3.9"
services:
  db:
    image: ankane/pgvector:latest
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: geariq
    ports: ["5432:5432"]
    volumes:
      - pgdata:/var/lib/postgresql/data
  cache:
    image: redis:7-alpine
    ports: ["6379:6379"]
  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    environment:
      - VECTOR_DB_URL=${VECTOR_DB_URL}
      - REDIS_URL=${REDIS_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ENV=${ENV}
    volumes:
      - ./backend:/app
    ports: ["8000:8000"]
    depends_on: [db, cache]
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    environment:
      - NEXT_PUBLIC_API_BASE=http://localhost:8000
    volumes:
      - ./frontend:/app
    command: npm run dev
    depends_on: [backend]
volumes:
  pgdata:

.github/workflows/ci.yml

name: CI
on: [push, pull_request]
jobs:
  backend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -e .[dev]
      - run: ruff check . && black --check . && mypy app && pytest -q
  frontend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: frontend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm run typecheck && npm run lint && npm test --silent

.github/ISSUE_TEMPLATE/bug_report.md

---
name: Bug report
about: Something broke
---
**Describe the bug**
**Steps to reproduce**
**Expected**
**Screenshots**
**Env** (browser, OS)

.github/ISSUE_TEMPLATE/feature_request.md

---
name: Feature request
about: I have an idea
---
**Problem**
**Proposal**
**Alternatives**
**Additional context**

.github/pull_request_template.md

## What
-

## Why
-

## How to test
-

## Screenshots

4) Backend (FastAPI)

backend/pyproject.toml

[project]
name = "geariq-backend"
version = "0.1.0"
dependencies = [
  "fastapi~=0.115",
  "uvicorn[standard]~=0.30",
  "pydantic~=2.8",
  "SQLAlchemy~=2.0",
  "psycopg[binary]~=3.2",
  "alembic~=1.13",
  "redis~=5.0",
  "httpx~=0.27",
  "tenacity~=9.0",
  "pgvector~=0.3.5",
]
[project.optional-dependencies]
dev = ["pytest", "pytest-asyncio", "ruff", "black", "mypy", "types-redis"]
[tool.black]
line-length = 100

backend/app/core/config.py

from pydantic import BaseModel
import os

class Settings(BaseModel):
    env: str = os.getenv("ENV", "dev")
    db_url: str = os.getenv("VECTOR_DB_URL", "postgresql+psycopg://postgres:postgres@db:5432/geariq")
    redis_url: str = os.getenv("REDIS_URL", "redis://cache:6379/0")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")

settings = Settings()

backend/app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.db_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

backend/app/db/base.py

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

backend/app/models/product.py

from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(512))
    url: Mapped[str] = mapped_column(String(1024))
    retailer: Mapped[str] = mapped_column(String(64))
    price: Mapped[float] = mapped_column(Float)
    rating: Mapped[float] = mapped_column(Float, default=0)
    features: Mapped[str] = mapped_column(String(2048), default="")  # JSON string for v0

backend/app/api/routes/health.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    return {"ok": True}

backend/app/services/matching.py

from typing import List, Dict, Any

# v0: simple weighted score; later: embeddings + rules
WEIGHTS = {"price": 0.5, "rating": 0.3, "shipping": 0.2}

def score(candidate: Dict[str, Any]) -> float:
    price = candidate.get("price", 1e9)
    rating = candidate.get("rating", 0)
    shipping_days = candidate.get("shipping_days", 7)
    price_norm = 1.0 / max(price, 1.0)
    rating_norm = rating / 5.0
    shipping_norm = 1.0 / max(shipping_days, 1)
    return (WEIGHTS["price"]*price_norm + WEIGHTS["rating"]*rating_norm + WEIGHTS["shipping"]*shipping_norm)

def pick_best(candidates: List[Dict[str, Any]]) -> Dict[str, Any] | None:
    if not candidates:
        return None
    return max(candidates, key=score)

backend/app/services/search_service.py

from typing import List, Dict, Any

# TODO: Replace with affiliate/APIs (Impact, CJ, Rakuten) and cached enrichment.
# For v0, we stub a couple of retailers.

async def search_marketplaces(query: str, budget: float | None = None) -> List[Dict[str, Any]]:
    data = [
        {"title": "Acme MIPS Helmet", "retailer": "REI", "price": 129.99, "rating": 4.6, "shipping_days": 2, "url": "https://example.com/rei/acme-helmet"},
        {"title": "RoadPro MIPS Helmet", "retailer": "Amazon", "price": 119.00, "rating": 4.4, "shipping_days": 2, "url": "https://example.com/amazon/roadpro"},
        {"title": "TrailGuard Helmet", "retailer": "Dicks", "price": 149.99, "rating": 4.7, "shipping_days": 3, "url": "https://example.com/dicks/trailguard"}
    ]
    if budget is not None:
        data = [d for d in data if d["price"] <= budget]
    return data

backend/app/api/routes/search.py

from fastapi import APIRouter, Query
from pydantic import BaseModel
from app.services.search_service import search_marketplaces
from app.services.matching import pick_best

router = APIRouter()

class SearchResponse(BaseModel):
    best: dict | None
    candidates: list[dict]

@router.get("/search", response_model=SearchResponse)
async def search(q: str = Query(..., description="e.g., 'MIPS bike helmet'"), budget: float | None = Query(None)):
    candidates = await search_marketplaces(q, budget)
    best = pick_best(candidates)
    return {"best": best, "candidates": candidates}

backend/app/main.py

from fastapi import FastAPI
from app.api.routes import search as search_routes
from app.api.routes import health as health_routes

app = FastAPI(title="GearIQ API", version="0.1.0")
app.include_router(health_routes.router, prefix="")
app.include_router(search_routes.router, prefix="/v1")

backend/alembic.ini

[alembic]
script_location = alembic
sqlalchemy.url = %(DB_URL)s

backend/alembic/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.db.base import Base
from app.models import product  # noqa: F401
import os

config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("VECTOR_DB_URL", ""))
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

5) Frontend (Next.js + Tailwind)

frontend/package.json

{
  "name": "geariq-web",
  "private": true,
  "scripts": {
    "dev": "next dev -p 3000",
    "build": "next build",
    "start": "next start -p 3000",
    "lint": "eslint .",
    "typecheck": "tsc --noEmit",
    "test": "vitest run"
  },
  "dependencies": {
    "next": "14.2.5",
    "react": "18.3.1",
    "react-dom": "18.3.1",
    "axios": "1.7.7"
  },
  "devDependencies": {
    "@types/node": "20.11.0",
    "@types/react": "18.2.66",
    "@types/react-dom": "18.2.22",
    "autoprefixer": "10.4.19",
    "eslint": "8.57.0",
    "postcss": "8.4.39",
    "tailwindcss": "3.4.10",
    "typescript": "5.6.2",
    "vitest": "2.0.5"
  }
}

frontend/next.config.ts

import type { NextConfig } from 'next'
const nextConfig: NextConfig = {
  reactStrictMode: true,
  experimental: { typedRoutes: true }
}
export default nextConfig

frontend/postcss.config.js

module.exports = { plugins: { tailwindcss: {}, autoprefixer: {} } }

frontend/tailwind.config.ts

import type { Config } from 'tailwindcss'
export default {
  content: ["./src/**/*.{ts,tsx}"],
  theme: { extend: {} },
  plugins: []
} satisfies Config

frontend/src/lib/api.ts

import axios from 'axios'
export const api = axios.create({ baseURL: process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000' })

frontend/src/components/SearchBar.tsx

import { useState } from 'react'
import { api } from '@/lib/api'

type Props = { onResult: (data: any) => void }
export default function SearchBar({ onResult }: Props) {
  const [q, setQ] = useState('MIPS bike helmet')
  const [budget, setBudget] = useState('150')
  const [loading, setLoading] = useState(false)

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    const { data } = await api.get('/v1/search', { params: { q, budget } })
    onResult(data)
    setLoading(false)
  }

  return (
    <form onSubmit={submit} className="flex gap-2 w-full max-w-3xl">
      <input className="flex-1 border rounded-xl px-3 py-2" value={q} onChange={e=>setQ(e.target.value)} placeholder="Describe what you need…" />
      <input className="w-28 border rounded-xl px-3 py-2" value={budget} onChange={e=>setBudget(e.target.value)} placeholder="$" />
      <button className="rounded-xl px-4 py-2 bg-black text-white" disabled={loading}>{loading? 'Searching…':'Search'}</button>
    </form>
  )
}

frontend/src/pages/index.tsx

import { useState } from 'react'
import SearchBar from '@/components/SearchBar'

export default function Home() {
  const [result, setResult] = useState<any | null>(null)
  return (
    <main className="min-h-screen p-8 flex flex-col items-center gap-8">
      <h1 className="text-3xl font-bold">GearIQ</h1>
      <p className="text-gray-600">Find the best product for you — not just the cheapest item.</p>
      <SearchBar onResult={setResult} />
      {result && (
        <div className="w-full max-w-3xl grid gap-4">
          {result.best && (
            <div className="border rounded-xl p-4">
              <h2 className="font-semibold">Best Match</h2>
              <a className="underline" href={result.best.url} target="_blank" rel="noreferrer">{result.best.title}</a>
              <div className="text-sm text-gray-600">{result.best.retailer} • ${result.best.price} • ⭐ {result.best.rating}</div>
            </div>
          )}
          <div className="border rounded-xl p-4">
            <h3 className="font-medium mb-2">All Candidates</h3>
            <ul className="list-disc ml-5">
              {result.candidates.map((c:any, i:number)=> (
                <li key={i}><a className="underline" href={c.url} target="_blank" rel="noreferrer">{c.title}</a> — {c.retailer} • ${c.price} • ⭐ {c.rating}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </main>
  )
}

6) Local Development

# copy env
cp .env.example .env

# start services
docker compose up --build

# visit frontend
open http://localhost:3000
# check API
curl http://localhost:8000/health
curl "http://localhost:8000/v1/search?q=MIPS%20bike%20helmet&budget=150"

Reproducible local development (manual steps)

If you prefer to run services locally without Docker, follow these steps (macOS):

1. Backend (Python / FastAPI)

```bash
# ensure Python 3.11 is installed (e.g., via pyenv or system)
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
# install the backend in editable mode with dev extras
cd backend
python -m pip install -e ".[dev]"
# start the backend (uvicorn). Logs: /tmp/uvicorn.log
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload > /tmp/uvicorn.log 2>&1 & echo $! > /tmp/uvicorn.pid
# quick health check
curl http://127.0.0.1:8000/health
```

2. Frontend (Next.js)

```bash
cd frontend
# install node deps (Node 20+)
npm install
# start Next dev server. Logs: /tmp/next-dev.log
npm run dev > /tmp/next-dev.log 2>&1 & echo $! > /tmp/next-dev.pid
# verify server is up
curl -I http://127.0.0.1:3000
tail -n 200 /tmp/next-dev.log
```

Notes:
- The repository includes `frontend/next.config.mjs` (JS ESM) because Next.js does not support `next.config.ts` at runtime in the dev server. If you prefer a TypeScript config, use `next.config.mjs` to import/run a compiled config or run a prebuild step.
- The backend requires Python 3.11+ because the codebase uses modern syntax (PEP 604 union types `X | None`).
- If you plan to run with Docker Compose, the compose file maps ports 3000 and 8000 for convenience.

7) Product Notes (from brief)

Category‑Level Tracking: start with rule‑based feature extraction (keywords + regex); iterate to embeddings in pgvector.

Dynamic Matching: current matching.py uses a simple weighted score; plan: learn weights from click‑through / conversions.

Profiles: persist per‑user weights (price sensitivity, brand preference) in DB; expose /v1/profile later.

Live Price Intelligence: cron workers to ingest feeds hourly; store time series per product/category.

Cross‑Retailer Coverage: prioritize affiliate/catalog feeds to avoid scraping/rate limits.

8) Initial Roadmap (create as GitHub issues)

Ingestion MVP: design catalog schema; import one affiliate feed.

Matching v0.2: add shipping speed, availability, and simple MIPS feature flag.

Frontend polish: result cards, filters, and “Track price” CTA.

Alerts: Redis queue + worker to send email/web push when thresholds met.

Auth: NextAuth or Clerk; per‑user preferences.

Observability: OpenTelemetry traces, basic dashboards.

Chrome extension: inject mini‑panel; query /v1/search from PDP and category pages.

