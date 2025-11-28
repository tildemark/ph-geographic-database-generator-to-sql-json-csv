import requests
from bs4 import BeautifulSoup
import os
import sys

# The specific PSA page where PSGC files are listed
# Note: PSA updates their site structure occasionally. 
# If this breaks, check if this URL is still valid.
PSA_URL = "https://psa.gov.ph/classification/psgc"

def download_latest_psgc():
    print(f"🔎 Scanning {PSA_URL}...")
    
    # We must use a User-Agent, otherwise PSA's firewall might block the script
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(PSA_URL, headers=headers, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to connect to PSA website: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Logic: Find the first <a> tag that links to an .xlsx file
    # and usually contains text like "Publication" or "PSGC"
    download_link = None
    
    for a in soup.find_all('a', href=True):
        href = a['href']
        # Check if it is an Excel file
        if href.endswith('.xlsx'):
            # PSA links are often relative (e.g., /system/files/...)
            if not href.startswith('http'):
                href = f"https://psa.gov.ph{href}"
            
            print(f"✅ Found candidate: {href}")
            download_link = href
            break # We assume the first one is the latest. 

    if not download_link:
        print("❌ No .xlsx file found on the page. PSA might have changed the HTML structure.")
        sys.exit(1)

    print(f"⬇️ Downloading from: {download_link}")
    
    try:
        file_resp = requests.get(download_link, headers=headers)
        file_resp.raise_for_status()
        
        # Save to the root directory
        output_path = 'psgc_data.xlsx'
        with open(output_path, 'wb') as f:
            f.write(file_resp.content)
            
        print(f"🎉 Success! File saved to: {output_path}")
        
    except Exception as e:
        print(f"❌ Error downloading file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_latest_psgc()
