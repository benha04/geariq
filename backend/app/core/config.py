from pydantic import BaseModel
import os

class Settings(BaseModel):
    env: str = os.getenv("ENV", "dev")
    db_url: str = os.getenv("VECTOR_DB_URL", "postgresql+psycopg://postgres:postgres@db:5432/geariq")
    redis_url: str = os.getenv("REDIS_URL", "redis://cache:6379/0")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")

settings = Settings()
