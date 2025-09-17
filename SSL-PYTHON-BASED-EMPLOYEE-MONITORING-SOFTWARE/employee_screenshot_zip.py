import tkinter as tk
from tkinter import messagebox
import threading
import pyautogui
import time
import os
from datetime import datetime, date
import zipfile

class ScreenshotApp:
    def __init__(self, master):
        self.master = master
        master.title("Employee Monitoring (Local)")
        master.geometry("300x180")

        self.status = "stopped"
        self.thread = None

        # Buttons
        self.start_btn = tk.Button(master, text="Start", width=10, command=self.start)
        self.start_btn.pack(pady=5)

        self.pause_btn = tk.Button(master, text="Pause", width=10, command=self.pause)
        self.pause_btn.pack(pady=5)

        self.stop_btn = tk.Button(master, text="Stop", width=10, command=self.stop)
        self.stop_btn.pack(pady=5)

        # Folder to save screenshots
        self.screenshot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)

    def capture_screenshots(self):
        while self.status == "started":
            now = datetime.now()
            filename = f"screenshot_{now.strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            print(f"Saved: {filename}")

            # Wait for 5 minutes, but break if paused/stopped
            for _ in range(300):
                if self.status != "started":
                    break
                time.sleep(1)

    def start(self):
        if self.status != "started":
            self.status = "started"
            self.thread = threading.Thread(target=self.capture_screenshots)
            self.thread.start()
            messagebox.showinfo("Status", "Screenshot capture started.")

    def pause(self):
        if self.status == "started":
            self.status = "paused"
            messagebox.showinfo("Status", "Screenshot capture paused.")

    def stop(self):
        if self.status != "stopped":
            self.status = "stopped"
            self.zip_today_screenshots()
            messagebox.showinfo("Status", "Screenshot capture stopped and zipped.")

    def zip_today_screenshots(self):
        today_str = date.today().strftime("%Y%m%d")
        zip_filename = f"screenshots_{today_str}.zip"

        # Ensure screenshots folder path is relative to the script location
        screenshot_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")

        # Temporary path for zip (inside the screenshots folder)
        temp_zip_path = os.path.join(screenshot_folder, zip_filename)

        with zipfile.ZipFile(temp_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in os.listdir(screenshot_folder):
                if file.startswith("screenshot_" + today_str):
                    zipf.write(os.path.join(screenshot_folder, file), arcname=file)

        # Move zip to user's Downloads folder
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", zip_filename)
        os.replace(temp_zip_path, downloads_path)

        print(f"ZIP created and moved to Downloads: {downloads_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()
