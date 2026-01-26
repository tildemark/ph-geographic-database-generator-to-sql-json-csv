import pandas as pd
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Region, Province, District, City, Barangay
from app.database import engine
import logging
import csv
import json
import os
import shutil

logger = logging.getLogger(__name__)

# Output paths
STATIC_DIR = "/app/static_exports"

async def process_psgc_file(file_path: str):
    """
    Parses the PSGC Excel file and upserts data into the database.
    """
    logger.info(f"Processing PSGC file: {file_path}")
    # List all sheet names
    try:
        xls = pd.ExcelFile(file_path)
        logger.info(f"Available sheets: {xls.sheet_names}")
        if "PSGC" in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name="PSGC")
            logger.info("Loaded sheet: PSGC")
        else:
            df = pd.read_excel(xls, sheet_name=0)
            logger.info(f"Loaded first sheet: {xls.sheet_names[0]}")
    except Exception as e:
        logger.error(f"Error reading Excel file: {e}")
        raise

    logger.info(f"Columns: {list(df.columns)}")
    logger.info(f"First 5 rows:\n{df.head()}\n")

    # Normalize columns
    df.columns = [c.strip() for c in df.columns]

    # ...existing code...
    
    async with AsyncSession(engine) as session:
        # 1. Regions
        regions_df = df[df['Geographic Level'] == 'Reg']
        logger.info(f"Regions found: {len(regions_df)}")
        for _, row in regions_df.iterrows():
            # New PSGC: Region code is first 2 digits + 8 zeros (10 digits)
            code = f"{str(row['10-digit PSGC'])[:2]}{'0'*8}"
            name = row['Name']
            logger.info(f"INSERT REGION: code={code}, name={name}")
            result = await session.execute(select(Region).where(Region.code == code))
            obj = result.scalars().first()
            if not obj:
                obj = Region(code=code, name=name)
                session.add(obj)
            else:
                obj.name = name
                session.add(obj)
        await session.commit()

        # 2. Provinces
        provinces_df = df[df['Geographic Level'] == 'Prov']
        logger.info(f"Provinces found: {len(provinces_df)}")
        for _, row in provinces_df.iterrows():
            full_code = str(row['10-digit PSGC'])
            name = row['Name']
            # Province code: first 5 digits + 5 zeros (10 digits)
            code = f"{full_code[:5]}{'0'*5}"
            # Region code: first 2 digits + 8 zeros (10 digits)
            region_code = f"{full_code[:2]}{'0'*8}"
            logger.info(f"INSERT PROVINCE: code={code}, name={name}, region_code={region_code}")
            result = await session.execute(select(Province).where(Province.code == code))
            obj = result.scalars().first()
            if not obj:
                obj = Province(code=code, name=name, region_code=region_code)
                session.add(obj)
            else:
                obj.name = name
                obj.region_code = region_code
                session.add(obj)
        await session.commit()

        # 3. Districts (NCR and others)
        districts_df = df[df['Geographic Level'] == 'Dist']
        logger.info(f"Districts found: {len(districts_df)}")
        for _, row in districts_df.iterrows():
            full_code = str(row['10-digit PSGC'])
            name = row['Name']
            # District code: all 10 digits
            code = full_code
            # Region code: first 2 digits + 8 zeros (10 digits)
            region_code = f"{full_code[:2]}{'0'*8}"
            result = await session.execute(select(District).where(District.code == code))
            obj = result.scalars().first()
            if not obj:
                obj = District(code=code, name=name, region_code=region_code)
                session.add(obj)
            else:
                obj.name = name
                obj.region_code = region_code
                session.add(obj)
        await session.commit()

        # 4. Cities/Municipalities
        cities_df = df[df['Geographic Level'] == 'City' ]
        logger.info(f"Cities found: {len(cities_df)}")
        for _, row in cities_df.iterrows():
            full_code = str(row['10-digit PSGC'])
            name = row['Name']
            # City code: first 7 digits + 3 zeros (10 digits)
            code = f"{full_code[:7]}{'0'*3}"
            # Province code: first 5 digits + 5 zeros (10 digits)
            province_code_candidate = f"{full_code[:5]}{'0'*5}"
            # Region code: first 2 digits + 8 zeros (10 digits)
            region_code = f"{full_code[:2]}{'0'*8}"
            # Check if province exists
            province_result = await session.execute(select(Province).where(Province.code == province_code_candidate))
            province_exists = province_result.scalars().first() is not None
            province_code = province_code_candidate if province_exists else None
            logger.info(f"INSERT CITY: code={code}, name={name}, province_code={province_code}, region_code={region_code}")
            result = await session.execute(select(City).where(City.code == code))
            obj = result.scalars().first()
            if not obj:
                obj = City(code=code, name=name, province_code=province_code, region_code=region_code)
                session.add(obj)
            else:
                obj.name = name
                obj.province_code = province_code
                obj.region_code = region_code
                session.add(obj)
        await session.commit()

        # 5. Barangays
        barangays_df = df[df['Geographic Level'] == 'Bgy']
        logger.info(f"Barangays found: {len(barangays_df)}")
        for _, row in barangays_df.iterrows():
            full_code = str(row['10-digit PSGC'])
            name = row['Name']
            # Barangay code: all 10 digits
            code = full_code
            # City code: first 7 digits + 3 zeros (10 digits)
            city_code = f"{full_code[:7]}{'0'*3}"
            # Province code: first 5 digits + 5 zeros (10 digits)
            province_code = f"{full_code[:5]}{'0'*5}"
            # Region code: first 2 digits + 8 zeros (10 digits)
            region_code = f"{full_code[:2]}{'0'*8}"
            result = await session.execute(select(Barangay).where(Barangay.code == code))
            obj = result.scalars().first()
            if not obj:
                obj = Barangay(code=code, name=name, city_code=city_code, province_code=province_code, region_code=region_code)
                session.add(obj)
            else:
                obj.name = name
                obj.city_code = city_code
                obj.province_code = province_code
                obj.region_code = region_code
                session.add(obj)
        await session.commit()
    
    logger.info("Ingestion complete. Generating static files...")
    await generate_static_files()

async def generate_static_files():
    """
    Dumps the database to JSON, CSV, SQL files in the static folder.
    """
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)

    async with AsyncSession(engine) as session:
        # Regions
        regions = (await session.execute(select(Region))).scalars().all()
        _dump_data("regions", regions)
        # Provinces
        provinces = (await session.execute(select(Province))).scalars().all()
        _dump_data("provinces", provinces)
        # Cities
        cities = (await session.execute(select(City))).scalars().all()
        _dump_data("cities", cities)
        # Barangays
        barangays = (await session.execute(select(Barangay))).scalars().all()
        _dump_data("barangays", barangays)

def _dump_data(name, data):
    # JSON
    json_path = os.path.join(STATIC_DIR, f"{name}.json")
    with open(json_path, 'w') as f:
        dicts = [d.model_dump() for d in data]
        json.dump(dicts, f)
        
    # CSV
    csv_path = os.path.join(STATIC_DIR, f"{name}.csv")
    if data:
        keys = data[0].model_dump().keys()
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for d in data:
                writer.writerow(d.model_dump())
