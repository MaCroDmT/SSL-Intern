import os
import time
import requests
import pandas as pd
from urllib.parse import urljoin, urlparse
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# =============== Selenium Setup =====================
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # remove if you want to see browser
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = ChromeService(ChromeDriverManager().install())

# =============== Function to download images =====================
def download_images_from_any_website(page_url, folder):
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(page_url)
    time.sleep(5)  # wait to load

    # Scroll to load lazy images
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Find images
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

# =============== Main =====================
def main():
    excel_file = input("Enter your Excel file path (e.g., C:\\Users\\DELL\\Documents\\links.xlsx): ").strip()
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
    main()
