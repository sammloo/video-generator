from fastapi import APIRouter
from app.api.routes import video, news, health

api_router = APIRouter()
api_router.include_router(video.router)
api_router.include_router(news.router)
api_router.include_router(health.router)

