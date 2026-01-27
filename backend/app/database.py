from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Fallback or error, but let's assume it's set or construct it
    from urllib.parse import quote_plus
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secure_password_here")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "ph_geo_db")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
    
    encoded_user = quote_plus(POSTGRES_USER)
    encoded_password = quote_plus(POSTGRES_PASSWORD)
    DATABASE_URL = f"postgresql+asyncpg://{encoded_user}:{encoded_password}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"
else:
    # Ensure usage of asyncpg driver
    if "postgresql://" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)

async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all) # Optional: if we want to wipe clean on restart
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
