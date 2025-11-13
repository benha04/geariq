from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

# Load .env from repository root if present so runtime picks up keys during local dev
try:
	from dotenv import load_dotenv

	env_path = Path(__file__).resolve().parents[2] / ".env"
	if env_path.exists():
		load_dotenv(dotenv_path=env_path)
except Exception:
	# dotenv is optional in production; ignore if not installed
	pass
from app.api.routes import search as search_routes
from app.api.routes import health as health_routes

app = FastAPI(title="GearIQ API", version="0.1.0")

# Enable CORS for the local frontend during development
if os.getenv("ENV") == "production":
	origins = [
		"http://localhost:3000",
		"http://127.0.0.1:3000",
	]
else:
	# During local development allow all origins to avoid CORS issues
	origins = ["*"]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(health_routes.router, prefix="")
app.include_router(search_routes.router, prefix="/v1")
