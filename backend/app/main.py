from fastapi import FastAPI
from app.api.routes import search as search_routes
from app.api.routes import health as health_routes

app = FastAPI(title="GearIQ API", version="0.1.0")
app.include_router(health_routes.router, prefix="")
app.include_router(search_routes.router, prefix="/v1")
