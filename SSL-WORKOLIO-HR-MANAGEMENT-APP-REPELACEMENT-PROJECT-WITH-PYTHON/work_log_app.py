import tkinter as tk
from tkinter import messagebox
import threading
import time
import os
import pandas as pd
from datetime import datetime, date, timedelta
import ctypes
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.drawing.image import Image as OpenpyxlImage
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font
import io

class WorkLogApp:
    def __init__(self, master):
        self.master = master
        master.title("Employee Work Log")
        master.geometry("400x300")
        master.configure(bg="#f0f0f0")
        
        self.username = ""
        self.is_monitoring = False
        self.is_paused = False
        self.log_data = []
        
        self.user_data_dir = os.path.join(os.path.expanduser("~"), "WorkLogData")
        os.makedirs(self.user_data_dir, exist_ok=True)
        self.username_file = os.path.join(self.user_data_dir, "username.txt")

        if os.path.exists(self.username_file):
            with open(self.username_file, "r") as f:
                self.username = f.read().strip()
            self.show_main_frame()
        else:
            self.show_name_input_frame()
        
    def show_name_input_frame(self):
        """Displays the name input GUI."""
        self.master.geometry("400x150")
        self.name_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.name_frame.pack(pady=20, padx=20)
        
        tk.Label(self.name_frame, text="Please enter your name:", font=("Arial", 12), bg="#f0f0f0").pack(pady=(0, 5))
        
        self.name_entry = tk.Entry(self.name_frame, width=30, font=("Arial", 12), bd=2, relief="groove")
        self.name_entry.pack(pady=5)
        
        self.save_btn = tk.Button(self.name_frame, text="Save & Proceed", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", bd=2, relief="raised", command=self.save_name_and_show_main_frame)
        self.save_btn.pack(pady=10)

    def save_name_and_show_main_frame(self):
        """Saves the entered name and switches to the main GUI."""
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
        """Displays the main monitoring GUI."""
        self.master.geometry("400x300")
        self.main_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.main_frame.pack(pady=20, padx=20)

        self.time_label = tk.Label(self.main_frame, text="", font=("Arial", 12), bg="#f0f0f0")
        self.time_label.pack(pady=5)
        self.update_time()

        self.status_label = tk.Label(self.main_frame, text="Status: Ready", font=("Arial", 14, "bold"), bg="#f0f0f0")
        self.status_label.pack(pady=10)

        self.clock_in_btn = tk.Button(self.main_frame, text="Clock-in", font=("Arial", 12, "bold"), width=15, bg="#4CAF50", fg="white", command=self.clock_in)
        self.clock_in_btn.pack(pady=5)
        
        self.break_btn = tk.Button(self.main_frame, text="Take a Break", font=("Arial", 12, "bold"), width=15, bg="#FFC107", fg="black", command=self.take_a_break)
        self.break_btn.pack(pady=5)

        self.clock_out_btn = tk.Button(self.main_frame, text="Clock-out", font=("Arial", 12, "bold"), width=15, bg="#F44336", fg="white", command=self.clock_out)
        self.clock_out_btn.pack(pady=5)

    def update_time(self):
        """Updates the time and date display."""
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%I:%M:%S %p")
        self.time_label.config(text=f"Date: {date_str}\nTime: {time_str}")
        self.master.after(1000, self.update_time)

    def clock_in(self):
        """Starts the work session."""
        if self.is_monitoring:
            messagebox.showinfo("Already Clocked In", "You are already clocked in.")
            return

        self.is_monitoring = True
        self.is_paused = False
        self.start_time = datetime.now()
        self.log_activity("Clocked in to work", self.start_time, self.start_time)
        self.status_label.config(text="Status: Working...")
        self.monitoring_thread = threading.Thread(target=self.monitor_activity, daemon=True)
        self.monitoring_thread.start()
        messagebox.showinfo("Clocked In", "You have successfully clocked in.")

    def take_a_break(self):
        """Pauses work and logs a break."""
        if not self.is_monitoring or self.is_paused:
            messagebox.showwarning("Not Working", "You must be clocked in to take a break.")
            return

        end_time = datetime.now()
        duration = end_time - self.start_time
        self.log_activity("Worked", self.start_time, end_time, duration)
        
        self.is_paused = True
        self.break_start_time = datetime.now()
        self.status_label.config(text="Status: On Break")
        messagebox.showinfo("On Break", "Enjoy your break!")
        
        self.master.after(1000, self.check_break_resumption)

    def check_break_resumption(self):
        """Continuously checks if the break is over."""
        if self.is_paused:
            return
        
        if self.is_monitoring:
            messagebox.showinfo("Break Over", "Resuming work now.")
            self.is_paused = False
            self.start_time = datetime.now()
            duration = self.start_time - self.break_start_time
            self.log_activity("Took a break from work", self.break_start_time, self.start_time, duration)
            self.status_label.config(text="Status: Working...")
            self.monitoring_thread = threading.Thread(target=self.monitor_activity, daemon=True)
            self.monitoring_thread.start()
        else:
            self.master.after(1000, self.check_break_resumption)
    
    def clock_out(self):
        """Stops monitoring and saves data."""
        if not self.is_monitoring:
            messagebox.showwarning("Not Clocked In", "You must be clocked in to clock out.")
            return

        if self.is_paused:
            duration = datetime.now() - self.break_start_time
            self.log_activity("Took a break from work", self.break_start_time, datetime.now(), duration)
            self.is_paused = False

        self.is_monitoring = False
        end_time = datetime.now()
        duration = end_time - self.start_time
        self.log_activity("Worked", self.start_time, end_time, duration)
        self.log_activity("Clocked out from work", end_time, end_time)
        
        self.save_data_to_excel()
        self.save_summary_to_excel()
        
        self.status_label.config(text="Status: Clocked Out")
        messagebox.showinfo("Clocked Out", f"Clocked out. Your activity logs have been saved to your Downloads folder.")
        
    def log_activity(self, activity_type, start_t, end_t, duration=None):
        """Logs an activity to the in-memory list."""
        if duration:
            total_seconds = int(duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            duration_str = f"Worked for {hours:02d}h {minutes:02d}m {seconds:02d}s"
        else:
            duration_str = activity_type
        
        start_time_str = start_t.strftime("%I:%M %p")
        end_time_str = end_t.strftime("%I:%M %p") if end_t else "-"
        
        self.log_data.append({
            "Employee": self.username,
            "Date": start_t.strftime("%d %B %Y"),
            "Start Time": start_time_str,
            "End Time": end_time_str,
            "Activity Duration": duration_str
        })

    def is_internet_connected(self):
        """Checks for internet connectivity."""
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except:
            return False

    def is_system_locked(self):
        """Checks if the system is locked."""
        try:
            user32 = ctypes.windll.User32
            return user32.GetForegroundWindow() == 0
        except:
            return False
            
    def monitor_activity(self):
        """The main monitoring loop running in a separate thread."""
        last_internet_status = self.is_internet_connected()
        last_system_status = self.is_system_locked()
        
        internet_loss_start = None
        system_lock_start = None
        
        while self.is_monitoring and not self.is_paused:
            time.sleep(1)
            
            # Monitor Internet
            current_internet_status = self.is_internet_connected()
            if not current_internet_status and last_internet_status:
                internet_loss_start = datetime.now()
                self.log_activity("Internet interrupted", internet_loss_start, internet_loss_start, duration=None)
            elif current_internet_status and not last_internet_status and internet_loss_start:
                end_time = datetime.now()
                duration = end_time - internet_loss_start
                self.log_activity("Internet interrupted", internet_loss_start, end_time, duration)
                internet_loss_start = None
            last_internet_status = current_internet_status

            # Monitor System Lock
            current_system_status = self.is_system_locked()
            if current_system_status and not last_system_status:
                system_lock_start = datetime.now()
                self.log_activity("System locked", system_lock_start, system_lock_start, duration=None)
            elif not current_system_status and last_system_status and system_lock_start:
                end_time = datetime.now()
                duration = end_time - system_lock_start
                self.log_activity("System locked", system_lock_start, end_time, duration)
                system_lock_start = None
            last_system_status = current_system_status

    def parse_duration(self, duration_str):
        """Parses a duration string into a timedelta object."""
        try:
            parts = duration_str.replace("Worked for ", "").strip().split(' ')
            hours = int(parts[0].replace('h', ''))
            minutes = int(parts[1].replace('m', ''))
            seconds = int(parts[2].replace('s', ''))
            return timedelta(hours=hours, minutes=minutes, seconds=seconds)
        except:
            return timedelta(0)

    def analyze_data(self, df):
        """
        Performs the main data analysis and aggregation.
        Returns both user-friendly strings and raw numerical data for the chart.
        """
        df['Activity Duration (sec)'] = df['Activity Duration'].apply(lambda x: self.parse_duration(x).total_seconds())
        
        analysis = {}
        
        # Calculate raw numerical seconds for charting
        total_work_seconds = df[df['Activity Duration'].str.contains("Worked for")]['Activity Duration (sec)'].sum()
        total_break_seconds = df[df['Activity Duration'].str.contains("Took a break")]['Activity Duration (sec)'].sum()
        total_locked_seconds = df[df['Activity Duration'].str.contains("System locked")]['Activity Duration (sec)'].sum()
        total_interrupted_seconds = df[df['Activity Duration'].str.contains("Internet interrupted")]['Activity Duration (sec)'].sum()
        
        # Calculate summary values for the report table
        analysis['Worked for in a day'] = str(timedelta(seconds=int(total_work_seconds)))
        analysis['System locked/clocked out'] = df[df['Activity Duration'].str.contains("System locked|Clocked out")].shape[0]
        analysis['Took a break'] = df[df['Activity Duration'].str.contains("Took a break")].shape[0]
        analysis['Internet Interrupted'] = df[df['Activity Duration'].str.contains("Internet interrupted")].shape[0]

        total_idle_seconds = total_break_seconds + total_locked_seconds + total_interrupted_seconds
        idle_events = df[df['Activity Duration'].str.contains("Took a break|System locked|Internet interrupted")]
        avg_idle_time = total_idle_seconds / len(idle_events) if len(idle_events) > 0 else 0
        analysis['Average Idle Time'] = str(timedelta(seconds=int(avg_idle_time)))

        # Add raw numerical values to the analysis dict for the chart
        analysis['total_work_hours'] = total_work_seconds / 3600
        analysis['total_break_hours'] = total_break_seconds / 3600
        analysis['total_locked_hours'] = total_locked_seconds / 3600
        analysis['total_interrupted_hours'] = total_interrupted_seconds / 3600

        return analysis

    def save_data_to_excel(self):
        """Saves all logged data to an Excel file."""
        if not self.log_data:
            return
        
        df = pd.DataFrame(self.log_data)
        
        filename = f"{self.username.replace(' ', '')}-Work-log-Activity-{date.today().strftime('%Y-%m-%d')}.xlsx"
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.excel_path = os.path.join(downloads_path, filename)

        try:
            df.to_excel(self.excel_path, index=False)
        except Exception as e:
            messagebox.showerror("File Save Error", f"Could not save file: {e}")
            self.excel_path = None
            
    def save_summary_to_excel(self):
        """Generates and saves the summary Excel file with a chart."""
        if not self.log_data:
            return

        try:
            df = pd.DataFrame(self.log_data)
            analysis = self.analyze_data(df)

            # Create the data for the summary table (user-facing strings)
            summary_data = {
                'Metric': ['Worked for in a day', 'System locked/clocked out', 'Took a break', 'Internet Interrupted', 'Average Idle Time'],
                'Value': [
                    analysis['Worked for in a day'],
                    analysis['System locked/clocked out'],
                    analysis['Took a break'],
                    analysis['Internet Interrupted'],
                    analysis['Average Idle Time']
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            
            # Prepare data for the horizontal chart (raw numerical seconds)
            chart_data = {
                'Metric': ['Work', 'Break', 'System Locked', 'Internet Interrupted'],
                'Duration': [
                    analysis['total_work_hours'],
                    analysis['total_break_hours'],
                    analysis['total_locked_hours'],
                    analysis['total_interrupted_hours'],
                ]
            }
            
            # Create the workbook and sheets
            workbook = Workbook()
            summary_sheet = workbook.active
            summary_sheet.title = "Summary Report"

            # Write the header information
            summary_sheet['A1'] = self.username
            summary_sheet['A3'] = datetime.now().strftime("%Y-%m-%d")

            # Write the summary data to the sheet
            for r_idx, row in enumerate(dataframe_to_rows(summary_df, index=False, header=True), start=5):
                for c_idx, value in enumerate(row, start=1):
                    cell = summary_sheet.cell(row=r_idx, column=c_idx, value=value)
                    if r_idx == 5:
                        cell.font = Font(bold=True)
            
            # Create the horizontal bar chart
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.barh(chart_data['Metric'], chart_data['Duration'])
            ax.set_title('Activity Breakdown')
            ax.set_xlabel('Duration (Hours)')
            ax.set_ylabel('Activity')
            plt.tight_layout()

            # Save the chart to a buffer
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            
            # Embed the image into the worksheet
            img = OpenpyxlImage(buf)
            img.anchor = 'A15'
            summary_sheet.add_image(img)
            
            # Save the workbook to the Downloads folder
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            filename = f"{self.username.replace(' ', '')}-Work-Summary-Report-{date.today().strftime('%Y-%m-%d')}.xlsx"
            file_path = os.path.join(downloads_path, filename)
            workbook.save(file_path)

        except Exception as e:
            messagebox.showerror("Summary File Save Error", f"Could not create summary report: {e}")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = WorkLogApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
