import pandas as pd
import sys
import os

REQUIRED_COLUMNS = ['Geographic Level', 'Name', 'Province Name'] # Add others as needed

def validate(file_path):
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found!")
        sys.exit(1)

    try:
        # Read just the header to be fast
        df = pd.read_excel(file_path, nrows=5)
        
        # Check if columns exist
        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            print(f"❌ Invalid Data! Missing columns: {missing}")
            print(f"   Found columns: {list(df.columns)}")
            sys.exit(1)
            
        print("✅ Excel file structure looks valid!")
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    validate('psgc_data.xlsx')