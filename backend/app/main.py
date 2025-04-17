from app.core.config import settings
from fastapi import FastAPI
from app.api.main import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title = settings.PROJECT_NAME,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)