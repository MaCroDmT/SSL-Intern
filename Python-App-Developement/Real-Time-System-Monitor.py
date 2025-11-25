import tkinter as tk
import psutil
import time
import os
import sys

# Attempt to import the Windows-specific WMI library
try:
    import wmi
    IS_WINDOWS = True
except ImportError:
    IS_WINDOWS = False

# --- Configuration ---
UPDATE_INTERVAL_MS = 1000  # Update data every 1 second (1000ms)
BG_COLOR = "#000000"       # Background color (Black)
FG_COLOR = "#FF8C00"       # Foreground/Text color (Dark Orange, similar to the image)
FONT_STYLE = ("Inter", 10, "bold") # Font for the text

# Global WMI connection object
w = None
if IS_WINDOWS:
    try:
        w = wmi.WMI(namespace="root\\wmi")
    except Exception as e:
        print(f"WMI Initialization Error: {e}")
        w = None

# --- Data Retrieval Functions ---

def get_cpu_temp_wmi():
    """Fetches CPU Temperature using Windows WMI (requires 'wmi' library)."""
    if w is None:
        return "N/A (WMI Fail)"
    
    try:
        # Querying the MSAcpi_ThermalZoneTemperature class for thermal data
        # Note: This often works for general CPU temp, but may not be the 'Core Temp'
        # Fallback 1: Try Win32_TemperatureSensor (often empty/inaccurate on modern hardware)
        # Fallback 2: Try specific WMI classes that return Celsius (like WMI's thermal zone)
        
        # A common, simple WMI query for temperature (usually in Kelvin * 10)
        # We rely on psutil first, as it's more direct for CPU cores.
        # However, since psutil failed, we try a more system-wide approach.
        
        # We will try to get the temperature from the CPU Thermal Zone
        temperatures = w.MSAcpi_ThermalZoneTemperature()
        if temperatures:
            # Get the highest reported temperature, convert from Kelvin*10 to Celsius
            max_temp_k = max(t.CurrentTemperature for t in temperatures)
            max_temp_c = (max_temp_k / 10.0) - 273.15
            return f"{max_temp_c:.1f}"
        
        return "N/A (No WMI Data)"
        
    except Exception as e:
        # print(f"WMI Temp Error: {e}") # Debugging aid
        return "N/A (WMI Error)"


def get_system_stats():
    """Fetches current CPU, RAM, and Temperature statistics."""
    stats = {}
    
    # 1. CPU Usage and Frequency
    stats['cpu_usage'] = psutil.cpu_percent(interval=None)
    cpu_freq = psutil.cpu_freq()
    stats['cpu_freq'] = f"{cpu_freq.current / 1000:.1f}" if cpu_freq else "N/A" # Convert from Mhz to Ghz
    
    # 2. RAM Usage
    ram = psutil.virtual_memory()
    stats['ram_used_gb'] = round(ram.used / (1024 ** 3), 1)
    stats['ram_total_gb'] = round(ram.total / (1024 ** 3), 1)
    
    # 3. CPU Temperature (Attempt psutil first, then WMI if on Windows)
    stats['cpu_temp'] = "N/A"
    if IS_WINDOWS:
        # Try psutil's direct access (often fails without low-level driver)
        try:
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps and temps['coretemp']:
                # Find the highest reported core temperature
                package_temp = max(s.current for s in temps['coretemp'])
                stats['cpu_temp'] = f"{package_temp:.1f}"
        except Exception:
            # psutil failed, fall back to WMI which might work better for Dell systems
            stats['cpu_temp'] = get_cpu_temp_wmi()
    else:
        # Non-Windows systems rely solely on psutil
        try:
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps and temps['coretemp']:
                package_temp = max(s.current for s in temps['coretemp'])
                stats['cpu_temp'] = f"{package_temp:.1f}"
        except Exception:
            stats['cpu_temp'] = "N/A (Sensor Fail)"


    # 4. CPU Power (Watts) - Requires specialized low-level APIs, WMI is usually inaccurate for this.
    stats['cpu_power'] = "---" # Keeping as placeholder

    # 5. GPU Data (Iris Xe) - Requires specialized libraries (e.g., Intel-specific)
    stats['gpu_usage'] = "---"
    stats['gpu_temp'] = "---"
    
    return stats

# --- UI Setup and Update ---

