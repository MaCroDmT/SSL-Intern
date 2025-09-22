import tkinter as tk
from tkinter import messagebox
import threading
import time
import os
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import win32gui

# Note: This code requires the following libraries to be installed.
# You can install them using pip:
# pip install pywin32 pandas openpyxl

class AppUsageMonitor:
    """
    A Tkinter-based application to monitor and log app and website usage.
    """
    def __init__(self, master):
        self.master = master
        master.title("App/Site Usage Monitor")
        master.geometry("400x200")
        master.configure(bg="#F0F0F0")

        self.username = ""
        self.monitoring_status = "stopped"
        self.monitoring_thread = None
        self.usage_data = {}
        self.start_time = time.time()
        self.active_window_title = None

        # Determine the user's profile directory for saving data
        self.user_data_dir = os.path.join(os.path.expanduser("~"), "AppUsageData")
        os.makedirs(self.user_data_dir, exist_ok=True)
        self.username_file = os.path.join(self.user_data_dir, "username.txt")
        
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Check if username exists, and show the appropriate frame
        if os.path.exists(self.username_file):
            with open(self.username_file, "r") as f:
                self.username = f.read().strip()
            self.show_main_frame()
        else:
            self.show_name_input_frame()
            
    def on_close(self):
        """Handle the window close event to ensure monitoring is stopped."""
        if self.monitoring_status == "started":
            self.stop_monitoring()
        self.master.destroy()

    def show_name_input_frame(self):
        """Displays the GUI for user name input."""
        self.master.geometry("400x150")
        
        self.name_frame = tk.Frame(self.master, bg="#F0F0F0")
        self.name_frame.pack(pady=20, padx=20)
        
        tk.Label(self.name_frame, text="Please enter your name:", font=("Arial", 12), bg="#F0F0F0").pack(pady=(0, 5))
        
        self.name_entry = tk.Entry(self.name_frame, width=30, font=("Arial", 12), bd=2, relief="groove")
        self.name_entry.pack(pady=5)
        
        self.save_btn = tk.Button(self.name_frame, text="Save & Proceed", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", bd=2, relief="raised", command=self.save_name_and_show_main_frame)
        self.save_btn.pack(pady=10)

    def save_name_and_show_main_frame(self):
        """Saves the entered name and transitions to the main monitoring GUI."""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Name cannot be empty.")
            return

        self.username = name
        with open(self.username_file, "w") as f:
            f.write(self.username)
        
        self.name_frame.destroy()
        self.show_main_frame()

    def show_main_frame(self):
        """Displays the main GUI with Start, Pause, and Stop buttons."""
        self.master.geometry("400x200")
        
        self.main_frame = tk.Frame(self.master, bg="#F0F0F0")
        self.main_frame.pack(pady=20, padx=20)
        
        self.status_label = tk.Label(self.main_frame, text="Status: Stopped", font=("Arial", 12, "bold"), bg="#F0F0F0")
        self.status_label.pack(pady=10)
        
        self.start_btn = tk.Button(self.main_frame, text="Start", font=("Arial", 10, "bold"), width=10, bg="#4CAF50", fg="white", command=self.start_monitoring)
        self.start_btn.pack(pady=5)
        
        self.pause_btn = tk.Button(self.main_frame, text="Pause", font=("Arial", 10, "bold"), width=10, bg="#FFC107", fg="black", command=self.pause_monitoring)
        self.pause_btn.pack(pady=5)
        
        self.stop_btn = tk.Button(self.main_frame, text="Stop", font=("Arial", 10, "bold"), width=10, bg="#F44336", fg="white", command=self.stop_monitoring)
        self.stop_btn.pack(pady=5)

    def start_monitoring(self):
        """Starts the monitoring thread."""
        if self.monitoring_status == "started":
            messagebox.showinfo("Already Running", "Monitoring is already in progress.")
            return

        self.monitoring_status = "started"
        self.status_label.config(text="Status: Monitoring...")
        self.start_time = time.time()
        self.active_window_title = self.get_active_window_title()
        
        if self.active_window_title and self.active_window_title not in self.usage_data:
            self.usage_data[self.active_window_title] = 0

        self.monitoring_thread = threading.Thread(target=self.monitor_activity, daemon=True)
        self.monitoring_thread.start()
        messagebox.showinfo("Success", "Monitoring started.")

    def pause_monitoring(self):
        """Pauses the monitoring thread."""
        if self.monitoring_status == "paused":
            messagebox.showinfo("Already Paused", "Monitoring is already paused.")
            return
        
        if self.monitoring_status == "started":
            self.monitoring_status = "paused"
            self.status_label.config(text="Status: Paused")
            messagebox.showinfo("Success", "Monitoring paused.")
            
    def stop_monitoring(self):
        """Stops the monitoring thread and saves data to Excel."""
        if self.monitoring_status == "stopped":
            messagebox.showinfo("Already Stopped", "Monitoring is already stopped.")
            return
        
        self.monitoring_status = "stopped"
        
        # Give a small delay for the monitoring thread to finish its loop
        time.sleep(0.5)

        self.status_label.config(text="Status: Stopped")
        
        # Save the current window's time before stopping
        if self.active_window_title and self.start_time:
            elapsed_time = time.time() - self.start_time
            self.usage_data[self.active_window_title] = self.usage_data.get(self.active_window_title, 0) + elapsed_time
            
        self.save_data_to_excel()
        messagebox.showinfo("Success", f"Monitoring stopped. Data saved to '{self.username}-appUsage.xlsx' in your Downloads folder.")

    def get_active_window_title(self):
        """
        Gets the title of the currently active window.
        Returns a simplified title by removing common suffixes like ' - Google Chrome'.
        """
        try:
            window_handle = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(window_handle)
            if not title:
                return "Unknown"
            
            # Simple title cleaning
            if " - Google Chrome" in title:
                title = title.replace(" - Google Chrome", "")
            if " - Mozilla Firefox" in title:
                title = title.replace(" - Mozilla Firefox", "")
            if " - Microsoft Edge" in title:
                title = title.replace(" - Microsoft Edge", "")
            if " - Brave" in title:
                title = title.replace(" - Brave", "")
            
            return title.strip()
        except:
            return "Unknown"

    def monitor_activity(self):
        """
        The main function that runs in a separate thread to monitor activity.
        """
        last_window_title = self.active_window_title
        self.start_time = time.time()
        
        while self.monitoring_status == "started":
            current_window_title = self.get_active_window_title()
            
            if current_window_title != last_window_title:
                # Update duration for the previous window
                if last_window_title and self.start_time:
                    elapsed_time = time.time() - self.start_time
                    self.usage_data[last_window_title] = self.usage_data.get(last_window_title, 0) + elapsed_time
                
                # Start timer for the new window
                self.start_time = time.time()
                last_window_title = current_window_title
                self.active_window_title = current_window_title
                
                # Initialize new window's duration if it's not in the data
                if self.active_window_title not in self.usage_data:
                    self.usage_data[self.active_window_title] = 0
            
            # Check the status every second
            time.sleep(1)
        
        # Final update when the loop breaks (due to pause/stop)
        if last_window_title and self.start_time:
            elapsed_time = time.time() - self.start_time
            self.usage_data[last_window_title] = self.usage_data.get(last_window_title, 0) + elapsed_time

    def format_duration(self, seconds):
        """
        Converts a total number of seconds into 'Hh Mm' format.
        """
        minutes, seconds_rem = divmod(seconds, 60)
        hours, minutes_rem = divmod(minutes, 60)
        
        return f"{int(hours):02d}h {int(minutes_rem):02d}m"

    def save_data_to_excel(self):
        """
        Saves the collected usage data to an Excel file.
        """
        if not self.usage_data:
            return
            
        data_list = []
        for app, duration in self.usage_data.items():
            if duration > 1: # Only save apps used for more than 1 second
                data_list.append({
                    "Employee": self.username,
                    "App/Site Name": app,
                    "Status": "Neutral",
                    "Activity Duration": self.format_duration(duration)
                })

        df = pd.DataFrame(data_list)
        
        filename = f"{self.username.replace(' ', '')}-appUsage.xlsx"
        
        # Save to the user's Downloads folder
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        file_path = os.path.join(downloads_path, filename)
        
        # Write the DataFrame to an Excel file
        try:
            df.to_excel(file_path, index=False)
        except Exception as e:
            messagebox.showerror("File Save Error", f"Could not save file: {e}")


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = AppUsageMonitor(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
