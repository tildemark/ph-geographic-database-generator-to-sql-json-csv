import pandas as pd
import asyncio
import os
import csv
import json
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from app.database import engine
from app.models import Region, Province, District, City, Barangay

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static_exports")

# Manual mapping for Independent Cities to their Geographic Provinces
GEOGRAPHIC_PROVINCE_MAP = {
    # NCR (Manila as "province" for context, though technically independent)
    "1300000000": "1300000000",
    # Cotabato City -> Maguindanao (BARMM)
    "1988040000": "1940000000", 
    # Isabela City -> Basilan
    "0997010000": "1507000000",
    # Region IX
    "0973320000": "0973000000", # Zamboanga City -> Zamboanga del Sur
    # Region X
    "1043050000": "1043000000", # Cagayan de Oro -> Misamis Oriental
    "1035040000": "1035000000", # Iligan City -> Lanao del Norte
    # Region XI
    "1124020000": "1124000000", # Davao City -> Davao del Sur
    "1130700000": "1102400000", # Davao City -> Davao del Sur
    # Region XII
    "1230800000": "1206300000", # General Santos -> South Cotabato
    # Region XIII (Caraga)
    "1630400000": "1600200000", # Butuan City -> Agusan del Norte
    # CAR
    "1430300000": "1401100000", # Baguio -> Benguet
}

async def upsert_model(session, model_class, code, data):
    """
    Robust upsert by code.
    """
    result = await session.execute(select(model_class).where(model_class.code == code))
    obj = result.scalars().first()
    if not obj:
        obj = model_class(code=code, **data)
        session.add(obj)
    else:
        for key, value in data.items():
            setattr(obj, key, value)
    try:
        await session.flush()
    except IntegrityError as e:
        logger.error(f"❌ IntegrityError for {model_class.__name__} code={code}: {str(e)}")
        logger.error(f"   Data: {data}")
        await session.rollback()
        # Fallback to update if insert failed due to race
        result = await session.execute(select(model_class).where(model_class.code == code))
        obj = result.scalars().first()
        if obj:
            logger.info(f"   Fallback: Found existing {model_class.__name__} with code={code}, updating...")
            for key, value in data.items():
                setattr(obj, key, value)
            try:
                await session.flush()
                logger.info(f"   ✅ Successfully updated {model_class.__name__} code={code}")
            except IntegrityError as e2:
                logger.error(f"   ❌ Fallback update also failed for {model_class.__name__} code={code}: {str(e2)}")
                await session.rollback()
        else:
            logger.error(f"   ❌ Fallback failed: No existing {model_class.__name__} found with code={code}")

async def find_parent_city(session, barangay_code: str) -> str:
    """
    Find the parent city code for a barangay by looking up in the database.
    
    The PSGC file uses intermediate organizational codes for some barangays
    that don't map to actual city codes. This function finds the actual parent
    city by matching the longest common prefix.
    """
    # Try standard 7-digit prefix first (most common case)
    standard_city_code = f"{barangay_code[:7]}{'0'*3}"
    result = await session.execute(select(City).where(City.code == standard_city_code))
    city = result.scalars().first()
    if city:
        return standard_city_code
    
    # Fallback: Find all cities in the same region and match by longest prefix
    region_code = f"{barangay_code[:2]}{'0'*8}"
    result = await session.execute(
        select(City).where(City.region_code == region_code).order_by(City.code)
    )
    cities = result.scalars().all()
    
    if not cities:
        logger.warning(f"No cities found in region {region_code} for barangay {barangay_code}")
        return None
    
    # Find best match by longest common prefix
    best_match = None
    max_prefix_len = 0
    
    for city in cities:
        # Calculate common prefix length
        common_len = 0
        for i in range(min(len(barangay_code), len(city.code))):
            if barangay_code[i] == city.code[i]:
                common_len += 1
            else:
                break
        
        if common_len > max_prefix_len:
            max_prefix_len = common_len
            best_match = city.code
    
    if best_match:
        logger.info(f"Matched barangay {barangay_code} to city {best_match} (prefix length: {max_prefix_len})")
    else:
        logger.warning(f"Could not find parent city for barangay {barangay_code}")
    
    return best_match

