import pandas as pd

xls = pd.ExcelFile('/app/new_psgc.xlsx')
df = pd.read_excel(xls, sheet_name='PSGC', header=None, dtype=str)

# Find barangays that would compute to city_code 1380601000
barangays_1380601 = df[(df[0].astype(str).str.startswith('1380601', na=False)) & (df[3] == 'Bgy')]
print(f"Barangays with code prefix 1380601: {len(barangays_1380601)}")
if len(barangays_1380601) > 0:
    print(f"\nFirst 5 barangays:")
    for idx, row in barangays_1380601.head(5).iterrows():
        full_code = row[0]
        city_code = f"{full_code[:7]}000"
        print(f"  Code: {full_code}, Name: {row[1]}, Computed city_code: {city_code}")
        
# Check what cities actually exist in NCR
print(f"\n\nNCR Cities in the Excel file:")
ncr_cities = df[(df[0].astype(str).str.startswith('1380', na=False)) & (df[3] == 'City')]
for idx, row in ncr_cities.iterrows():
    full_code = row[0]
    truncated_code = f"{full_code[:7]}000"
    print(f"  {full_code} (truncated: {truncated_code}) - {row[1]}")
