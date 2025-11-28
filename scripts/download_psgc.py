import requests
from bs4 import BeautifulSoup
import os

# Target the main PSGC page
URL = "https://psa.gov.ph/classification/psgc"

def download_latest_file():
    print(f"Checking {URL}...")
    headers = {'User-Agent': 'Mozilla/5.0'} # Pretend to be a browser
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Logic: Find the first link that ends in .xlsx and has "Publication" in text/url
    # Note: PSA changes their site often, so this logic needs to be robust
    download_link = None
    for a in soup.find_all('a', href=True):
        href = a['href']
        text = a.text.lower()
        if '.xlsx' in href and 'publication' in text:
            download_link = href
            break
    
    if not download_link:
        print("❌ No Excel file found. PSA might have changed the site structure.")
        exit(1)

    print(f"⬇️ Found file: {download_link}")
    
    # Download content
    file_resp = requests.get(download_link, headers=headers)
    with open('psgc_data.xlsx', 'wb') as f:
        f.write(file_resp.content)
    print("✅ Download complete: psgc_data.xlsx")

if __name__ == "__main__":
    download_latest_file()