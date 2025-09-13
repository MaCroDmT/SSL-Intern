import os
import requests
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_images():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a valid URL.")
        return

    # Ask user where to save images
    folder = filedialog.askdirectory(title="Select Folder to Save Images")
    if not folder:
        return

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all <img> tags
        imgs = soup.find_all("img")
        total = len(imgs)

        if total == 0:
            messagebox.showinfo("No Images", "No images found on this website.")
            return

        # Configure progress bar
        progress_bar["maximum"] = total
        progress_bar["value"] = 0
        root.update_idletasks()

        count = 0
        for i, img in enumerate(imgs, start=1):
            img_url = img.get("src")
            if not img_url:
                continue

            # Handle relative URLs
            img_url = urljoin(url, img_url)

            try:
                img_data = requests.get(img_url, timeout=10).content
                file_ext = os.path.splitext(img_url)[1].split("?")[0]  # get file extension
                if file_ext == "":
                    file_ext = ".jpg"

                file_name = os.path.join(folder, f"image_{i}{file_ext}")
                with open(file_name, "wb") as f:
                    f.write(img_data)
                count += 1
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")

            # Update progress bar
            progress_bar["value"] = i
            root.update_idletasks()

        messagebox.showinfo("Success", f"Downloaded {count} images to:\n{folder}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch webpage:\n{e}")


# Tkinter UI
root = Tk()
root.title("Website Image Downloader")
root.geometry("400x200")

Label(root, text="Enter Website URL:").pack(pady=5)
url_entry = Entry(root, width=50)
url_entry.pack(pady=5)

Button(root, text="Download Images", command=download_images).pack(pady=10)

# Progress bar
progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=300, mode="determinate")
progress_bar.pack(pady=10)

root.mainloop()
