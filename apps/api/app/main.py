from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.settings import settings

app = FastAPI(
    title=f"{settings.APP_NAME} API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        f"http://{settings.WEB_HOST}:{settings.WEB_PORT}",
        f"http://127.0.0.1:{settings.WEB_PORT}",
        f"http://localhost:{settings.WEB_PORT}",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/healthz")
def root_health() -> dict:
    return {
        "ok": True,
        "service": "futurefunded-api",
        "env": settings.ENV,
    }
