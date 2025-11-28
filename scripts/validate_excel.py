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
            print(f"    Found columns: {list(df.columns)}")
            sys.exit(1)
            
        print(f"✅ Excel file '{file_path}' structure looks valid!")
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # --- START OF NEW/MODIFIED CODE ---
    
    # sys.argv[0] is the script name itself.
    # We check if there is at least one argument after the script name (index 1).
    if len(sys.argv) < 2:
        print("Usage: python validation_script.py <excel_file_path>")
        # Indicate an error and exit if the argument is missing
        sys.exit(1)
    
    # The filename is the second item in the argument list (index 1)
    file_to_validate = sys.argv[1] 
    
    # Call the validation function with the provided filename
    validate(file_to_validate)

    # --- END OF NEW/MODIFIED CODE ---
