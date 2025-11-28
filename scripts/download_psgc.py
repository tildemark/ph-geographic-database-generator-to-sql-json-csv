import cloudscraper
from bs4 import BeautifulSoup
import os
import sys

# The specific PSA page where PSGC files are listed
PSA_URL = "https://psa.gov.ph/classification/psgc"

def download_latest_psgc():
    print(f"🔎 Scanning {PSA_URL} with Cloudscraper...")
    
    # Create a scraper instance that mimics a real Chrome browser
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )

    try:
        # We use scraper.get() instead of requests.get()
        response = scraper.get(PSA_URL)
        
        if response.status_code == 403:
            print("❌ Still getting 403 Forbidden. The site might have blocked your IP specifically.")
            sys.exit(1)
            
        response.raise_for_status()
        
    except Exception as e:
        print(f"❌ Failed to connect to PSA website: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Logic: Find the first <a> tag that links to an .xlsx file
    download_link = None
    
    for a in soup.find_all('a', href=True):
        href = a['href']
        # Check if it is an Excel file
        if href.endswith('.xlsx'):
            # PSA links are often relative (e.g., /system/files/...)
            if not href.startswith('http'):
                href = f"https://psa.gov.ph{href}"
            
            # Additional check: often the file we want contains "Publication" or "PSGC"
            # We accept the first xlsx we find on the main PSGC page as it's usually the latest release
            print(f"✅ Found candidate: {href}")
            download_link = href
            break 

    if not download_link:
        print("❌ No .xlsx file found on the page. PSA might have changed the HTML structure.")
        # Debug: Save the HTML to see what the bot saw
        with open("debug_page.html", "w", encoding='utf-8') as f:
            f.write(soup.prettify())
        print("ℹ️ Saved page content to debug_page.html for inspection.")
        sys.exit(1)

    print(f"⬇️ Downloading from: {download_link}")
    
    try:
        # Use the same scraper instance to download the file (preserves cookies/session)
        file_resp = scraper.get(download_link)
        file_resp.raise_for_status()
        
        output_path = 'psgc_data.xlsx'
        with open(output_path, 'wb') as f:
            f.write(file_resp.content)
            
        print(f"🎉 Success! File saved to: {output_path}")
        
    except Exception as e:
        print(f"❌ Error downloading file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_latest_psgc()
