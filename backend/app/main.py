from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import init_db
from app.routers import public, admin
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
    r = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)
    yield
    # Shutdown
    await r.close()

app = FastAPI(
    title="Open PH Geographic Data Platform",
    version="2.3.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

app.include_router(public.router, prefix="/api", tags=["Public"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])