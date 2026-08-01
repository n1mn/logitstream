from fastapi import FastAPI

from app.config.settings import settings
from app.api.routes import router 

from prometheus_client import make_asgi_app

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version

    
)

metrics_app = make_asgi_app()

app.mount("/metrics", metrics_app)

app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to LogiStream",
        "environment": settings.environment
    }