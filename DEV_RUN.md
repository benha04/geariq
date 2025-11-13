Local development: bring up DB, Redis, backend and frontend

1. Ensure Docker and docker-compose are installed and running.

2. From the repository root run the helper script (it will start DB + Redis, run alembic migrations, then start backend + frontend):

   ./scripts/dev_up.sh

3. Environment variables

   - The backend reads DB URL from VECTOR_DB_URL (used by alembic/env.py and settings). If you want to point to a custom DB, export VECTOR_DB_URL before running the script.
   - To enable Redis caching set REDIS_URL in backend env or your process.
   - To enable live Impact adapter set IMPACT_API_KEY and optionally IMPACT_PARTNER_SID.

4. Stopping services
   docker-compose down

Notes

- The helper script uses docker-compose.yml at the repo root and assumes services are named `db` and `cache` for Postgres+pgvector and Redis.
- Alembic runs inside the backend folder and will apply all migrations in backend/alembic/versions.
