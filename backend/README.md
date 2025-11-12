Backend (FastAPI)

Run locally:

pip install -e .[dev]
uvicorn app.main:app --reload

Migrations:

alembic revision --autogenerate -m "init"
alembic upgrade head
