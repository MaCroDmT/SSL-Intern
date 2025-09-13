import os
import time
import requests
import pandas as pd
from urllib.parse import urljoin, urlparse
import re
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import platform

# ======== Step 1: Set GeckoDriver path =========
# Make sure you download the correct version from:
# https://github.com/mozilla/geckodriver/releases
# Choose win64 if your system is 64-bit
gecko_path = r"C:\Users\DELL\AppData\Local\Programs\Python\Python313\Scripts\geckodriver.exe"  # <-- Update this path

# ======== Step 2: Firefox Selenium Setup =========
firefox_options = Options()
firefox_options.add_argument("--headless")  # Remove this line if you want to see browser
firefox_options.add_argument("--disable-gpu")
firefox_options.add_argument("--no-sandbox")

service = FirefoxService(executable_path=gecko_path)

# ======== Step 3: Image Downloader Function =========
def download_images_from_any_website(page_url, folder):
    try:
        driver = webdriver.Firefox(service=service, options=firefox_options)
    except Exception as e:
        print(f"❌ Could not start Firefox: {e}")
        return 0

    try:
        driver.get(page_url)
        time.sleep(5)  # Wait for page to load

        # Scroll to load lazy images
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Collect image URLs
        images = driver.find_elements(By.XPATH, "//img | //picture | //div[contains(@style, 'background-image')]")
        img_urls = set()
        for img in images:
            src = img.get_attribute("src")
            if src and 'data:image' not in src:
                img_urls.add(src)

            srcset = img.get_attribute("srcset")
            if srcset:
                for part in [p.strip().split()[0] for p in srcset.split(',') if p.strip()]:
                    img_urls.add(part)

            data_src = img.get_attribute("data-src")
            if data_src:
                img_urls.add(data_src)

            style = img.get_attribute("style")
            if style and 'background-image' in style:
                url_match = re.search(r'url\("?\'?(.+?)"?\'?\)', style)
                if url_match:
                    img_urls.add(url_match.group(1))

        driver.quit()
        print(f"Found {len(img_urls)} images on {page_url}")

        # Save images
        count = 0
        for i, url in enumerate(img_urls, start=1):
            try:
                abs_url = urljoin(page_url, url)
                response = requests.get(abs_url, timeout=10,
                                        headers={'User-Agent': 'Mozilla/5.0'})
                if response.status_code == 200:
                    ext = os.path.splitext(abs_url)[1].split('?')[0]
                    if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                        ext = '.jpg'
                    filename = os.path.join(folder, f"image_{i}{ext}")
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    count += 1
            except Exception as e:
                print(f"❌ Failed {url}: {e}")
        return count

    except Exception as e:
        driver.quit()
        print(f"❌ Error processing {page_url}: {e}")
        return 0

# ======== Step 4: Main =========
def main():
    excel_file = input("Enter your Excel file path (e.g., C:\\Users\\DELL\\Downloads\\Sample-Link.xlsx): ").strip().strip('"').strip("'")
    if not os.path.exists(excel_file):
        print("❌ File does not exist!")
        return

    df = pd.read_excel(excel_file, header=None)

    base_folder = os.path.join(os.getcwd(), "Downloaded_Images")
    os.makedirs(base_folder, exist_ok=True)

    for index, row in df.iterrows():
        url = str(row.iloc[0]).strip()
        if not url.startswith(('http://', 'https://')):
            print(f"Skipping invalid URL in row {index+1}: {url}")
            continue

        domain = urlparse(url).netloc
        domain_folder = os.path.join(base_folder, re.sub(r'[^a-zA-Z0-9]', '_', domain))
        os.makedirs(domain_folder, exist_ok=True)

        print(f"\n--- Processing {url} ---")
        downloaded = download_images_from_any_website(url, domain_folder)
        print(f"✅ {downloaded} images saved in {domain_folder}")

    print("\n🎉 Done! All images saved into:", base_folder)

if __name__ == "__main__":
    print(f"Running on {platform.system()} {platform.architecture()[0]}")
    main()
