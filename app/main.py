from fastapi import FastAPI

from app.config.settings import settings
from app.api.routes import router as shipment_router 


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)
app.include_router(shipment_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to LogiStream",
        "environment": settings.environment
    }