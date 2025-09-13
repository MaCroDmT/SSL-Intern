import os
import time
import requests
from urllib.parse import urljoin
from tkinter import *
from tkinter import messagebox, filedialog, ttk

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def download_images_from_zara(page_url, folder, update_progress, total_count_callback):
    # Setup headless browser if you like
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # Path to your chromedriver executable
    service = Service('chromedriver.exe')  # adjust path if needed
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(page_url)
    time.sleep(3)  # wait for JS, images, lazy load to load (adjust as needed)
    
    # Optionally scroll a bit to force lazy load
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.5);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    
    # Find image elements
    images = driver.find_elements(By.TAG_NAME, "img")
    img_urls = set()
    for img in images:
        # Try different attributes
        src = img.get_attribute("src")
        if src:
            img_urls.add(src)
        # some images have srcset (multiple urls)
        srcset = img.get_attribute("srcset")
        if srcset:
            # srcset may have multiple sizes; pick maybe largest or all
            parts = [p.strip() for p in srcset.split(',')]
            for part in parts:
                # Each part is like "url xw" e.g. "https://... 800w"
                url_part = part.split()[0]
                if url_part:
                    img_urls.add(url_part)
        # could also check data-src, data-lazy, etc.
        data_src = img.get_attribute("data-src")
        if data_src:
            img_urls.add(data_src)

    driver.quit()

    img_urls = list(img_urls)
    total = len(img_urls)
    total_count_callback(total)
    
    if total == 0:
        return 0

    count = 0
    for i, url in enumerate(img_urls, start=1):
        try:
            # make absolute URL if needed
            abs_url = urljoin(page_url, url)
            response = requests.get(abs_url, timeout=10)
            if response.status_code == 200:
                # Determine extension
                ext = os.path.splitext(abs_url)[1].split('?')[0]
                if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    ext = '.jpg'
                filename = os.path.join(folder, f"image_{i}{ext}")
                with open(filename, 'wb') as f:
                    f.write(response.content)
                count += 1
        except Exception as e:
            print(f"Failed to download {url}: {e}")
        update_progress(i)
    return count

def on_download():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return
    folder = filedialog.askdirectory(title="Select Folder to Save Images")
    if not folder:
        return

    # Reset progress bar
    progress_bar["value"] = 0
    status_label.config(text="Preparing...")

    # Disable button while running
    download_btn.config(state=DISABLED)

    def update_progress(val):
        progress_bar["value"] = val
        root.update_idletasks()
        status_label.config(text=f"Downloaded {val} of {total_images} images")

    def total_count_callback(total):
        nonlocal total_images
        total_images = total
        progress_bar["maximum"] = total

    total_images = 0
    try:
        downloaded = download_images_from_zara(url, folder, update_progress, total_count_callback)
        if downloaded == 0:
            messagebox.showinfo("No Images", "No images found on this website.")
        else:
            messagebox.showinfo("Success", f"Downloaded {downloaded} images to:\n{folder}")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")
    finally:
        download_btn.config(state=NORMAL)
        status_label.config(text="Done")

# Tkinter UI
root = Tk()
root.title("Zara Image Downloader")
root.geometry("500x200")

Label(root, text="Enter Zara Product Page URL:").pack(pady=5)
url_entry = Entry(root, width=70)
url_entry.pack(pady=5)

download_btn = Button(root, text="Download Images", command=on_download)
download_btn.pack(pady=10)

progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=400, mode="determinate")
progress_bar.pack(pady=10)

status_label = Label(root, text="")
status_label.pack()

root.mainloop()
