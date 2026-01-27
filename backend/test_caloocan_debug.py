import pandas as pd
from sqlmodel import select
from app.database import engine
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import City

async def test_caloocan():
    xls = pd.ExcelFile('/app/new_psgc.xlsx')
    df = pd.read_excel(xls, sheet_name='PSGC', header=None, dtype=str)
    
    # Get first Caloocan barangay
    caloocan_bgys = df[(df[0].astype(str).str.startswith('1380100')) & (df[3] == 'Bgy')]
    
    if len(caloocan_bgys) > 0:
        first_bgy_code = caloocan_bgys.iloc[0, 0]
        print(f"First Caloocan barangay code: {first_bgy_code}")
        
        # Apply same logic as ingestion script
        city_code = f"{first_bgy_code[:7]}{'0'*3}"
        print(f"Computed city_code: {city_code}")
        
        # Check if city exists
        async with AsyncSession(engine) as session:
            result = await session.execute(select(City).where(City.code == city_code))
            city = result.scalars().first()
            if city:
                print(f"✅ City FOUND: {city.name} (code: {city.code})")
            else:
                print(f"❌ City NOT FOUND for code: {city_code}")
                # Check what cities DO exist near this code
                result = await session.execute(select(City).where(City.code.like('13801%')))
                nearby_cities = result.scalars().all()
                print(f"\nNearby cities:")
                for c in nearby_cities:
                    print(f"  - {c.code}: {c.name}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_caloocan())
