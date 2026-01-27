import pandas as pd

xls = pd.ExcelFile('/app/temp_psgc.xlsx')
df = pd.read_excel(xls, sheet_name='PSGC', header=None, dtype=str)

# Check Caloocan city entry
caloocan_city = df[(df[0] == '1380100000') & (df[3] == 'City')]
print("Caloocan City entry:")
print(caloocan_city[[0,1, 3]].to_string(index=False))
print()

# Check if Caloocan barangays exist in file
caloocan_bgy = df[(df[0].str.startswith('1380100', na=False)) & (df[3] == 'Bgy')]
print(f"Caloocan barangays in file: {len(caloocan_bgy)}")
if len(caloocan_bgy) > 0:
    print("\nFirst 5 barangays:")
    print(caloocan_bgy[[0, 1]].head(5).to_string(index=False))

# Check which city code pattern the barangays have    
if len(caloocan_bgy) > 0:
    print("\nFirst barangay full code:")
    print(caloocan_bgy.iloc[0, 0])
    print(f"City code extracted (7 digits + 000): {caloocan_bgy.iloc[0, 0][:7]}000")