async def process_psgc_file(file_path: str):
    """
    Parses the PSGC Excel file and upserts data into the database.
    """
    logger.info(f"Processing PSGC file: {file_path}")
    try:
        xls = pd.ExcelFile(file_path)
        sheet_name = 'PSGC' if 'PSGC' in xls.sheet_names else xls.sheet_names[0]
        # Load without headers to manually control indexing
        df = pd.read_excel(xls, sheet_name=sheet_name, header=None, dtype=str)
        logger.info(f"Loaded sheet: {sheet_name} with {len(df)} rows")
    except Exception as e:
        logger.error(f"Error reading Excel file: {e}")
        raise

    # Clean data: Strictly pad code to 10 digits
    def clean_code(x):
        if pd.isna(x): return None
        s = str(x).split('.')[0].strip()
        if not s.isdigit(): return None
        return s.zfill(10)

    # Filter rows that look like data
    valid_levels = {'Reg', 'Prov', 'Dist', 'City', 'Mun', 'Bgy'}
    
    data_rows = []
    for i in range(len(df)):
        level = str(df.iloc[i, 3]).strip() if pd.notnull(df.iloc[i, 3]) else ""
        if level in valid_levels:
            code = clean_code(df.iloc[i, 0])
            name = str(df.iloc[i, 1]).strip() if pd.notnull(df.iloc[i, 1]) else None
            if code and name:
                data_rows.append({
                    'code': code,
                    'name': name,
                    'level': level
                })

    logger.info(f"Identified {len(data_rows)} valid geographic records.")

    async with AsyncSession(engine) as session:
        # 1. Regions
        regions = [r for r in data_rows if r['level'] == 'Reg']
        logger.info(f"Syncing {len(regions)} regions...")
        for r in regions:
            code = f"{r['code'][:2]}{'0'*8}"
            await upsert_model(session, Region, code, {'name': r['name']})
        await session.commit()

        # 2. Provinces
        provinces = [r for r in data_rows if r['level'] == 'Prov']
        logger.info(f"Syncing {len(provinces)} provinces...")
        for r in provinces:
            code = f"{r['code'][:5]}{'0'*5}"
            region_code = f"{r['code'][:2]}{'0'*8}"
            await upsert_model(session, Province, code, {'name': r['name'], 'region_code': region_code})
        await session.commit()

        # 3. Districts
        districts = [r for r in data_rows if r['level'] == 'Dist']
        logger.info(f"Syncing {len(districts)} districts...")
        for r in districts:
            code = f"{r['code'][:5]}{'0'*5}"
            region_code = f"{r['code'][:2]}{'0'*8}"
            await upsert_model(session, District, code, {'name': r['name'], 'region_code': region_code})
        await session.commit()

        # 4. Cities/Municipalities
        cities = [r for r in data_rows if r['level'] in {'City', 'Mun'}]
        logger.info(f"Syncing {len(cities)} cities/municipalities...")
        for r in cities:
            full_code = r['code']
            code = f"{full_code[:7]}{'0'*3}"
            parent_code = f"{full_code[:5]}{'0'*5}"
            region_code = f"{full_code[:2]}{'0'*8}"
            
            # Identify parent
            province_result = await session.execute(select(Province).where(Province.code == parent_code))
            province_exists = province_result.scalars().first() is not None
            province_code = parent_code if province_exists else None
            district_code = None
            if not province_code:
                dist_exists = (await session.execute(select(District).where(District.code == parent_code))).scalars().first() is not None
                district_code = parent_code if dist_exists else None

            # Apply Geographic Mapping for HUCs/ICCs
            if code in GEOGRAPHIC_PROVINCE_MAP:
                province_code = GEOGRAPHIC_PROVINCE_MAP[code]
                logger.info(f"Mapping independent city {code} to geographic province {province_code}")

            await upsert_model(session, City, code, {
                'name': r['name'],
                'province_code': province_code,
                'district_code': district_code,
                'region_code': region_code
            })
        await session.commit()

        # 5. Barangays
        barangays = [r for r in data_rows if r['level'] == 'Bgy']
        logger.info(f"Syncing {len(barangays)} barangays...")
        for r in barangays:
            full_code = r['code']
            code = full_code
            city_code = await find_parent_city(session, full_code)
            
            if not city_code:
                logger.error(f"Could not find parent city for barangay {code} ({r['name']}), skipping...")
                continue
            
            parent_code = f"{full_code[:5]}{'0'*5}"
            region_code = f"{full_code[:2]}{'0'*8}"
            
            prov_exists = (await session.execute(select(Province).where(Province.code == parent_code))).scalars().first() is not None
            province_code = parent_code if prov_exists else None

            if city_code in GEOGRAPHIC_PROVINCE_MAP:
                province_code = GEOGRAPHIC_PROVINCE_MAP[city_code]

            await upsert_model(session, Barangay, code, {
                'name': r['name'],
                'city_code': city_code,
                'province_code': province_code,
                'region_code': region_code
            })
        await session.commit()
    
    logger.info("Ingestion complete. Generating static files...")
    await generate_static_files()

