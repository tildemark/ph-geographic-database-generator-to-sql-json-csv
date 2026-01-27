from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_session
from app.models import Region, Province, City, Barangay
from fastapi_limiter.depends import RateLimiter

router = APIRouter()

# Dependency for Rate Limiting: 60 requests per minute
limit_dependency = Depends(RateLimiter(times=60, seconds=60))


@router.get("/regions", response_model=List[Region], dependencies=[limit_dependency])
async def get_regions(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Region))
    return result.scalars().all()


@router.get("/regions/{code}/provinces", response_model=List[Province], dependencies=[limit_dependency])
async def get_provinces_by_region(code: str, session: AsyncSession = Depends(get_session)):
    code = code.zfill(10)
    result = await session.execute(select(Province).where(Province.region_code == code))
    return result.scalars().all()


@router.get("/provinces/{code}/cities", response_model=List[City], dependencies=[limit_dependency])
async def get_cities_by_province(code: str, session: AsyncSession = Depends(get_session)):
    code = code.zfill(10)
    result = await session.execute(select(City).where(City.province_code == code))
    return result.scalars().all()


@router.get("/regions/{code}/cities", response_model=List[City], dependencies=[limit_dependency])
async def get_cities_by_region(code: str, session: AsyncSession = Depends(get_session)):
    """Fetch cities directly under a region. Primarily for NCR which has no provinces."""
    code = code.zfill(10)
    result = await session.execute(select(City).where(City.region_code == code))
    return result.scalars().all()


@router.get("/cities/{code}/barangays", response_model=List[Barangay], dependencies=[limit_dependency])
async def get_barangays_by_city(code: str, session: AsyncSession = Depends(get_session)):
    code = code.zfill(10)
    result = await session.execute(select(Barangay).where(Barangay.city_code == code))
    return result.scalars().all()
