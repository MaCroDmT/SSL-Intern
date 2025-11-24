import tkinter as tk
from tkinter import ttk
import psutil
import requests
import threading

class AdvancedMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Dell Command Center")
        self.geometry("500x450")
        self.resizable(False, False)
        self.configure(bg="#121212") 
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#121212", foreground="#e0e0e0", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 11, "bold"), foreground="#00ff99")
        style.configure("Warning.TLabel", foreground="#ff4444")

       
        self.rows = 0
        
       
        self.add_header("PROCESSOR & THERMALS")
        self.lbl_cpu_load = self.add_metric("CPU Load")
        self.lbl_cpu_temp = self.add_metric("CPU Package Temp")

        
        self.add_header("MEMORY ANALYSIS")
        self.lbl_ram = self.add_metric("Physical RAM")
        self.lbl_swap = self.add_metric("Swap File (Virtual RAM)")

        # Section 3: Storage (SSD Activity)
        self.add_header("STORAGE & BATTERY")
        self.lbl_disk = self.add_metric("SSD Read/Write")
        self.lbl_batt = self.add_metric("Battery Status")

        self.previous_disk_io = psutil.disk_io_counters()
        
        # Start Update Loop
        self.update_metrics()

    def add_header(self, text):
        ttk.Label(self, text=text, style="Header.TLabel").grid(
            row=self.rows, column=0, padx=20, pady=(15, 5), sticky="w"
        )
        self.rows += 1

    def add_metric(self, label):
        ttk.Label(self, text=label).grid(row=self.rows, column=0, padx=30, pady=2, sticky="w")
        value_lbl = ttk.Label(self, text="WAITING...", font=("Consolas", 10))
        value_lbl.grid(row=self.rows, column=1, padx=20, pady=2, sticky="e")
        self.rows += 1
        return value_lbl

    def get_ohm_temp(self):
        """Fetches temp from Open Hardware Monitor (localhost:8085)"""
        try:
            # OHM runs a local webserver with a JSON file of all your hardware
            response = requests.get('http://localhost:8085/data.json', timeout=0.5)
            data = response.json()
            
            # Traverse the JSON tree to find CPU Temperature
            # Usually: Children -> (CPU Name) -> Children -> Temperatures -> CPU Package
            for hardware in data['Children']:
                if 'cpu' in hardware['ImageURL']: # Find the CPU node
                    for child in hardware['Children']:
                        if child['Text'] == 'Temperatures':
                            for sensor in child['Children']:
                                if 'Package' in sensor['Text'] or 'Core' in sensor['Text']:
                                    # Return the value (e.g., "55.0 °C")
                                    return sensor['Value']
            return "N/A (Check OHM)"
        except:
            return "N/A (Start OHM App)"

    def update_metrics(self):
        # 1. CPU Load
        self.lbl_cpu_load.config(text=f"{psutil.cpu_percent()}%")

        # 2. CPU Temp (Via Bridge)
        temp_str = self.get_ohm_temp()
        self.lbl_cpu_temp.config(text=temp_str)
        if "N/A" in temp_str:
            self.lbl_cpu_temp.config(foreground="gray")
        else:
            # Parse number to change color if hot
            try:
                temp_val = float(temp_str.split()[0])
                self.lbl_cpu_temp.config(foreground="#ff4444" if temp_val > 80 else "#00ff99")
            except:
                pass

        # 3. RAM (Critical for you)
        ram = psutil.virtual_memory()
        self.lbl_ram.config(text=f"{ram.percent}% Used", 
                            foreground="#ff4444" if ram.percent > 85 else "white")

        # 4. Swap Memory (Virtual RAM)
        # If this is high (>50%), your PC is using the SSD because RAM is full
        swap = psutil.swap_memory()
        self.lbl_swap.config(text=f"{swap.percent}% ({swap.used // (1024**2)} MB)")

        # 5. Disk I/O (Speed)
        disk_now = psutil.disk_io_counters()
        # Calculate difference since last check (approx 1 sec)
        read_speed = (disk_now.read_bytes - self.previous_disk_io.read_bytes) / 1024 / 1024
        write_speed = (disk_now.write_bytes - self.previous_disk_io.write_bytes) / 1024 / 1024
        self.lbl_disk.config(text=f"R: {read_speed:.1f} MB/s | W: {write_speed:.1f} MB/s")
        self.previous_disk_io = disk_now

        # 6. Battery
        if hasattr(psutil, "sensors_battery"):
            batt = psutil.sensors_battery()
            if batt:
                plugged = "⚡" if batt.power_plugged else "🔋"
                self.lbl_batt.config(text=f"{batt.percent}% {plugged}")
            else:
                self.lbl_batt.config(text="Not Detected")

        # Update in 1 second
        self.after(1000, self.update_metrics)

if __name__ == "__main__":
    app = AdvancedMonitor()
    app.mainloop()