async def generate_static_files():
    """
    Dumps the database to JSON, CSV, SQL, XML files in the static folder.
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
        # Note: Large dataset, might need optimization but for now fetch all
        barangays = (await session.execute(select(Barangay))).scalars().all()
        _dump_data("barangays", barangays)

    # 1. JSON (Combined) - all.json
    all_data = {
        "regions": [r.model_dump() for r in regions],
        "provinces": [p.model_dump() for p in provinces],
        "cities": [c.model_dump() for c in cities],
        "barangays": [b.model_dump() for b in barangays]
    }
    with open(os.path.join(STATIC_DIR, "all.json"), 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2)

    # 2. SQL (Concatenated)
    with open(os.path.join(STATIC_DIR, "all.sql"), 'w', encoding='utf-8') as f_out:
        f_out.write(f"-- Complete Database Dump\n-- Generated on {pd.Timestamp.now().isoformat()}\n\n")
        for name in ["regions", "provinces", "cities", "barangays"]:
            src = os.path.join(STATIC_DIR, f"{name}.sql")
            if os.path.exists(src):
                with open(src, 'r', encoding='utf-8') as f_in:
                    f_out.write(f_in.read())
                    f_out.write("\n\n")

    # 3. XML (Combined)
    with open(os.path.join(STATIC_DIR, "all.xml"), 'w', encoding='utf-8') as f_out:
        f_out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f_out.write(f'<ph_geographic_data generated="{pd.Timestamp.now().isoformat()}">\n')
        
        for name, data in [("regions", regions), ("provinces", provinces), ("cities", cities), ("barangays", barangays)]:
            f_out.write(f'  <{name}>\n')
            for item in data:
                f_out.write('    <record>\n')
                for k, v in item.model_dump().items():
                    val = str(v) if v is not None else ""
                    # Basic escaping
                    val = val.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("'", "&apos;")
                    f_out.write(f'      <{k}>{val}</{k}>\n')
                f_out.write('    </record>\n')
            f_out.write(f'  </{name}>\n')
        f_out.write('</ph_geographic_data>')

    # 4. CSV (Flattened Master List using Pandas)
    try:
        # Convert to DataFrames
        df_r = pd.DataFrame([r.model_dump() for r in regions])
        df_p = pd.DataFrame([p.model_dump() for p in provinces])
        df_c = pd.DataFrame([c.model_dump() for c in cities])
        df_b = pd.DataFrame([b.model_dump() for b in barangays])
        
        logger.info(f"DF shapes: R={df_r.shape}, P={df_p.shape}, C={df_c.shape}, B={df_b.shape}")

        if not df_r.empty:
            df_r = df_r.rename(columns={'code': 'region_code', 'name': 'region_name', 'id': 'region_id'})
        if not df_p.empty:
            df_p = df_p.rename(columns={'code': 'province_code', 'name': 'province_name', 'id': 'province_id'})
        if not df_c.empty:
            df_c = df_c.rename(columns={'code': 'city_code', 'name': 'city_name', 'id': 'city_id'})
        if not df_b.empty:
            df_b = df_b.rename(columns={'code': 'barangay_code', 'name': 'barangay_name', 'id': 'id'})
            
        # Merge: Barangay -> City
        if df_b.empty:
            master = pd.DataFrame()
        else:
            master = pd.merge(df_b, df_c, on='city_code', how='left', suffixes=('', '_city'))
            
            # Merge: -> Province
            if not df_p.empty and 'province_code' in master.columns:
                master = pd.merge(master, df_p, on='province_code', how='left')
            
            # Merge: -> Region
            if not df_r.empty and 'region_code' in master.columns:
                master = pd.merge(master, df_r, on='region_code', how='left')

            # Reorder columns for readability
            cols = [
                'region_code', 'region_name',
                'province_code', 'province_name',
                'city_code', 'city_name',
                'barangay_code', 'barangay_name'
            ]
            desired_cols = [c for c in cols if c in master.columns]
            remaining = [c for c in master.columns if c not in desired_cols]
            final_cols = desired_cols + remaining
            
            master = master[final_cols]
            
            master.to_csv(os.path.join(STATIC_DIR, "all.csv"), index=False, encoding='utf-8')
            logger.info("Generated all.json, all.csv, all.sql, all.xml")
            
    except Exception as e:
        logger.error(f"Failed to generate all.csv: {e}")
        import traceback
        logger.error(traceback.format_exc())

def _format_sql_value(v):
    if v is None:
        return 'NULL'
    if isinstance(v, (int, float, bool)):
        return str(v)
    escaped = str(v).replace("'", "''")
    return f"'{escaped}'"

def _dump_data(name, data):
    """
    Dumps data in multiple formats: JSON, CSV, SQL INSERT, and XML
    """
    if not data:
        return
    
    dicts = [d.model_dump() for d in data]
    
    # JSON
    json_path = os.path.join(STATIC_DIR, f"{name}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(dicts, f, indent=2)
        
    # CSV
    csv_path = os.path.join(STATIC_DIR, f"{name}.csv")
    keys = list(data[0].model_dump().keys())
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for d in data:
            writer.writerow(d.model_dump())
    
    # SQL INSERT statements
    sql_path = os.path.join(STATIC_DIR, f"{name}.sql")
    table_name = name  # regions, provinces, cities, barangays
    with open(sql_path, 'w', encoding='utf-8') as f:
        f.write(f"-- SQL INSERT statements for {table_name}\n")
        f.write(f"-- Generated on {pd.Timestamp.now().isoformat()}\n\n")
        
        for record in dicts:
            columns = ', '.join(record.keys())
            values = ', '.join([_format_sql_value(v) for v in record.values()])
            f.write(f"INSERT INTO {table_name} ({columns}) VALUES ({values});\n")
    
    # XML format
    xml_path = os.path.join(STATIC_DIR, f"{name}.xml")
    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(f'<{name} generated="{pd.Timestamp.now().isoformat()}">\n')
        
        for record in dicts:
            f.write('  <record>\n')
            for k, v in record.items():
                val = str(v) if v is not None else ""
                val = val.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("'", "&apos;")
                f.write(f'    <{k}>{val}</{k}>\n')
            f.write('  </record>\n')
        f.write(f'</{name}>')
    
    logger.info(f"Generated {name}.json, {name}.csv, {name}.sql, {name}.xml")

if __name__ == "__main__":
    import asyncio
    asyncio.run(process_psgc_file("/app/temp_psgc.xlsx"))