class SystemMonitorApp:
    def __init__(self, master):
        self.master = master
        master.title("System Monitor")
        
        # Check for WMI and Admin recommendation
        admin_warning = "RUN AS ADMIN for Temp/Power!"
        
        if IS_WINDOWS and w is not None:
             admin_warning = "WMI Active. Run as Admin if Temp fails."
        elif IS_WINDOWS and w is None:
             admin_warning = "WMI Import Failed. Install 'pip install wmi'."
        elif not IS_WINDOWS:
             admin_warning = "Linux/macOS: Using psutil only."


        # Make the window frameless and always on top
        master.overrideredirect(True)
        master.attributes('-topmost', True)
        
        # Set background color and transparency
        master.config(bg=BG_COLOR)
        
        # Initial position (Top Right Corner)
        self.x = master.winfo_screenwidth() - 250
        self.y = 10
        master.geometry(f'+{self.x}+{self.y}')

        # Create labels dictionary to hold references to the text widgets
        self.labels = {}
        
        # Define layout: (Label, Data Field Key, Unit/Suffix)
        monitor_fields = [
            ("CPU Temp:", "cpu_temp", "°C"),
            ("CPU Load:", "cpu_usage", "%"),
            ("CPU Freq:", "cpu_freq", "GHz"),
            ("CPU Power:", "cpu_power", "W"),
            ("RAM Used:", "ram_used_gb", "GB"),
            ("GPU Load:", "gpu_usage", "%"),
            ("GPU Temp:", "gpu_temp", "°C"),
        ]

        # Build the UI table
        for i, (label_text, key, unit) in enumerate(monitor_fields):
            # Label (e.g., "CPU:")
            tk.Label(master, text=label_text, bg=BG_COLOR, fg=FG_COLOR, font=FONT_STYLE, anchor='w', padx=5).grid(row=i, column=0, sticky='w')
            
            # Value (e.g., 65.0)
            value_label = tk.Label(master, text="--", bg=BG_COLOR, fg=FG_COLOR, font=FONT_STYLE, anchor='w')
            value_label.grid(row=i, column=1, sticky='w')
            self.labels[key] = value_label  # Store reference
            
            # Unit (e.g., °C, %)
            tk.Label(master, text=unit, bg=BG_COLOR, fg=FG_COLOR, font=FONT_STYLE, anchor='w').grid(row=i, column=2, sticky='w')
            
        # Add instruction label and status
        admin_color = "#FF0000" if "Fail" in admin_warning else "#00FF00"
        
        tk.Label(master, text=f"Status: {admin_warning}", bg=BG_COLOR, fg=admin_color, font=("Inter", 8, "bold"), pady=5).grid(row=len(monitor_fields), column=0, columnspan=3)
        tk.Label(master, text="Drag to Move | Close window to exit", bg=BG_COLOR, fg="#666666", font=("Inter", 8), pady=0).grid(row=len(monitor_fields) + 1, column=0, columnspan=3)

        # Make the window draggable
        self.master.bind("<Button-1>", self.start_move)
        self.master.bind("<B1-Motion>", self.do_move)

        # Start the update loop
        self.update_stats()

    def update_stats(self):
        """Fetches new data and updates the labels."""
        stats = get_system_stats()
        
        # Update the UI elements
        self.labels['cpu_temp'].config(text=stats['cpu_temp'])
        self.labels['cpu_usage'].config(text=f"{stats['cpu_usage']:.1f}")
        self.labels['cpu_freq'].config(text=stats['cpu_freq'])
        self.labels['cpu_power'].config(text=stats['cpu_power']) 
        
        # Format RAM usage as "Used GB / Total GB"
        ram_text = f"{stats['ram_used_gb']:.1f} / {stats['ram_total_gb']:.1f}"
        self.labels['ram_used_gb'].config(text=ram_text)
        
        # Display GPU place holders
        self.labels['gpu_temp'].config(text=stats['gpu_temp'])
        self.labels['gpu_usage'].config(text=stats['gpu_usage'])

        # Schedule the next update
        self.master.after(UPDATE_INTERVAL_MS, self.update_stats)

    # --- Drag Functionality ---
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        new_x = self.master.winfo_x() + deltax
        new_y = self.master.winfo_y() + deltay
        self.master.geometry(f"+{new_x}+{new_y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()